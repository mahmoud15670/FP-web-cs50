from django.urls import path
from . import views
urlpatterns =[
    path('', views.index, name='index'),
    # path('login', views.login_view, name='login'),
    # path('logout', views.logout_view, name='logout'),
    # path('teacher/register', views.teacher_register, name='teacher_register'),
    # path('student/register', views.Student_register.as_view(), name='student_register'),
    # path('teacher/<int:pk>/detsil/entry', views.Teacher_detail_entry.as_view(), name='teacher_detail_entry'),
]
