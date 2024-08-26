from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('group/<int:pk>/details', views.Group_detail_view.as_view(), name='group_details'),
    path('group/<int:pk>/enroll', views.student_enroll, name='student_enroll'),
    path('section/list', views.Section_list_view.as_view(), name='section_list'),
    path('course/create', views.Course_create_view.as_view(), name='course_create'),
    path('course/<int:pk>/detail', views.Course_detail_view.as_view(), name='course_detail'),
    path('course/<int:course_id>/unit/create', views.unit_create, name='unit_create'),
    path('section/<int:pk>/details', views.Section_details_view.as_view(), name='section_details')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
