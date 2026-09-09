from flask import Flask, render_template, request, jsonify, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

app.secret_key = "nexacart-secret-key"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="nexacart"
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# CUSTOMER REGISTER
# =========================================================

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json(silent=True) or {}

    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    # Remove extra spaces
    if username:
        username = username.strip()

    if email:
        email = email.strip().lower()

    if phone:
        phone = phone.strip()

    # Check empty fields
    if not username or not email or not phone or not password:

        return jsonify({
            "success": False,
            "message": "Please fill all fields."
        }), 400

    try:

        # Connect database
        db = get_db_connection()
        cursor = db.cursor()

        # Check existing username or email
        check_query = """
            SELECT id
            FROM users
            WHERE username = %s OR email = %s
        """

        cursor.execute(
            check_query,
            (username, email)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.close()
            db.close()

            return jsonify({
                "success": False,
                "message": "Username or Email already exists."
            }), 409

        # Hash password
        password_hash = generate_password_hash(password)

        # Insert user
        insert_query = """
            INSERT INTO users
            (
                username,
                email,
                phone,
                password_hash
            )
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (
                username,
                email,
                phone,
                password_hash
            )
        )

        db.commit()

        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "message": "Registration successful!"
        })

    except mysql.connector.Error as error:

        print("MySQL Error:", error)

        return jsonify({
            "success": False,
            "message": "Database error occurred."
        }), 500


# =========================================================
# CUSTOMER LOGIN
# =========================================================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    # Remove extra spaces
    if username:
        username = username.strip()

    # Check empty fields
    if not username or not password:

        return jsonify({
            "success": False,
            "message": "Username and password are required."
        }), 400

    try:

        # Connect database
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Find user
        query = """
            SELECT *
            FROM users
            WHERE username = %s
        """

        cursor.execute(
            query,
            (username,)
        )

        user = cursor.fetchone()

        cursor.close()
        db.close()

        # User not found
        if user is None:

            return jsonify({
                "success": False,
                "message": "Invalid username or password."
            }), 401

        # Check password
        if check_password_hash(
            user["password_hash"],
            password
        ):

            # Save customer session
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return jsonify({
                "success": True,
                "message": "Login successful!",
                "username": user["username"]
            })

        # Wrong password
        return jsonify({
            "success": False,
            "message": "Invalid username or password."
        }), 401

    except mysql.connector.Error as error:

        print("MySQL Error:", error)

        return jsonify({
            "success": False,
            "message": "Database error occurred."
        }), 500


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)