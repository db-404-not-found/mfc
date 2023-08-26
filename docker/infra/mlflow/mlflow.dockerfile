FROM python:3.11-slim

RUN pip install -U pip && pip install boto3 psycopg2-binary mlflow

COPY ./mlflow-start.sh /
RUN chmod +x /mlflow-start.sh

CMD /mlflow-start.sh