#!/usr/bin/env sh

if [ -z "${LATITUDE}" ]; then
  echo "ERROR: Env var LATITUDE missing"
  sleep 30
  exit 1
fi

if [ -z "${LONGITUDE}" ]; then
  echo "ERROR: Env var LONGITUDE missing"
  sleep 30
  exit 1
fi

if [ -z "${INFLUXDB_TOKEN}" ]; then
  echo "ERROR: Env var INFLUXDB_TOKEN missing"
  sleep 30
  exit 1
fi

if [ -z "${INFLUXDB_URL}" ]; then
  echo "ERROR: Env var INFLUXDB_URL missing"
  sleep 30
  exit 1
fi

if [ -z "${INFLUXDB_ORG}" ]; then
  echo "ERROR: Env var INFLUXDB_ORG missing"
  sleep 30
  exit 1
fi

if [ -z "${INFLUXDB_BUCKET}" ]; then
  echo "ERROR: Env var INFLUXDB_BUCKET missing"
  sleep 30
  exit 1
fi

while true; do
    echo "fetch weather forecast..."
    python3 main.py ${LATITUDE} ${LONGITUDE} "${INFLUXDB_TOKEN}" --influx_url "${INFLUXDB_URL}" --influx_org "${INFLUXDB_ORG}" --influx_bucket "${INFLUXDB_BUCKET}" --locality "${LOCALITY:-Home}"
    echo "sleep ${UPDATE_INTERVAL_IN_SECONDS:-21600}"
    sleep ${UPDATE_INTERVAL_IN_SECONDS:-21600}
done
