from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User  # Import your custom User model


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('signin')

        if check_password(password, user.password_hash):
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['role'] = user.role
            request.session.modified = True

            messages.success(request, 'Logged in successfully')

            if user.role == 'admin':
                return redirect('admin_dashboard')  # URL name for admin dashboard
            else:
                return redirect('user_dashboard')  # URL name for user dashboard

        else:
            messages.error(request, 'Invalid email or password')
            return redirect('signin')

    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role', 'user')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')

        hashed_password = make_password(password)
        user = User(username=username, email=email, password_hash=hashed_password, role=role)
        user.save()

        messages.success(request, 'User registered successfully')
        return redirect('signin')

    return render(request, 'signup.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            # TODO: Implement password reset email logic here
            messages.success(request, f'Password reset instructions sent to {email}')
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email')

        return redirect('forgot_password')

    return render(request, 'forgot_password.html')


def logout_view(request):
    request.session.flush()  # Clears all session data
    messages.success(request, 'Logged out successfully')
    return redirect('signin')

from .decorators import login_required, admin_required, user_required
from .models import Problem, UserNote, UserProgress

# views.py
@login_required
@admin_required
def admin_dashboard(request):
    problems = Problem.objects.all()
    return render(request, 'admin_dashboard.html', {'problems': problems})

@login_required
@user_required
def user_dashboard(request):
    user_id = request.session['user_id']
    problems = Problem.objects.all()
    # Fetch user notes and progress for this user
    user_notes = UserNote.objects.filter(user_id=user_id)
    user_progress = UserProgress.objects.filter(user_id=user_id)
    # You can process and send data as needed for the UI
    return render(request, 'user_dashboard.html', {
        'problems': problems,
        'user_notes': user_notes,
        'user_progress': user_progress,
    })

@login_required
@admin_required
def add_problem(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        difficulty = request.POST.get('difficulty')
        name = request.POST.get('name')
        youtube_link = request.POST.get('youtube_link') or None
        practice_link = request.POST.get('practice_link') or None

        # Basic validation here if needed

        Problem.objects.create(
            topic=topic,
            difficulty=difficulty,
            name=name,
            youtube_link=youtube_link,
            practice_link=practice_link
        )
        messages.success(request, 'Problem added successfully.')
        return redirect('admin_dashboard')

    return render(request, 'add_problem.html')

from django.shortcuts import get_object_or_404

@admin_required
@login_required
def edit_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    if request.method == 'POST':
        problem.name = request.POST.get('name')
        problem.topic = request.POST.get('topic')
        problem.difficulty = request.POST.get('difficulty')
        problem.youtube_link = request.POST.get('youtube_link')
        problem.practice_link = request.POST.get('practice_link')
        problem.save()
        messages.success(request, 'Problem updated successfully.')
        return redirect('admin_dashboard')

    return render(request, 'edit_problem.html', {'problem': problem})


@admin_required
@login_required
def delete_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    problem.delete()
    messages.success(request, f'Problem "{problem.name}" deleted successfully.')
    return redirect('admin_dashboard')
