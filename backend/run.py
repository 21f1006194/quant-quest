from app import create_app, initialize_app
import os

app = create_app()


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        initialize_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
