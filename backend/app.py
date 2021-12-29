from flask import Flask

app = Flask(__name__)

@app.route("/<user>/orders")
def index(user):
    return f"""
        <h3>{user}
        <h5>0 Orders</h5>
    """