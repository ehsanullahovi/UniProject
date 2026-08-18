from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/<str:role>/", views.login_view, name="login"),
    path("dashboard/", views.load_dashboard, name="dashboard"),
    path("register_user/<str:role>/", views.register_user, name="register_user"),
    path("students/", views.student_list, name="student_list"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/save/",views.save_students,name="save_students"),
    path("students/update/<int:id>/", views.update_student, name="update_student"),
    path("students/delete/<int:id>/", views.delete_student, name="delete_student"),
]