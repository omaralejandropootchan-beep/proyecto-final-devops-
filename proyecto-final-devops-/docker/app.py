from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "¡Hola Omar! Aplicacion Flask corriendo en Docker para el proyecto final."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# Trigger v2
