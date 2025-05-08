def create_admin_if_not_exists():
    """Create an admin user if one does not already exist."""
    from app.models import User
    from app import db

    # TODO: Get these from environment variables
    email = "admin@gmail.com"
    username = "admin"
    password = "admin"
    full_name = "Admin"

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
