from app import create_app, initialize_app
import os

app = create_app()

# Connect to the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:supersecurepassword@db:5432/gamedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


initialize_app(app) 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
