# Introduction

This project is used to produce simulated machine data to a Kafka topic.

## Configuration

Any environment variable that is prefixed with `KAFKA_` will be passed as config to the Kafka 
producer. For example `KAFKA_BOOTSTRAP_SERVERS` will be passed as `bootstrap_servers` to the python
KafkaProducer class. 

## Minimal Config

This configuration will work on a Kafka Cluster that does not have security configured.

| Environment Variable    | Value      |
|-------------------------|------------|
| KAFKA_BOOTSTRAP_SERVERS | kafka:9092 |
| TOPIC                   | testing    |

## Kubernetes Example

This configuration will work on a Kafka Cluster that does not have security configured.

```yaml
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: demo-kafka
  namespace: demo-kafka
spec:
  replicas: 1
  selector:
    matchLabels:
      demo: kafka
  serviceName: demo
  template:
    metadata:
      labels:
        demo: kafka
    spec:
      containers:
        - image: nstream/nstream-machine-demo-producer:0.0.1
          imagePullPolicy: Always
          name: demo
          env:
            - name: KAFKA_BOOTSTRAP_SERVERS
              value: kafka-01:9071
            - name: TOPIC
              value: testing
          resources:
            limits:
              cpu: ".5"
              memory: 256Mi
            requests:
              cpu: ".5"
              memory: 256Mi
```