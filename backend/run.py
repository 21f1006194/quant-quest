from app import create_app, initialize_app

app = create_app()
initialize_app(app)  # Call this after migrations are complete

if __name__ == "__main__":
    app.run(debug=True)
