import boto3
from datetime import datetime, timedelta

# Inicialización de clientes
ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')
s3 = boto3.client('s3')
autoscaling = boto3.client('autoscaling')

def listar_ec2():
    print("\n=== 1. LISTADO DE INSTANCIAS EC2 ===")
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for inst in reservation['Instances']:
            print(f"ID: {inst['InstanceId']} | Tipo: {inst['InstanceType']} | Estado: {inst['State']['Name']}")

def reporte_cpu_24h():
    print("\n=== 2. REPORTE CPU ÚLTIMAS 24 HORAS ===")
    # Definir el rango de tiempo
    fin = datetime.utcnow()
    inicio = fin - timedelta(days=1)
    
    instancias = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    
    for res in instancias['Reservations']:
        for inst in res['Instances']:
            instance_id = inst['InstanceId']
            stats = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=inicio,
                EndTime=fin,
                Period=3600, # Granularidad de 1 hora
                Statistics=['Average']
            )
            
            if stats['Datapoints']:
                avg_cpu = stats['Datapoints'][0]['Average']
                print(f"Instancia {instance_id}: Promedio CPU: {avg_cpu:.2f}%")
            else:
                print(f"Instancia {instance_id}: Sin métricas suficientes.")

def listar_s3():
    print("\n=== 3. BUCKETS S3 Y OBJETOS ===")
    buckets = s3.list_buckets()
    for bucket in buckets['Buckets']:
        name = bucket['Name']
        print(f"Bucket: {name}")
        # Listar objetos dentro del bucket
        objs = s3.list_objects_v2(Bucket=name)
        if 'Contents' in objs:
            for obj in objs['Contents']:
                print(f"  - Objeto: {obj['Key']}")
        else:
            print("  - Bucket vacío")

def consultar_asg():
    print("\n=== 4. GRUPOS DE AUTO SCALING ===")
    asgs = autoscaling.describe_auto_scaling_groups()
    for asg in asgs['AutoScalingGroups']:
        print(f"Nombre: {asg['AutoScalingGroupName']}")
        print(f"  Capacidad -> Deseada: {asg['DesiredCapacity']} | Mín: {asg['MinSize']} | Máx: {asg['MaxSize']}")

if __name__ == "__main__":
    try:
        listar_ec2()
        reporte_cpu_24h()
        listar_s3()
        consultar_asg()
    except Exception as e:
        print(f"Error al ejecutar la automatización: {e}")