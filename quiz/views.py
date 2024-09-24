from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Result
from django.shortcuts import render
from .forms import UserRegisterForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

def test_view(request):
    return render(request, 'test.html')

def homepage(request): 
    return render(request, 'homepage.html')

def home(request):
    if request.user.is_authenticated:
        # Staff quizzes visible to all users and user-created quizzes only visible to their creator
        quizzes = Quiz.objects.filter(
            Q(creator__is_staff=True) | Q(creator=request.user)
        )
    else:
        # If not authenticated, no quizzes are visible
        quizzes = Quiz.objects.none()

    return render(request, 'home.html', {'quizzes': quizzes})  

def profile(request):

    return render(request, 'profile.html')


def register(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
    
            return redirect('login')
        else:
            context = {'form': form}
            
            return render(request, 'signup.html', context)

    context = {'form': form}
    return render(request, 'register.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

@login_required
def create_quiz(request):
    if request.method == 'POST':
        title = request.POST['title']
        quiz = Quiz.objects.create(title=title, creator=request.user)
        return redirect('add_question', quiz_id=quiz.id)
    return render(request, 'create_quiz.html')

@login_required
def add_question(request, quiz_id):
    if request.method == 'POST':
        question_text = request.POST['question_text']
        option1 = request.POST['option1']
        option2 = request.POST['option2']
        answer = request.POST['answer']
        quiz = Quiz.objects.get(id=quiz_id)
        Question.objects.create(
            quiz=quiz,
            question_text=question_text,
            option1=option1,
            option2=option2,
            answer=answer
        )
        return redirect('add_question', quiz_id=quiz_id)
    return render(request, 'add_question.html', {'quiz_id': quiz_id})

# @login_required
# def take_quiz(request, quiz_id):
#     quiz = Quiz.objects.get(id=quiz_id)  # Fetch the quiz based on the ID
#     questions = quiz.questions.all()  # Retrieve all questions related to the quiz

#     if request.method == 'POST':
#         score = 0
#         for question in questions:
#             selected_answer = request.POST.get(str(question.id))
#             if selected_answer == question.answer:
#                 score += 1
#         Result.objects.create(quiz=quiz, user=request.user, score=score)  # Save the result
#         return redirect('quiz_results', quiz_id=quiz.id)  # Redirect to results page

#     return render(request, 'take_quizz.html', {'quiz': quiz, 'questions': questions})  # Render quiz

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Check if the quiz creator is a staff member or the current user
    if quiz.creator == request.user or quiz.creator.is_staff:
        questions = quiz.questions.all()

        if request.method == 'POST':
            score = 0
            for question in questions:
                selected_answer = request.POST.get(str(question.id))
                if selected_answer == question.answer:
                    score += 1
            Result.objects.create(quiz=quiz, user=request.user, score=score)
            return redirect('quiz_results', quiz_id=quiz.id)

        return render(request, 'take_quizz.html', {'quiz': quiz, 'questions': questions})
    else:
        # Optionally, you can return an error or a forbidden access message
        return redirect('home')


@login_required
def quiz_results(request, quiz_id):
    results = Result.objects.filter(quiz_id=quiz_id, user=request.user).first()
    return render(request, 'quizz_result.html', {'results': results})


def logout_user(request):
    logout(request)
    return redirect('login')

# def delete_quiz(request, quiz_id):
#     quiz = get_object_or_404(Quiz, id=quiz_id)
#     if request.method == 'POST':
#         quiz.delete() 
#         return redirect('home')  
#     return render(request, 'confirm_delete.html', {'quiz': quiz})@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Only allow the creator or staff to delete the quiz
    if request.user == quiz.creator or request.user.is_staff:
        if request.method == 'POST':
            quiz.delete()
            return redirect('home')
    else:
        return redirect('home')  # Redirect if they don't have permission

    return render(request, 'confirm_delete.html', {'quiz': quiz})


