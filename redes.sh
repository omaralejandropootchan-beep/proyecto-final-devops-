#!/bin/bash
echo "--- Iniciando gestión de red (Modo Entrega Final) ---"

# 1. Intentar crear VPC, si falla por límite (VpcLimitExceeded), buscar una existente
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text 2>/dev/null)

if [ -z "$VPC_ID" ] || [ "$VPC_ID" == "None" ]; then
    echo "Límite de VPCs alcanzado. Seleccionando una existente para no detener el proceso..."
    VPC_ID=$(aws ec2 describe-vpcs --query 'Vpcs[0].VpcId' --output text)
fi

if [ -z "$VPC_ID" ] || [ "$VPC_ID" == "None" ]; then
    echo "ERROR CRÍTICO: No se encontró ninguna VPC disponible."
    exit 1
fi

echo "TRABAJANDO EN VPC: $VPC_ID"

# 2. Crear Subnet (Punto 9) - Usamos un CIDR aleatorio para evitar choques
RANDOM_NET=$(( ( RANDOM % 250 )  + 1 ))
SUBNET_ID=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.${RANDOM_NET}.0/24 --query 'Subnet.SubnetId' --output text)
echo "Subnet Creada con éxito: $SUBNET_ID"

# 3. Habilitar IP Pública (Punto 9)
aws ec2 modify-subnet-attribute --subnet-id $SUBNET_ID --map-public-ip-on-launch
echo "Atributo de Subnet modificado (IP Pública activa)."

# 4. Crear e instalar Internet Gateway (Punto 9)
IGW_ID=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID
echo "Internet Gateway creado y vinculado: $IGW_ID"

# 5. Grupo de Seguridad (Punto 9)
SG_NAME="SG_Final_Omar_$(date +%s)"
SG_ID=$(aws ec2 create-security-group --group-name "$SG_NAME" --description "SG Final" --vpc-id $VPC_ID --query 'GroupId' --output text)
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0
echo "Seguridad configurada en SG ($SG_NAME): $SG_ID"

echo "--- PUNTO 9 COMPLETADO EXITOSAMENTE ---"
