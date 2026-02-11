students = [
    {"name": "Ana", "grades": [8.5, 7.0, 9.0]},
    {"name": "Luis", "grades": [5.0, 4.5, 6.0]},
    {"name": "Maria", "grades": [9.5, 9.0, 10.0]},
    {"name": "Pedro", "grades": [3.0, 4.0, 2.5]},
    {"name": "Sofia", "grades": [7.0, 7.5, 8.0]},
]

def aver(lst):
    c = 0
    t = 0
    for ch in lst:
        t = t + ch
        c = c + 1
    return round(t/c, 1)

def get_status(avg):
    if avg >= 5.0:
        return "PASS"
    else:
        return "FAIL"

pass_count = 0
fail_count = 0
for student in students:
    name = student["name"]
    grades = student["grades"]
    avg = aver(grades)
    status = get_status(avg)
    print(name + ": " + str(avg) + " -> " + status)
    if status == "PASS":
        pass_count = pass_count + 1
    else:
        fail_count = fail_count + 1

print("The amount of students that pass is:", pass_count)
print("The amount of students that fail is:", fail_count)




