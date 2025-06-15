from locust import HttpUser, task, between
import random
import json

class ModelUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def call_model_inference(self):
        # FastAPI 모델 서버의 엔드포인트와 입력 포맷에 맞게 수정
        url = "/inference"
        payload = {
            "input": [random.random() for _ in range(10)]
        }
        headers = {"Content-Type": "application/json"}
        self.client.post(url, data=json.dumps(payload), headers=headers)
