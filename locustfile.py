from locust import User, task, between
import paho.mqtt.client as mqtt
import random, time
import config

class MQTTUser(User):
    wait_time = between(1, 2)  # 센서마다 퍼블리시 주기

    def on_start(self):
        self.client = mqtt.Client()
        self.client.connect(config.AWS_IOT_BROKER, config.AWS_IOT_PORT, 60)
        self.client.loop_start()

    @task
    def publish_sensor_data(self):
        temp = round(random.uniform(20, 30), 2)
        self.client.publish(config.AWS_IOT_TOPIC, payload=str(temp))

    def on_stop(self):
        self.client.loop_stop()
        self.client.disconnect()