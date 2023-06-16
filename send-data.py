import math
import random
import time
import os
from kafka import KafkaProducer
import logging
import sys
logger = logging.getLogger('kafka')
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


producer_settings = {}

for k, v in os.environ.items():
    key = k.lower()
    if key.startswith("kafka_"):
        setting_name = key.replace("kafka_", "")
        producer_settings[setting_name] = v

bootstrap_servers = producer_settings.get("bootstrap_servers")

if bootstrap_servers is None:
    raise Exception('bootstrap_servers must be configured. Set environment variable KAFKA_BOOTSTRAP_SERVERS')
else:
    print("Connecting to " + producer_settings["bootstrap_servers"])

producer_settings['key_serializer'] = str.encode
producer_settings['value_serializer'] = str.encode

topic = os.environ.get('TOPIC')

if topic is None:
    raise Exception('topic must be configured. Set environment variable TOPIC')
else:
    print("Producing to topic " + topic)

interval = 10

if not os.environ.get('INTERVAL') is None:
    interval = int(os.environ.get('INTERVAL'))

producer = KafkaProducer(**producer_settings)
machines = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'N1', 'N2', 'N3', 'N4', 'O1', 'O2', 'P1', 'P2', 'Q1', 'Q2']

#Send data to all the machines, generate random values for health, current, power, voltage
while True:
    for machine in machines:
        base_health_score = random.random() * 20
        rnd = random.random()
        boost = 0
        if (0.05 <= rnd and rnd < 0.15):
            boost += 20
        elif (0.15 <= rnd and rnd < 0.25):
            boost += 40
        elif (0.25 <= rnd and rnd < 0.45):
            boost += 60
        elif (rnd >= 0.45):
            boost += 80

        health_score = math.ceil((boost + base_health_score) * 100.0) / 100.0
        current = math.ceil((random.random() * 20) * 100.0) / 100.0
        power = math.ceil((random.random() * 20) * 100.0) / 100.0
        voltage = math.ceil((random.random() * 20) * 100.0) / 100.0
        payload = '{"current":' + str(current) + ',"power":' + str(power) + ',"voltage":' + str(voltage) + ',"health":' + str(health_score) + ',"id":' + machine  + '}'
        keyVal = str(machine)
        future = producer.send(topic=topic, key=keyVal, value=payload)
        result = future.get(timeout=60)
        producer.flush()

    time.sleep(interval)