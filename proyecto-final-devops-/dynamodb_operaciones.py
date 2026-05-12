import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# 1. Crear tabla
try:
    print("Creando tabla devops-tabla...")
    table = dynamodb.create_table(
        TableName='devops-tabla',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    table.wait_until_exists()
    print("Tabla creada con éxito.")
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceInUseException':
        print("La tabla ya existe, procediendo...")
        table = dynamodb.Table('devops-tabla')
    else:
        print(f"Error: {e}")

# 2. Insertar registro
table.put_item(Item={'id': '001', 'nombre': 'Omar', 'status': 'inicial'})
print("Registro insertado: id 001")

# 3. Actualizar registro (status es palabra reservada)
table.update_item(
    Key={'id': '001'},
    UpdateExpression="SET #s = :val",
    ExpressionAttributeNames={'#s': 'status'},
    ExpressionAttributeValues={':val': 'completado'}
)
print("Registro actualizado a status: completado")

# 4. Eliminar registro
table.delete_item(Key={'id': '001'})
print("Registro eliminado correctamente.")
