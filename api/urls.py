# edu_track/urls.py
from django.urls import path
from api.views import GradeCreateAPIView, RegisterView, StudentDetailAPIView, StudentGradeListAPIView, StudentListCreateAPIView, TeacherReportAPIView, login_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    
      # Étudiants
    path('students/', StudentListCreateAPIView.as_view(), name='student-list'),
    path('students/<int:id>/', StudentDetailAPIView.as_view(), name='student-detail'),

    # Notes
    path('grades/', GradeCreateAPIView.as_view(), name='grade-create'),
    path('grades/student/<int:id>/', StudentGradeListAPIView.as_view(), name='student-grade-list'),

    # Rapports
    path('teachers/reports/', TeacherReportAPIView.as_view(), name='teacher-reports'),
]
