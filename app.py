from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__)

users = []
logs = []

@app.route("/")
def home():
    return "Secure File Sharing API is running!"

@app.route("/users")
def get_users():
    return jsonify(users)

@app.route("/test-register",methods=["GET"])
def test_register():

    users.append({
        "username": "neha",
        "email": "neha@mail.com",
        "password": "123456"
    })

    return jsonify({
        "message": "User registered successfully"
    })

@app.route("/login/<username>/<password>")
def login(username,password):
    for user in users:
        if (
            user["username"] == username and
            user["password"] == password
        ):    

            return jsonify({
                "message": "Login successful"
            })
    return jsonify({
        "message": "User not found"
    }), 401

@app.route("/upload")
def upload_file():
    filename = "sample.txt"

    with open(
        os.path.join("uploads", filename),
        "w"
    ) as file:
         file.write("Hello Neha")
         logs.append("Uploaded sample.txt")

    return jsonify({
        "message": "File uploaded successfully"
    })

@app.route("/files")
def list_files():
    if not os.path.exists("uploads"):
        return jsonify({
            "files": []
        })
    files = os.listdir("uploads")

    return jsonify({
        "files": files
    })
@app.route("/download/<filename>")
def download_file(filename):

    logs.append(f"Downloaded {filename}")

    return send_from_directory(
        "uploads",
        filename,
        as_attachment=True
    )

@app.route("/delete/<filename>")
def delete_file(filename):
    os.remove(os.path.join("uploads", filename))

    logs.append(f"Deleted {filename}")

    return jsonify({
        "message": "File deleted successfully"
    })

@app.route("/file-info/<filename>")
def file_info(filename):
    path = os.path.join("uploads", filename)

    if not os.path.exists(path):
        return jsonify({
            "error": "File not found"
        }), 404

    return jsonify({
        "filename": filename,
        "size_in_bytes":os.path.getsize(path)
    })

@app.route("/logs")
def view_logs():
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True)
