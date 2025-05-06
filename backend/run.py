from app import create_app, initialize_app
import os

app = create_app()

# Configure the database URI from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:supersecurepassword@localhost:5432/gamedb'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

initialize_app(app) 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
