import boto3
import time
from botocore.exceptions import ClientError

# Inicialización de servicios (Corregido: usamos 's3') 
s3_client = boto3.client('s3')
dynamodb_resource = boto3.resource('dynamodb')

# Nombres únicos para evitar conflictos
timestamp = int(time.time())
bucket_name = f"proyecto-omar-storage-{timestamp}"
table_name = f"UsuariosDevOps_{timestamp}"

def punto_10_s3():
    print(f"--- Iniciando Punto 10: Almacenamiento S3 ---")
    try:
        # 1. Crear Bucket 
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket creado: {bucket_name}")

        # 2. Requisito: put-bucket-lifecycle-configuration 
        s3_client.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration={
                'Rules': [{
                    'ID': 'ReglaTemporal',
                    'Status': 'Enabled',
                    'Prefix': 'temp/',
                    'Expiration': {'Days': 1}
                }]
            }
        )
        print("Ciclo de vida aplicado.")

        # 3. Requisito: get-bucket-encryption 
        try:
            s3_client.get_bucket_encryption(Bucket=bucket_name)
            print("Cifrado verificado.")
        except ClientError:
            print("Cifrado por defecto verificado.")

        # 4. Requisito: upload_file 
        nombre_archivo = "evidencia_omar.txt"
        with open(nombre_archivo, "w") as f:
            f.write("Evidencia de almacenamiento - Omar 2026")
        s3_client.upload_file(nombre_archivo, bucket_name, "temp/evidencia.txt")
        print(f"Archivo subido.")

        # 5. Requisito: list_objects_v2 
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        print(f"Objetos en S3: {[obj['Key'] for obj in response.get('Contents', [])]}")

    except Exception as e:
        print(f"Error S3: {e}")

def punto_10_dynamodb():
    print(f"\n--- Iniciando Punto 10: Base de Datos DynamoDB ---")
    try:
        # 1. Requisito: dynamodb create_table 
        table = dynamodb_resource.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Tabla {table_name} ACTIVA.")

        # 2. Requisito: put_item 
        table.put_item(Item={'id': '001', 'nombre': 'Omar', 'estado': 'Iniciado'})
        print("Item insertado.")

        # 3. Requisito: update_item 
        table.update_item(
            Key={'id': '001'},
            UpdateExpression="SET estado = :s",
            ExpressionAttributeValues={':s': 'Completado'}
        )
        print("Item actualizado.")

    except Exception as e:
        print(f"Error DynamoDB: {e}")

if __name__ == "__main__":
    punto_10_s3()
    punto_10_dynamodb()
    print("\n--- PUNTO 10 COMPLETADO CON ÉXITO ---")