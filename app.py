from flask import Flask
import os

app = Flask(__name__)

ENV = os.getenv("ENV", "UNKNOWN")

@app.route('/')
def home():
    return f"CI/CD Pipeline Working in {ENV} environment!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
