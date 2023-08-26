mlflow server \
    --backend-store-uri "postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB" \
    --default-artifact-root s3://${AWS_S3_BUCKET}/ \
    --host 0.0.0.0 \
    --port $MLFLOW_PORT