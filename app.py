from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        absences = int(request.form['absences'])
        prelim_exam = float(request.form['prelim_exam'])
        quizzes = float(request.form['quizzes'])
        requirements = float(request.form['requirements'])
        recitation = float(request.form['recitation'])

        attendance = calculate_attendance(absences)
        class_standing = calculate_class_standing(quizzes, requirements, recitation)
        prelim_grade = calculate_prelim_grade(prelim_exam, attendance, class_standing)

        if prelim_grade == "FAILED":
            result = "Student has failed due to absences."
        else:
            required_passing_grades = calculate_required_grades(prelim_grade, 75)
            required_deans_lister_grades = calculate_required_grades(prelim_grade, 90)
            result = f"Prelim Grade: {prelim_grade}<br>Required Midterm and Final Grades to pass with 75%: {required_passing_grades}<br>Required Midterm and Final Grades to achieve Dean's Lister status with 90%: {required_deans_lister_grades}"

        return render_template('result.html', result=result)
    return render_template('index.html')

def calculate_attendance(absences):
    if absences >= 4:
        return "FAILED"
    else:
        return 100 - (absences * 10)

def calculate_class_standing(quizzes, requirements, recitation):
    return (0.4 * quizzes) + (0.3 * requirements) + (0.3 * recitation)

def calculate_prelim_grade(prelim_exam, attendance, class_standing):
    if attendance == "FAILED":
        return "FAILED"
    else:
        return (0.6 * prelim_exam) + (0.1 * attendance) + (0.3 * class_standing)

def calculate_required_grades(prelim_grade, target_overall_grade):
    if prelim_grade == "FAILED":
        return "FAILED"
    else:
        required_midterm_grade = ((target_overall_grade - (0.2 * prelim_grade)) / 0.3) * 100
        required_finals_grade = ((target_overall_grade - (0.2 * prelim_grade) - (0.3 * required_midterm_grade)) / 0.5) * 100
        return required_midterm_grade, required_finals_grade

if __name__ == '__main__':
    app.run(debug=True)