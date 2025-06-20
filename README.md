# Monitory Test

**Monitory**의 부하 테스트와 모니터링을 위한 프로젝트입니다.

## 📁 프로젝트 구조

```
configs/         # AWS, Docker, Prometheus 등 환경설정 파일
dashboards/      # Grafana 등에서 사용할 대시보드 JSON 파일
locustfile/      # Locust 부하 테스트 스크립트 및 관련 모델/서비스 코드
reports/         # 테스트 결과 리포트 (CSV, HTML 등)
.github/         # GitHub 이슈/PR 템플릿
requirement.txt  # Python 패키지 의존성 목록
```

## 🚀 설치 방법

1. Python 3.10 이상 설치
2. 의존성 설치
   ```sh
   pip install -r requirement.txt
   ```

## 🧪 테스트 실행

Locust를 사용하여 부하 테스트를 실행할 수 있습니다.

```sh
locust -f locustfile/data-source-iot.py
```

또는

```sh
locust -f locustfile/service-user.py
```

## 📊 리포트 및 모니터링

- 테스트 결과는 `reports/` 폴더에 저장됩니다.
- Prometheus, Grafana 등과 연동하여 실시간 모니터링이 가능합니다.
- 대시보드 예시는 `dashboards/` 폴더 참고

## 🐞 이슈 및 기여

- 버그 리포트 및 기능 요청은 PR 또는 Issue로 남겨주세요.

## 📄 라이선스

(필요시 라이선스 정보 추가)
