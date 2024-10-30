FROM python:3.10.14-alpine

WORKDIR /app

COPY requirements.txt /app
COPY entrypoint.sh /app
COPY src /app/src

# requirements.txt 파일을 기반으로 패키지 설치
RUN pip install -r /app/requirements.txt

# entrypoint.sh에 실행 권한 부여
RUN chmod +x /app/entrypoint.sh

# ENTRYPOINT 설정 (쉘 스크립트를 개별 인수로 실행)
ENTRYPOINT ["sh", "/app/entrypoint.sh"]