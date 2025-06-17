import json
import random
import uuid
import os
from dotenv import load_dotenv
from locust import task, between
from locust_plugins.users.mqtt import MqttUser
from datetime import datetime, timezone

load_dotenv()

# 환경 변수에서 AWS IoT 엔드포인트를 가져옵니다.
AWS_IOT_ENDPOINT = os.getenv("AWS_IOT_BROKER")
if not AWS_IOT_ENDPOINT:
    print("Error: AWS_IOT_BROKER environment variable not set.")
    exit(1)

PORT = 8883

class SensorMqttUser(MqttUser):
    host = AWS_IOT_ENDPOINT
    port = PORT
    wait_time = between(1, 5)

    def on_start(self):
        """각 가상 사용자가 시작될 때 호출됩니다."""
        # 1. 고유한 클라이언트 ID를 명시적으로 설정하여 충돌 방지
        self.client_id = f"locust-user-{uuid.uuid4()}"

        # 2. 사용자별 고유 데이터 생성
        now_str = datetime.now().strftime("%Y%m%d%H%M%S")
        rand_suffix = random.randint(100, 999)
        self.zone_id = f"zone-{now_str}-{rand_suffix}"
        self.equip_id = f"equip-{now_str}-{rand_suffix}"
        sensor_prefix = "UA10H-REAL-"
        sensor_numeric_part = random.randint(24000000, 24999999)
        self.sensor_id = f"{sensor_prefix}{sensor_numeric_part}"

        print(f"Starting MQTT user with Client ID: {self.client_id}")

        # 3. AWS IoT Core 인증 설정
        #    이 스크립트를 실행하는 위치를 기준으로 certs 폴더를 찾습니다.
        #    예: locustfile/data-source-iot.py 와 certs/ 가 같은 부모 폴더에 있어야 함
        try:
            self.client.tls_set(ca_certs="../certs/root.pem",
                                    certfile="../certs/certificate.pem.crt",
                                    keyfile="../certs/private.pem.key")
        except FileNotFoundError:
            print(f"ERROR: Certificates not found. Make sure the 'certs' folder is in the parent directory of your script.")
            self.stop()
            return

    def _generate_utc_ingestion_time_ms(self):
        """현재 UTC 시간을 Unix timestamp (밀리초)로 반환합니다."""
        return int(datetime.now(timezone.utc).timestamp() * 1000)
        
    def _publish_data(self, topic, payload):
        """locust-plugins의 publish를 호출하여 통계를 자동으로 집계합니다."""
        self.client.publish(topic, payload, qos=1)

    def _create_base_message(self, category, sensor_type, val):
        """메시지 페이로드의 기본 구조를 생성합니다."""
        return {
            "msgId": str(uuid.uuid4()),
            "zoneId": self.zone_id,
            "equipId": self.equip_id,
            "sensorId": self.sensor_id,
            "sensorType": sensor_type,
            "val": val,
            "utc_ingestion_time": self._generate_utc_ingestion_time_ms(),
            "category": category
        }

    # 아래 Task들은 정상적으로 동작하므로 수정할 필요 없습니다.
    @task(3)
    def send_environment_data(self):
        category = "ENVIRONMENT"
        sensor_type, val = random.choice([
            ("humid", round(random.uniform(0, 100), 2)),
            ("temp", round(random.uniform(-35, 50), 2)),
            ("vibration", random.randint(0, 10)),
            ("voc", round(random.uniform(0, 2000), 2)),
        ])
        message_data = self._create_base_message(category, sensor_type, val)
        payload = json.dumps(message_data)
        topic = f"sensor/zone/{self.zone_id}/{self.equip_id}/{self.sensor_id}/{sensor_type}"
        self._publish_data(topic, payload)

    @task(2)
    def send_wearable_data(self):
        category = "WEARABLE"
        sensor_type, val = random.choice([("heartRate", random.randint(50, 150))])
        
        message_data = self._create_base_message(category, sensor_type, val)
        message_data["equipId"] = self.sensor_id
        
        payload = json.dumps(message_data)
        topic = f"wearable/{self.zone_id}/{self.sensor_id}/{sensor_type}"
        self._publish_data(topic, payload)

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
        message_data = self._create_base_message(category, sensor_type, val)
        payload = json.dumps(message_data)
        topic = f"sensor/{self.zone_id}/{self.equip_id}/{self.sensor_id}/{sensor_type}"
        self._publish_data(topic, payload)