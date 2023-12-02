import os
from dotenv import load_dotenv

# Carga las variables de entorno desde .env en el directorio actual
load_dotenv()

# Prueba de lectura de variables
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_default_region = os.environ.get('AWS_DEFAULT_REGION')

print(f"AWS_ACCESS_KEY_ID: {aws_access_key_id}")
print(f"AWS_SECRET_ACCESS_KEY: {aws_secret_access_key}")
print(f"AWS_DEFAULT_REGION: {aws_default_region}")