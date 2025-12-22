from flask import Flask, request, jsonify, send_from_directory
import os
from jwt_service import verify_jwt
from db_service import init_db, add_course, get_course_by_filename, get_all_courses, get_courses_by_subject
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
COURSE_DIR = "../courses"
os.makedirs(COURSE_DIR, exist_ok=True)

init_db()

ALLOWED_UPLOAD_ROLES = ["ADMIN", "PROFESSOR"]


@app.route("/upload", methods=["POST"])
def upload_course():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split(" ")[1]
    payload = verify_jwt(token)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 403

    user_role = payload.get("role")
    if user_role not in ALLOWED_UPLOAD_ROLES:
        return jsonify({"error": "Forbidden: You do not have permission to upload"}), 403

    # Get subject from form data
    subject = request.form.get("subject")
    if not subject:
        return jsonify({"error": "Subject is required"}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    file_path = os.path.join(COURSE_DIR, file.filename)
    file.save(file_path)

    # Add to database
    user_id = payload.get("user_id") or payload.get("sub")
    course_id = add_course(user_id, file.filename, file_path, subject)

    return jsonify({
        "message": f"File '{file.filename}' uploaded successfully",
        "course_id": course_id,
        "subject": subject
    }), 201


@app.route("/download/<filename>", methods=["GET"])
def download_course(filename):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split(" ")[1]
    payload = verify_jwt(token)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 403

    file_path = os.path.join(COURSE_DIR, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(COURSE_DIR, filename, as_attachment=True)


@app.route("/courses", methods=["GET"])
def list_courses():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split(" ")[1]
    payload = verify_jwt(token)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 403

    subject = request.args.get("subject")

    if subject:
        courses = get_courses_by_subject(subject)
    else:
        courses = get_all_courses()

    return jsonify({"courses": courses}), 200


if __name__ == "__main__":
    app.run(port=5052)