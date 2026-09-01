from flask import Flask, render_template, request

app = Flask(__name__)

list_students = []


class Student:
    def __init__(self, student_id, name, age, course, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks

    def calculate_grade(self):
        if float(self.marks) > 90:
            return "A+"
        elif float(self.marks) > 80:
            return "A"
        elif float(self.marks) > 70:
            return "B"
        elif float(self.marks) < 40:
            return "F"
        else:
            return "C"

    def get_details(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "marks": self.marks,
            "grade": self.calculate_grade()
        }

    def update_marks(self, marks):
        self.marks = marks


class StudentManager:

    def add_student(self, student):
        list_students.append(student)

    def find_student(self, student_id):
        for student in list_students:
            if student.student_id == student_id:
                return student

        return None

    def update_student(self, student_id, name=None, age=None,
                       course=None, marks=None):

        student = self.find_student(student_id)

        if student is None:
            return "Student not found"

        if name is not None:
            student.name = name

        if age is not None:
            student.age = age

        if course is not None:
            student.course = course

        if marks is not None:
            student.marks = marks

        return "Student updated successfully"

    def delete_student(self, student_id):
        student = self.find_student(student_id)

        if student is None:
            return "Student not found"

        list_students.remove(student)

        return "Student deleted successfully"

    def get_all_students(self):
        return [student.get_details() for student in list_students]

    def get_passed_students(self):
        return [
            student.get_details()
            for student in list_students
            if student.marks >= 40
        ]


manager = StudentManager()


@app.route("/students", methods=["POST"])
def add_student():

    data = request.json

    student = Student(
        data["student_id"],
        data["name"],
        data["age"],
        data["course"],
        data["marks"]
    )

    manager.add_student(student)

    return student.get_details()
@app.route("/students", methods=["GET"])
def get_students():
    return manager.get_all_students()
@app.route("/students/<id>", methods=["GET"])
def get_student(id):
    student=manager.find_student(id)
    if student is None:
        return {"message": "Student not found"}, 404
    return student.get_details()

if __name__ == "__main__":
    app.run(debug=True)