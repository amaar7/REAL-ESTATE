from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from models import db, Property, User, Booking

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///real_estate.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def home():
    data = {"Server side": "Real Estate"}
    return jsonify(data), 200

@app.route("/user_signup", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return (
                jsonify({"error": True, "message": "Invalid JSON data in request"}),
                400,
            )

        required_fields = ["username", "email", "password"]
        for field in required_fields:
            if field not in data or not data[field]:
                return (
                    jsonify({"error": True, "message": f"Missing or empty {field}"}),
                    400,
                )

        hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        new_user = User(
            username=data["username"],
            email=data["email"],
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": new_user.id,
                    "username": new_user.username,
                    "message": "User added successfully",
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

@app.route("/get_all_users", methods=["GET"])
def get_all_users():
    try:
        users = User.query.all()
        user_list = [{"username": user.username, "email": user.email} for user in users]

        return jsonify({"users": user_list}), 200

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500


@app.route("/create_property", methods=["POST"])
def create_property():
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return (
                jsonify({"error": True, "message": "Invalid JSON data in request"}),
                400,
            )

        required_fields = ["title", "description", "price", "bedrooms", "bathrooms", "location", "image_link"]
        for field in required_fields:
            if field not in data or not data[field]:
                return (
                    jsonify({"error": True, "message": f"Missing or empty {field}"}),
                    400,
                )

        new_property = Property(
            title=data["title"],
            description=data["description"],
            price=data["price"],
            bedrooms=data["bedrooms"],
            bathrooms=data["bathrooms"],
            location=data["location"],
            image_link=data["image_link"],
        )
        db.session.add(new_property)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": new_property.id,
                    "title": new_property.title,
                    "message": "Property created successfully",
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

@app.route("/get_all_properties", methods=["GET"])
def get_all_properties():
    try:
        properties = Property.query.all()
        property_list = [
            {
                "title": prop.title,
                "price": prop.price,
                "location": prop.location,
                "image_link": prop.image_link,  
            }
            for prop in properties
        ]

        return jsonify({"properties": property_list}), 200

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500
    
@app.route("/create_booking", methods=["POST"])
def create_booking():
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return (
                jsonify({"error": True, "message": "Invalid JSON data in request"}),
                400,
            )

        required_fields = ["user_id", "property_id", "check_in_date", "check_out_date", "property_image_link"]
        for field in required_fields:
            if field not in data or not data[field]:
                return (
                    jsonify({"error": True, "message": f"Missing or empty {field}"}),
                    400,
                )

        new_booking = Booking(
            user_id=data["user_id"],
            property_id=data["property_id"],
            check_in_date=data["check_in_date"],
            check_out_date=data["check_out_date"],
            property_image_link=data["property_image_link"], 
        )
        db.session.add(new_booking)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": new_booking.id,
                    "user_id": new_booking.user_id,
                    "property_id": new_booking.property_id,
                    "message": "Booking created successfully",
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

@app.route("/get_all_bookings", methods=["GET"])
def get_all_bookings():
    try:
        bookings = Booking.query.all()
        booking_list = [
            {
                "user_id": booking.user_id,
                "property_id": booking.property_id,
                "check_in_date": str(booking.check_in_date),
                "check_out_date": str(booking.check_out_date),
                "property_image_link": booking.property_image_link,  # Add this line
            }
            for booking in bookings
        ]

        return jsonify({"bookings": booking_list}), 200

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=4000, debug=True)
