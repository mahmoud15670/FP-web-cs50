from django.urls import path
from . import views
urlpatterns =[
    path('', views.index, name='index'),
    path('stage/list', views.Stage_List.as_view(), name='stage_list'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('teacher/register', views.teacher_register, name='teacher_register'),
    path('student/register', views.student_register, name='student_register'),
    path('teacher/<int:pk>/detsil/entry', views.Teacher_detail_entry.as_view(), name='teacher_detail_entry'),
    path('group/create', views.Group_creation.as_view(), name='group_creation'),
    path('section/list', views.Section_list_view.as_view(), name='section_list'),
    path('section/details', views.Section_details_view.as_view(), name='dection_details')
]
