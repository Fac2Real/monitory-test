import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

AWS_IOT_BROKER = os.getenv("AWS_IOT_BROKER")
AWS_IOT_PORT = int(os.getenv("AWS_IOT_PORT", 8883))  # 기본값 설정
AWS_IOT_TOPIC = os.getenv("AWS_IOT_TOPIC")

AWS_IOT_CLIENT_ID = os.getenv("AWS_IOT_CLIENT_ID")
AWS_IOT_CA_PEM_PATH = os.getenv("AWS_IOT_CA_PEM_PATH")
AWS_IOT_CERT_PATH = os.getenv("AWS_IOT_CERT_PATH")
AWS_IOT_PRIVATE_KEY_PATH = os.getenv("AWS_IOT_PRIVATE_KEY_PATH")

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
