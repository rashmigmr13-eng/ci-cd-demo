from flask import Flask
import os

app = Flask(__name__)

def get_env():
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                if line.startswith("ENV="):
                    return line.strip().split("=")[1]
    return "UNKNOWN"

ENV = get_env()

@app.route('/')
def home():
    return f"CI/CD Pipeline Working in {ENV} environment!"

@app.route('/health')
def health():
    return {
        "status": "UP",
        "env": ENV
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
