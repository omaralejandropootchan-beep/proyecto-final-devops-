#!/bin/bash
echo "--- Iniciando Punto 13: Microservicios ---"

# 1. Crear código de la función
echo "def lambda_handler(event, context): return {'statusCode': 200, 'body': 'Hola Omar, Lambda funcional'}" > lambda_function.py

# 2. Comprimir la función (Punto 13: zip)
zip function.zip lambda_function.py

# 3. Crear la función Lambda (Punto 13: lambda create-function)
# Usamos el LabRole que es el estándar de AWS Academy
ROLE_ARN=$(aws iam list-roles --query 'Roles[?RoleName==`LabRole`].Arn' --output text)

aws lambda create-function \
    --function-name "FuncionProyectoFinalOmar" \
    --runtime python3.9 \
    --handler lambda_function.lambda_handler \
    --role $ROLE_ARN \
    --zip-file fileb://function.zip

# 4. Crear el API Gateway (Punto 13: apigateway create-rest-api)
API_ID=$(aws apigateway create-rest-api --name 'API_Proyecto_Omar' --query 'id' --output text)
echo "Lambda y API Gateway creadas exitosamente. API ID: $API_ID"

echo "--- PUNTO 13 COMPLETADO ---"
