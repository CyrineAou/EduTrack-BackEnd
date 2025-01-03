# edu_track/views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login
from api.models.grade import Grade
from api.serializers import GradeSerializer, RegisterSerializer, LoginSerializer, StudentGradeReportSerializer, UserSerializer
from api.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Avg
# Vue d'enregistrement de l'utilisateur
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# Vue de connexion de l'utilisateur
@csrf_exempt
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)  # Authentifier l'utilisateur
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GradeCreateAPIView(generics.CreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

# CRUD pour les étudiants
class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(role='student')
    serializer_class = UserSerializer

class StudentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role='student')
    serializer_class = UserSerializer

# Ajouter des notes
class GradeCreateAPIView(generics.CreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

# Liste des notes d'un étudiant
class StudentGradeListAPIView(generics.ListAPIView):
    serializer_class = GradeSerializer

    def get_queryset(self):
        student_id = self.kwargs['id']
        return Grade.objects.filter(student_id=student_id)

# Rapport pour enseignants
#class TeacherReportAPIView(generics.ListAPIView):
   # serializer_class = StudentGradeReportSerializer
    #def get_queryset(self):
        return CustomUser.objects.filter(role='student')

class TeacherReportAPIView(APIView):

    def get(self, request, *args, **kwargs):
        # Obtenir tous les étudiants
        students = CustomUser.objects.filter(role='student')

        # Préparer le rapport
        report = []
        for student in students:
            # Récupérer les notes de l'étudiant
            grades = Grade.objects.filter(student=student)

            # Calculer la moyenne des notes
            average_score = grades.aggregate(Avg('score'))['score__avg']

            # Ajouter les données de l'étudiant au rapport
            student_report = {
                "student_id": student.id,
                "student_name": f"{student.first_name} {student.last_name}",
                "email": student.email,
                "grades": [
                    {"subject": grade.subject, "score": grade.score, "date": grade.date}
                    for grade in grades
                ],
                "average_score": average_score,
            }
            report.append(student_report)

        return Response({"report": report}, status=status.HTTP_200_OK)