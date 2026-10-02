from flask import Flask, request

app = Flask(__name__)

@app.get('/')
def root():
    return "hello world"