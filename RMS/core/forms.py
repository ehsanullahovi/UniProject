from django import forms
from .models import Student, User

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            "student_name",
            "student_roll",
            "department",
            "session",
        ]

    def __init__(self, *args, **kwargs):

        department = kwargs.pop("admin_department", None)

        super().__init__(*args, **kwargs)

        if department:
            self.fields["department"].choices = [
                (department, department)
            ]

class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
