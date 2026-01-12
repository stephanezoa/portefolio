# Getting Started with Flask: A Minimalist Guide

Flask is a lightweight WSGI web application framework in Python. It’s perfect for small to medium projects where you need **flexibility** and **control**.

## Why Flask?

- **Minimal core**: No ORM, no form validation — you choose your tools.
- **Easy to learn**: Ideal for beginners and experts alike.
- **Extensible**: Add only what you need via extensions.

## Quick Example

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Developer!"

if __name__ == '__main__':
    app.run(debug=True)