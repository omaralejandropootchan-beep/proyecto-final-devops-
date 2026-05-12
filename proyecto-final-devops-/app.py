import json
import random

def lambda_handler(event, context):
    mensajes = [
        "Infraestructura desplegada con éxito",
        "Pipeline de CI/CD funcionando al 100%",
        "Dockerización completada por Omar",
        "Seguridad aplicada en Security Groups",
        "Monitoreo activo en CloudWatch"
    ]
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'mensaje': random.choice(mensajes),
            'servicio': 'microservicio-devops'
        })
    }
