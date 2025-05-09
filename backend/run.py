from app import create_app, initialize_app
import os

app = create_app()


initialize_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
