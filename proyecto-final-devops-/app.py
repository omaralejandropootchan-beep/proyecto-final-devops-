from flask import Flask
import os

app = Flask(__name__)

@app.get('/')
def home():
    return {
        "mensaje": "¡Hola desde Docker en AWS!",
        "usuario": "Omar Alejandro",
        "proyecto": "Final DevOps",
        "status": "Contenedor funcionando"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
