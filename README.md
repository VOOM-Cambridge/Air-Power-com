To run this code follow the followign guides in this order. The main steps are:
1) Run the set up logging code
2) Run the docker compose for air monitoring
3) Run the docker compose for power monitoring

The guides to help do this are:
For 1) and 2):
https://community.digitalshoestring.net/t/air-quality-monitoring-co2-voc-aqi-starter-solution-guide/172

For step 3):
https://community.digitalshoestring.net/t/power-monitoring-guide/84

Once both parts are running, if it is the first time, check that both influx buckets are created. If not you may have to create them manually in the influx interface as "localhost:8086"
****
