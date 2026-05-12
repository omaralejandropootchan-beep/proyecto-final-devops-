from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Proyecto DevOps - Omar Alejandro</h1><p>Aplicación Flask funcionando tras Nginx</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
