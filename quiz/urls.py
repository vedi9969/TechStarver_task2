from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    path('test/', views.test_view, name='test'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.home, name='home'),
    path('', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/add_question/', views.add_question, name='add_question'),
    path('<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    path('<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),

]
