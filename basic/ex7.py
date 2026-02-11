student = {
    "name": "Carlos",
    "age": 22,
    "subjects": ["PNE", "Networks", "Databases"],
    "grades": {"PNE": 8.5, "Networks": 7.0, "Databases": 9.2}
}
total_grade = 0.0
grade_count = 0
for subject in student["grades"]:
    total_grade = total_grade + student["grades"][subject]
    grade_count = grade_count + 1

print(student["name"])
print(len(student["subjects"]))
print("PNE" in student["subjects"])
print(student["grades"]["Databases"])
print(round(total_grade/grade_count, 2))
print("Subject grades:")
for subject in student["grades"]:
    print(" ", subject + ":", student["grades"][subject])