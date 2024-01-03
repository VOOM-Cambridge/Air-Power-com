# ----------------------------------------------------------------------
#
#    Air Quality Monitoring -- This digital solution measures,
#    reports and records the concentration of Volatile Organic Compound (VOC)
#    CO2 and VOC index in the environment. 
#    The solution provides a Grafana dashboard that 
#    displays VOC and CO2 concentration and VOC Index, and an InfluxDB database 
#    to store timestamp, VOC, CO2 and VOC Index. 
#
#    Copyright (C) 2023  Shoestring and University of Cambridge
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/.
#
# ----------------------------------------------------------------------


# run at poll rate
# make requests
# extract variables
# output variables

import datetime
import logging
import multiprocessing
import time

import importlib
import zmq

import calculate as calc

logger = logging.getLogger("main.measure")
context = zmq.Context()


class AirQualityMeasureBuildingBlock(multiprocessing.Process):
    def __init__(self, config, zmq_conf):
        super().__init__()

        self.config = config
        self.constants = config['constants']

        # declarations
        self.zmq_conf = zmq_conf
        self.zmq_out = None

        self.collection_interval = config['sampling']['sample_interval']
        self.sample_count = config['sampling']['sample_count']
        self.adc_module = config['adc']['adc_module']
        logger.info(f"read adc module {self.adc_module} from config")

    def do_connect(self):
        self.zmq_out = context.socket(self.zmq_conf['type'])
        if self.zmq_conf["bind"]:
            self.zmq_out.bind(self.zmq_conf["address"])
        else:
            self.zmq_out.connect(self.zmq_conf["address"])

    def run(self):
        logger.info("started")
        self.do_connect()

        # timezone determination
        __dt = -1 * (time.timezone if (time.localtime().tm_isdst == 0) else time.altzone)
        tz = datetime.timezone(datetime.timedelta(seconds=__dt))
        #
        today = datetime.datetime.now().date()
        next_check = (datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(days=1)).timestamp()

        run = True
        period = self.collection_interval

        # get correct ADC module
        try:
            adc_module = importlib.import_module(f"adc.{self.adc_module}")
            logger.debug(f"Imported {self.adc_module}")
        except ModuleNotFoundError as e:
            logger.error(f"Unable to import module {self.adc_module}. Stopping!!")
            return

        adc = adc_module.ADC(self.config)

        calculation = calc.AirQualityMonitoringCalculation(self.config)
        

        sleep_time = period
        t = time.time()
        while run:
            t += period

            # Collect samples from ADC
            try:
                sample = adc.sample()
            except Exception as e:
                logger.error(f"Sampling lead to exception{e}")

            # handle timestamps and timezones
            if time.time() > next_check:
                __dt = -1 * (time.timezone if (time.localtime().tm_isdst == 0) else time.altzone)
                tz = datetime.timezone(datetime.timedelta(seconds=__dt))
                # set up next check
                today = datetime.datetime.now().date()
                next_check = (datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(
                    days=1)).timestamp()

            # dispatch messages

            # capture timestamp
            timestamp = datetime.datetime.now(tz=tz).isoformat()

            # convert
            results = calculation.calculate(sample)
            payload = {**results, **self.constants, "timestamp": timestamp}

                # send
            output = {"path": "", "payload": payload}
            self.dispatch(output)

            # handle sample rate
            if sleep_time <= 0:
                logger.warning(f"previous loop took longer that expected by {-sleep_time}s")
                t = t - sleep_time  # prevent free-wheeling to make up the slack

            sleep_time = t - time.time()
            time.sleep(max(0.0, sleep_time))
        logger.info("done")

    def dispatch(self, output):
        logger.info(f"dispatch to { output['path']} of {output['payload']}")
        self.zmq_out.send_json({'path': output.get('path', ""), 'payload': output['payload']})
