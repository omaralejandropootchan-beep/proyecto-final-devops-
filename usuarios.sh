#!/bin/bash
# Crear usuario de desarrollo
sudo useradd devops_user
sudo usermod -aG docker devops_user

# Restaurar permisos del entorno para ec2-user (Vital para Cloud9)
sudo chown -R ec2-user:ec2-user ~/environment
echo "Usuarios configurados y permisos restaurados."
