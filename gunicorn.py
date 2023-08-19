from importlib import import_module

app = import_module('app')

with app.app_context():
    app.run(host="0.0.0.0", port=5000)
