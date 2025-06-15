from locust import HttpUser, task, between
import random
import json

class ServiceUser(HttpUser):
    wait_time = between(1, 3)  # 요청 간 대기 시간(초)

    @task
    def call_backend_api(self):
        # 실제 API 엔드포인트와 요청 데이터에 맞게 수정
        url = "/predict"
        payload = {
            "sensor_id": f"sensor_{random.randint(1, 100)}",
            "data": [random.random() for _ in range(10)]
        }
        headers = {"Content-Type": "application/json"}
        self.client.post(url, data=json.dumps(payload), headers=headers)
