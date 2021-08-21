FROM python:3.8-slim

COPY . .

RUN pip3 install --prefer-binary -r requirements.txt

ENTRYPOINT ["python3", "inject.py"]
