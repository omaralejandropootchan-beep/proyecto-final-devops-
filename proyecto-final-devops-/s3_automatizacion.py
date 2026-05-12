import boto3
import os

s3 = boto3.client('s3')
# Usando el bucket que confirmamos antes
bucket_name = 'proyecto-omar-storage-1778619038' 

# 1. Crear archivo de prueba local
file_name = 'test_devops.txt'
with open(file_name, 'w') as f:
    f.write('Archivo de prueba para el proyecto final de DevOps - Omar Alejandro Poot Chan')

# 2. Subir al bucket en la carpeta pruebas/
object_name = f'pruebas/{file_name}'
s3.upload_file(file_name, bucket_name, object_name)
print(f"Archivo subido exitosamente a: {object_name}")

# 3. Listar objetos
response = s3.list_objects_v2(Bucket=bucket_name)
print("\nContenido actual del Bucket:")
for obj in response.get('Contents', []):
    print(f"- Nombre: {obj['Key']} | Tamaño: {obj['Size']} bytes")
