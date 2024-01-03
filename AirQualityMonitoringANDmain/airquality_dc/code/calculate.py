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

import logging


logger = logging.getLogger("main.measure.conversion")


class AirQualityMonitoringCalculation:

    def __init__(self, config):
        calculation_conf = config['calculation']


    def calculate(self, sample):
        logger.debug(f"TVOC: {sample.tvoc} CO2: {sample.ppm} AQI: {sample.aqi}")
        return {"TVOC": str(sample.tvoc), "CO2": str(sample.ppm), "AQI": str(sample.aqi)}
