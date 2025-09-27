from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ---------- MODELS ----------
class Student(BaseModel):
    name: str
    roll_no: int
    class_name: str

class Result(BaseModel):
    subject: str
    marks: int

# ----------  DATA ----------
students = {
    1: {"name": "Ali", "roll_no": 101, "class_name": "10th"},
    2: {"name": "Sara", "roll_no": 102, "class_name": "10th"},
    3: {"name": "Ahmed", "roll_no": 103, "class_name": "9th"},
    4: {"name": "Furqan", "roll_no": 103, "class_name": "9th"},
    5: {"name": "Daniyal", "roll_no": 103, "class_name": "9th"},
    6: {"name": "Hamza", "roll_no": 103, "class_name": "9th"},
    7: {"name": "Maaz", "roll_no": 103, "class_name": "9th"},
    8: {"name": "Ibrahim", "roll_no": 103, "class_name": "9th"},
    9: {"name": "Saad", "roll_no": 103, "class_name": "9th"},
    10: {"name": "Muzammil", "roll_no": 103, "class_name": "9th"}
}

results = {
    1: [
        {"subject": "Math", "marks": 85},
        {"subject": "Science", "marks": 78},
    ],
    2: [
        {"subject": "Math", "marks": 65},
        {"subject": "Science", "marks": 55},
    ],
    3: [
        {"subject": "Math", "marks": 90},
        {"subject": "Science", "marks": 88},
    ],
    4: [
        {"subject": "Math", "marks": 88},
        {"subject": "Science", "marks": 65},
    ],
    5: [
        {"subject": "Math", "marks": 95},
        {"subject": "Science", "marks": 84},
    ],
    6: [
        {"subject": "Math", "marks": 78},
        {"subject": "Science", "marks": 80},
    ],
    7: [
        {"subject": "Math", "marks": 91},
        {"subject": "Science", "marks": 82},
    ],
    8: [
        {"subject": "Math", "marks": 72},
        {"subject": "Science", "marks": 59},
    ],
    9: [
        {"subject": "Math", "marks": 76},
        {"subject": "Science", "marks": 85},
    ],
    10: [
        {"subject": "Math", "marks": 67},
        {"subject": "Science", "marks": 98},
    ]
}

# ---------- ENDPOINTS ----------

@app.get("/")
def home():
    return {"message": "Welcome to School Management API!"}

@app.get("/students")
def get_all_students():
    return students

@app.get("/students/{roll_no}")
def get_student(roll_no: int):
    student = students.get(roll_no)
    if not student:
        return {"message": "Student not found"}
    return student

@app.post("/students")
def add_student(student: Student):
    if student.roll_no in students:
        return {"message": "Student with this roll number already exists"}
    students[student.roll_no] = student.dict()
    results[student.roll_no] = []
    return {"message": "Student added", "students": students}

@app.delete("/students/{roll_no}")
def delete_student(roll_no: int):
    if roll_no not in students:
        return {"message": "Student not found"}
    del students[roll_no]
    results.pop(roll_no, None)
    return {"message": "Student deleted", "students": students}

@app.get("/results/{roll_no}")
def get_results(roll_no: int):
    if roll_no not in students:
        return {"message": "Student not found"}
    student_results = results.get(roll_no, [])
    if not student_results:
        return {"message": "No results found"}
    
    total = sum(r["marks"] for r in student_results)
    percentage = total / (len(student_results) * 100) * 100
    grade = "A+" if percentage >= 80 else "A" if percentage >= 70 else "B" if percentage >=60 else "C" if percentage >=50 else "Fail"
    return {
        "student": students[roll_no],
        "results": student_results,
        "total_marks": total,
        "percentage": round(percentage, 2),
        "grade": grade
    }

@app.post("/results/{roll_no}")
def add_result(roll_no: int, result: Result):
    if roll_no not in students:
        return {"message": "Student not found"}
    results[roll_no].append(result.dict())
    return {"message": "Result added", "results": results[roll_no]}