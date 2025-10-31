from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from adminapp.models import Student, Course, Result


def student_login(request):
    """
    Handles student login using matric number and password.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Try to find the student by matric number
            student = Student.objects.get(matric_number=username)

            # Verify password
            if check_password(password, student.password):
                # Save session data
                request.session['student_id'] = student.id
                request.session['student_name'] = f"{student.first_name} {student.last_name}"
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid password.')
        except Student.DoesNotExist:
            messages.error(request, 'Invalid matric number or password.')

    return render(request, 'studentapp/login.html')


def dashboard(request):
    """
    Displays student dashboard with basic academic stats.
    """
    student_id = request.session.get('student_id')
    student_name = request.session.get('student_name', 'Student')

    if not student_id:
        return redirect('student_login')

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        messages.error(request, "Student record not found.")
        return redirect('student_login')

    # Fetch data for dashboard
    total_courses = Course.objects.filter(department=student.department).count()
    uploaded_results = Result.objects.filter(student=student).count()

    # Calculate average grade if results exist
    average_grade = "N/A"
    if uploaded_results > 0:
        total_score = sum(result.score for result in Result.objects.filter(student=student))
        average_score = total_score / uploaded_results

        # Convert average score to grade
        if average_score >= 70:
            average_grade = "A"
        elif average_score >= 60:
            average_grade = "B"
        elif average_score >= 50:
            average_grade = "C"
        elif average_score >= 45:
            average_grade = "D"
        else:
            average_grade = "F"

    context = {
        'student_name': student_name,
        'total_courses': total_courses,
        'uploaded_results': uploaded_results,
        'average_grade': average_grade,
        'status': student.status,
    }

    return render(request, 'studentapp/dashboard.html', context)


def logout_view(request):
    """
    Logs out the student by clearing the session.
    """
    request.session.flush()
    return redirect('student_login')
