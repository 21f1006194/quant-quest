def create_admin_if_not_exists():
    """Create an admin user if one does not already exist."""
    from app.models import User
    from app import db
    from flask import current_app

    # Get admin credentials from current app's configuration
    email = current_app.config["ADMIN_EMAIL"]
    username = current_app.config["ADMIN_USERNAME"]
    password = current_app.config["ADMIN_PASSWORD"]
    full_name = current_app.config["ADMIN_FULL_NAME"]

    # Check if an admin user already exists
    admin_user = User.query.filter_by(is_admin=True).first()
    if admin_user:
        return {"message": "Admin user already exists."}, 200

    # Create new admin user
    admin_user = User(
        email=email,
        username=username,
        full_name=full_name,
        is_admin=True,
    )
    admin_user.set_password(password)

    try:
        db.session.add(admin_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        import traceback

        traceback.print_exc()
        return {"error": "Error creating admin user"}, 500

    return {
        "message": "Admin user created successfully",
        "user": admin_user.to_dict(),
    }, 201


# ----------------- Password Strength Check -----------------
import re


def is_password_strong(password):
    """Check the strength of the password."""
    if (
        len(password) < 8
        or not re.search(r"[a-z]", password)
        or not re.search(r"[A-Z]", password)
        or not re.search(r"[0-9]", password)
        or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    ):
        return False
    return True


# ----------------- CSV Processing Helper -----------------
import csv
from io import StringIO
from typing import List, Dict


def process_whitelist_csv(csv_content: str) -> List[Dict]:
    """
    Process a CSV file containing whitelist user data.

    Args:
        csv_content (str): The content of the CSV file as a string

    Returns:
        List[Dict]: List of dictionaries containing user data

    Expected CSV format:
    - Required columns: Name, Email, Level
    - Optional column: Any column containing "physical" for physical presence
    - First row should be headers
    """
    try:
        # Create a CSV reader from the string content
        csv_file = StringIO(csv_content)
        reader = csv.DictReader(csv_file)

        # Validate required columns
        required_columns = {"Name", "email", "Level"}
        # strip all the column names
        reader.fieldnames = [col.strip() for col in reader.fieldnames]
        if not all(col in reader.fieldnames for col in required_columns):
            raise ValueError("CSV must contain Name, Email, and Level columns")

        # Find physical presence column if it exists
        physical_column = next(
            (col for col in reader.fieldnames if "physical" in col.lower()), None
        )

        # Process each row
        users = []
        for row in reader:
            user = {
                "name": row.get("Name", "").strip(),
                "email": row["email"].strip(),
                "level": row.get("Level", "").strip(),
                "physical_presence": False,  # Default value
            }

            # Set physical presence if column exists
            if physical_column:
                physical_value = row[physical_column].strip().lower()
                user["physical_presence"] = physical_value in ("yes", "true", "1", "y")

            # Validate required fields
            if not user["email"]:
                raise ValueError(f"Missing required fields in row: {row}")

            users.append(user)

        return users

    except Exception as e:
        from traceback import print_exc

        print_exc()
        raise ValueError(f"Error processing CSV file: {str(e)}")
