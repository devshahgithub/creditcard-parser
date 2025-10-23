from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Flask is working!"

if __name__ == '__main__':
    print("Starting test app...")
    app.run(debug=True)
