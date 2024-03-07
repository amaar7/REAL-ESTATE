from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from models import db, Property, User, Booking
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///real_estate.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)
db.init_app(app)
CORS(app)

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
    
@app.route("/user_signin", methods=["POST"])
def user_signin():
    try:
        data = request.get_json()
        required_fields = ["username", "password"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": True, "message": f"Missing or empty {field}"}), 400

        user = User.query.filter_by(username=data["username"]).first()

        if user and bcrypt.check_password_hash(user.password, data["password"]):
            return jsonify({"message": "User signed in successfully"}), 200
        else:
            return jsonify({"error": True, "message": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user_to_delete = User.query.get(user_id)
        if not user_to_delete:
            return jsonify({"error": True, "message": "User not found"}), 404

        db.session.delete(user_to_delete)
        db.session.commit()

        return jsonify({"id": user_to_delete.id, "message": "User deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

@app.route("/update_user/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return (
                jsonify({"error": True, "message": "Invalid JSON data in request"}),
                400,
            )

        user_to_update = User.query.get(user_id)
        if not user_to_update:
            return (
                jsonify({"error": True, "message": "User not found"}),
                404,
            )

        for key, value in data.items():
            if hasattr(user_to_update, key):
                setattr(user_to_update, key, value)

        db.session.commit()

        return (
            jsonify(
                {
                    "id": user_to_update.id,
                    "username": user_to_update.username,
                    "message": "User updated successfully",
                }
            ),
            200,
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
    
@app.route("/get_property_by_id/<int:property_id>", methods=["GET"])
def get_property_by_id(property_id):
    try:
        property_details = Property.query.get(property_id)
        if not property_details:
            return (
                jsonify({"error": True, "message": "Property not found"}),
                404,
            )

        property_info = {
            "title": property_details.title,
            "description": property_details.description,
            "price": property_details.price,
            "bedrooms": property_details.bedrooms,
            "bathrooms": property_details.bathrooms,
            "location": property_details.location,
            "image_link": property_details.image_link,
        }

        return jsonify({"property": property_info}), 200

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

@app.route("/get_all_properties", methods=["GET"])
def get_all_properties():
    try:
        properties = Property.query.all()
        property_list = [
            {
                "id": prop.id,
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
@app.route("/update_property/<int:property_id>", methods=["PATCH"])
def update_property(property_id):
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return (
                jsonify({"error": True, "message": "Invalid JSON data in request"}),
                400,
            )

        property_to_update = Property.query.get(property_id)
        if not property_to_update:
            return (
                jsonify({"error": True, "message": "Property not found"}),
                404,
            )

        for key, value in data.items():
            if hasattr(property_to_update, key):
                setattr(property_to_update, key, value)

        db.session.commit()

        return (
            jsonify(
                {
                    "id": property_to_update.id,
                    "title": property_to_update.title,
                    "message": "Property updated successfully",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500
    
@app.route("/delete_property/<int:property_id>", methods=["DELETE"])
def delete_property(property_id):
    try:
        property_to_delete = Property.query.get(property_id)
        if not property_to_delete:
            return (
                jsonify({"error": True, "message": "Property not found"}),
                404,
            )

        db.session.delete(property_to_delete)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": property_to_delete.id,
                    "message": "Property deleted successfully",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

@app.route("/create_booking", methods=["POST"])
def create_booking():
    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            return jsonify({"error": True, "message": "Invalid JSON data in request"}), 400

        required_fields = ["user_id", "property_id", "check_in_date", "check_out_date"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": True, "message": f"Missing or empty {field}"}), 400

        data["check_in_date"] = datetime.strptime(data["check_in_date"], "%dth %b %Y")
        data["check_out_date"] = datetime.strptime(data["check_out_date"], "%dth %b %Y")

        new_booking = Booking(
            user_id=data["user_id"],
            property_id=data["property_id"],
            check_in_date=data["check_in_date"],
            check_out_date=data["check_out_date"],
        )
        db.session.add(new_booking)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": new_booking.id,
                    "user_id": new_booking.user_id,
                    "property_id": new_booking.property_id,
                    "check_in_date": new_booking.check_in_date.strftime("%dth %b %Y"),
                    "check_out_date": new_booking.check_out_date.strftime("%dth %b %Y"),
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
        booking_list = []

        for booking in bookings:
            property_details = Property.query.get(booking.property_id)

            if property_details:
                booking_info = {
                    "user_id": booking.user_id,
                    "property_id": booking.property_id,
                    "check_in_date": str(booking.check_in_date),
                    "check_out_date": str(booking.check_out_date),
                    "property_image_link": property_details.image_link,
                }
                booking_list.append(booking_info)

        return jsonify({"bookings": booking_list}), 200

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500
        
@app.route("/booking/<int:booking_id>")
def get_booking(booking_id):
    try:
        booking_details = Booking.query.get(booking_id)
        if not booking_details:
            return (
                jsonify({"error": True, "message": "Booking not found"}),
                404,
            )

        booking_info = {
            "user_id": booking_details.user_id,
            "property_id": booking_details.property_id,
            "check_in_date": str(booking_details.check_in_date),
            "check_out_date": str(booking_details.check_out_date),
            "property_image_link": booking_details.property_image_link,
        }

        return jsonify({"booking": booking_info}), 200

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500

@app.route("/delete_booking/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    try:
        booking_to_delete = Booking.query.get(booking_id)
        if not booking_to_delete:
            return (
                jsonify({"error": True, "message": "Booking not found"}),
                404,
            )

        db.session.delete(booking_to_delete)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": booking_to_delete.id,
                    "message": "Booking deleted successfully",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": True, "message": f"An error occurred: {str(e)}"}), 500
    
if __name__ == "__main__":
    app.run(port=4000, debug=True)
