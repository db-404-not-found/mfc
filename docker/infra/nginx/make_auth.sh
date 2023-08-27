set -x
echo -n "${MLFLOW_USER}:" > /etc/mlflow/.htpasswd
openssl passwd -apr1 "${MLFLOW_PASSWORD}" >> /etc/mlflow/.htpasswd
echo "Auth basic was created!"