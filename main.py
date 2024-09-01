
#!/usr/bin/env python3

import requests
import json
import argparse
import socket

from influxdb import InfluxDBClient
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("latitude", type=float, help="Forecast Latitude")
    argparser.add_argument("longitude", type=float, help="Forecast Longitude")
    argparser.add_argument("influx_token", type=str, help="InfluxDB token")
    argparser.add_argument("--influx_url", type=str, default="localhost:8086", help="InfluxDB URL")
    argparser.add_argument("--influx_org", type=str, default="homelab", help="InfluxDB organisation")
    argparser.add_argument("--influx_bucket", type=str, default="weather-forecast", help="InfluxDB bucket")
    argparser.add_argument("--locality", type=str, default="Home", help="forecast Locality/Label")
    args = argparser.parse_args()
    
    useragent = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'
    url = 'https://api.met.no/weatherapi/locationforecast/2.0/.json?lat={latitude}&lon={longitude}'.format(latitude=args.latitude,longitude=args.longitude)

    influx_client = InfluxDBClient(
        url=args.influx_url,
        token=args.influx_token,
        org=args.influx_org,
    )

    influx = influx_client.write_api(write_options=SYNCHRONOUS)

    data = json.loads(
        requests.get(url, headers={'User-Agent': useragent}
    ).content.decode('utf-8'))

    timeseries = data['properties']['timeseries']

    for timeserie in timeseries:
        stats = {k:v for k,v in timeserie['data']['instant']['details'].items() if not isinstance(v,dict)}

        if 'next_1_hours' in timeserie['data']:
            stats['precipitation_amount'] = timeserie['data']['next_1_hours']['details']['precipitation_amount']

        influx.write(
            args.influx_bucket, 
            args.influx_org, 
            [{
                "measurement": "WeatherForecast",
                "tags": {
                    "Server": socket.getfqdn(),
                    "Longitude": data['geometry']['coordinates'][0],
                    "Latitude": data['geometry']['coordinates'][1],
                    "Height": str(float(data['geometry']['coordinates'][2])*0.3048),
                    "Location": args.locality
                },
                "time": timeserie['time'],
                "fields": stats
            }]
        )
