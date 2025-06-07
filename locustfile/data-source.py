
import json
import random
import uuid
import os
from locust import task, between
from locust_plugins.users.mqtt import MqttUser
from datetime import datetime, timezone

AWS_IOT_ENDPOINT = os.getenv("AWS_IOT_BROKER")
PORT = 8883

class SensorMqttUser(MqttUser):
    host = AWS_IOT_ENDPOINT
    port = PORT

    wait_time = between(1, 5)

    def on_start(self):
        """
        각 가상 사용자가 시작될 때 호출됩니다.
        여기서 사용자별 고유 ID 등을 설정합니다.
        """
        now_str = datetime.now().strftime("%Y%m%d%H%M%S")
        rand_suffix_zone = random.randint(100, 999)
        rand_suffix_equip = random.randint(100, 999)

        self.zone_id = f"{now_str}-{rand_suffix_zone}"
        self.equip_id = f"{now_str}-{rand_suffix_equip}"

        sensor_prefix = "UA10H-REAL-"
        sensor_numeric_part = random.randint(24000000, 24999999)
        self.sensor_id = f"{sensor_prefix}{sensor_numeric_part}"

        print(f"Starting MQTT user. Zone: {self.zone_id}, Equip: {self.equip_id}, Sensor: {self.sensor_id}")

        # AWS IoT Core에 연결하려면 인증서 설정이 필요할 수 있습니다.
        self.client.tls_set(ca_certs="../certs/root.pem",
                                certfile="../certs/certificate.pem.crt",
                                keyfile="../certs/private.pem.key")

    def _generate_utc_ingestion_time_ms(self):
        """현재 UTC 시간을 Unix timestamp (밀리초)로 반환합니다."""
        return int(datetime.now(timezone.utc).timestamp() * 1000)

    @task(3)
    def send_environment_data(self):
        category = "ENVIRONMENT"
        # 환경 센서 종류 중 하나를 랜덤 선택
        sensor_type, val = random.choice([
            ("humid", round(random.uniform(0, 100), 2)),
            ("temp", round(random.uniform(-35, 50), 2)),
            ("vibration", random.randint(0, 10)),
            ("voc", round(random.uniform(0, 2000), 2)),
        ])

        message_data = {
            "zoneId": self.zone_id,
            "equipId": self.equip_id,
            "sensorId": self.sensor_id,
            "sensorType": sensor_type,
            "val": val,
            "utc_ingestion_time": self._generate_utc_ingestion_time_ms(),
            "category": category
        }
        payload = json.dumps(message_data)
        topic = f"sensor_data/{category}/{self.zone_id}/{self.equip_id}/{self.sensor_id}/{sensor_type}"
        
        self.client.publish(topic, payload, qos=1)
        print(f"Published to {topic}: {payload}")

    @task(2)
    def send_wearable_data(self):
        category = "WEARABLE"
        sensor_type, val = random.choice([
            ("heartRate", random.randint(50, 150))
        ])

        message_data = {
            "zoneId": self.zone_id,
            "equipId": self.sensor_id,
            "sensorId": self.sensor_id,
            "sensorType": sensor_type,
            "val": val,
            "utc_ingestion_time": self._generate_utc_ingestion_time_ms(),
            "category": category
        }
        payload = json.dumps(message_data)
        topic = f"sensor_data/{category}/{self.zone_id}/{self.sensor_id}/{sensor_type}"
        
        self.client.publish(topic, payload, qos=1)
        print(f"Published to {topic}: {payload}")

    @task(1)
    def send_equipment_data(self):
        category = "EQUIPMENT"
        sensor_type, val = random.choice([
            ("temp", round(random.uniform(10, 150), 3)),
            ("vibration", round(random.uniform(-0.5, 5), 2)),
            ("pressure", round(random.uniform(3.5, 80), 2)),
            ("active_power", round(random.uniform(0, 241576), 2)),
            ("reactive_power", round(random.uniform(0, 478960), 2)),
            ("humidity", round(random.uniform(10, 90), 2)),
        ])
        
        message_data = {
            "zoneId": self.zone_id,
            "equipId": self.equip_id,
            "sensorId": self.sensor_id,
            "sensorType": sensor_type,
            "val": val,
            "utc_ingestion_time": self._generate_utc_ingestion_time_ms(),
            "category": category
        }
        payload = json.dumps(message_data)
        topic = f"sensor_data/{category}/{self.zone_id}/{self.equip_id}/{self.sensor_id}/{sensor_type}"
        
        self.client.publish(topic, payload, qos=1)
        print(f"Published to {topic}: {payload}")
