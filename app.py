from flask import Flask
import os

app = Flask(__name__)

# Read environment from system variable (BEST PRACTICE)
ENV = os.getenv("ENV", "UNKNOWN")

@app.route('/')
def home():
    return f"CI/CD Pipeline Working in {ENV} environment!"

@app.route('/health')
def health():
    return {
        "status": "UP",
        "environment": ENV
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
