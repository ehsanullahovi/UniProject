from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password, check_password

from .forms import StudentForm
from .models import Student, User


# Home page
def home(request):
    return render(request, 'core/home.html')


# Login page + login processing
def login_view(request, role):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        try:
            from django.contrib.auth import authenticate, login


            user = authenticate(
                username=username,
                password=password
                )

            if user:
                login(request, user)

            # Create session
                request.session["user_id"] = user.id
                request.session["username"] = user.username
                request.session["role"] = user.role

            return redirect("dashboard")

        except User.DoesNotExist:

            return render(request, 'core/login.html', {
                "role": role,
                "error": "Invalid username, password, or role"
            })


    return render(request, 'core/login.html', {
        "role": role
    })


# Dashboard loader
def load_dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role == "college_admin":
        return render(request, "core/college_admin_dashboard.html")

    elif request.user.role == "department_admin":

        return render(request, "core/department_admin_dashboard.html", {
            "department": request.user.department,
        })

    return redirect("home")


# Logout
def logout(request):
    request.session.flush()
    return redirect("home")

# Registering new user
def register_user(request, role):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'core/register_user.html', {
                "error": "Username already exists"
            })

        # Create a new user
        user = User(username=username, password=make_password(password), role=role)
        user.save()

        return render(request, 'core/register_user.html', {
                        "error": "User registered successfully"
                    })

    return render(request, 'core/register_user.html')

# Student list
def student_list(request):

    if request.user.role == "department_admin":

        students = Student.objects.filter(
            department=request.user.department
        )

    elif request.user.role == "college_admin":

        students = Student.objects.all()

    else:
        return redirect("home")

    return render(request, "core/manage_student.html", {
        "students": students
    })
    
# Student registration
def add_student(request):

    if request.user.role == "department_admin":

        department = request.user.department

    elif request.user.role == "college_admin":

        department = None

    else:
        return redirect("home")

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            admin_department=department
        )

        if form.is_valid():

            student = form.save(commit=False)

            if department:
                student.department = department

            student.save()

            return redirect("student_list")

    else:

        form = StudentForm(
            admin_department=department
        )

    return render(request, "core/add_student.html", {
        "form": form
    })
    
#Save students to database
def save_students(request):

    students = request.session.get("students", [])

    for student in students:

        Student.objects.create(
            student_name=student["student_name"],
            student_roll=student["student_roll"],
            department=student["department"],
            session=student["session"]
        )

    request.session["students"] = []

    return redirect("student_list")


# Student info update
def update_student(request, id):

    if request.user.role == "department_admin":

        student = get_object_or_404(
            Student,
            id=id,
            department=request.user.department
        )

    elif request.user.role == "college_admin":

        student = get_object_or_404(Student, id=id)

    else:
        return redirect("home")

    if request.method == "POST":

        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:

        form = StudentForm(instance=student)

    return render(request, "core/update_student.html", {
        "form": form,
        "student": student
    })
    
# Student deletion
def delete_student(request, id):

    if request.user.role == "department_admin":

        student = get_object_or_404(
            Student,
            id=id,
            department=request.user.department
        )

    elif request.user.role == "college_admin":

        student = get_object_or_404(Student, id=id)

    else:
        return redirect("home")

    if request.method == "POST":
        student.delete()

    return redirect("student_list")