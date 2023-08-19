from app import app


def when_ready(server):
    app.app_context().push()


bind = "0.0.0.0:5000"
workers = 4
when_ready = when_ready
