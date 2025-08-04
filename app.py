from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb+srv://sayantanisaha28022002:sayantanisaha28022002@cluster0.30czd2n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["HomeworkPractice"]
students = db["students"]

@app.route('/')
def home():
    return render_template("student.html", page='home')

@app.route('/form')
def form_page():
    return render_template("student.html", page='form')

@app.route('/view')
def view_students():
    all_students = list(students.find())
    for s in all_students:
        s['_id'] = str(s['_id'])
    return render_template("student.html", page='view', students=all_students)

@app.route("/create", methods=["POST"])
def create_student():
    form = request.form
    data = {
        "name": form.get("name"),
        "address": form.get("address"),
        "email": form.get("email"),
        "subjects": {
            "name": form.get("subject_name"),
            "author": form.get("subject_author"),
            "description": form.get("subject_description")
        }
    }
    students.insert_one(data)
    return redirect(url_for('view_students'))

@app.route('/delete/<id>')
def delete_student(id):
    students.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('view_students'))

@app.route('/edit/<id>')
def edit_page(id):
    student = students.find_one({"_id": ObjectId(id)})
    student['_id'] = str(student['_id'])
    return render_template("student.html", page='edit', student=student)

@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    form = request.form
    updated_data = {
        "name": form.get("name"),
        "address": form.get("address"),
        "email": form.get("email"),
        "subjects": {
            "name": form.get("subject_name"),
            "author": form.get("subject_author"),
            "description": form.get("subject_description")
        }
    }
    students.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
    return redirect(url_for('view_students'))

if __name__ == "__main__":
    app.run(debug=True)