from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Problem, UserNote, UserProgress  # Import your models
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.db.models import Count
from .decorators import login_required, admin_required, user_required


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
    problems = Problem.objects.all().order_by('topic', 'difficulty')
    
    # Group problems by topic and difficulty
    grouped_problems = {}
    topics = set()
    difficulties = set()
    
    for problem in problems:
        topic = problem.topic
        difficulty = problem.difficulty
        topics.add(topic)
        difficulties.add(difficulty)
        
        if topic not in grouped_problems:
            grouped_problems[topic] = {
                'difficulties': {},
                'total': 0
            }
        
        if difficulty not in grouped_problems[topic]['difficulties']:
            grouped_problems[topic]['difficulties'][difficulty] = []
        
        grouped_problems[topic]['difficulties'][difficulty].append(problem)
        grouped_problems[topic]['total'] += 1
    
    context = {
        'grouped_problems': grouped_problems,
        'topics': sorted(list(topics)),
        'difficulties': sorted(list(difficulties)),
        'all_problems': problems  # For search functionality
    }
    
    return render(request, 'admin_dashboard.html', context)

@login_required
@user_required
def user_dashboard(request):
    user_id = request.session['user_id']
    problems = Problem.objects.all().order_by('topic', 'difficulty')
    user_notes = UserNote.objects.filter(user_id=user_id)
    user_progress = UserProgress.objects.filter(user_id=user_id)
    
    # Create dictionaries for quick lookups
    notes_dict = {note.problem_id: note.note for note in user_notes}
    progress_dict = {prog.problem_id: prog.is_completed for prog in user_progress}
    
    # Calculate statistics
    total_problems = problems.count()
    completed_problems = user_progress.filter(is_completed=True).count()
    remaining_problems = total_problems - completed_problems
    completion_rate = (completed_problems / total_problems * 100) if total_problems > 0 else 0
    
    # Group problems by topic and difficulty
    grouped_problems = {}
    for problem in problems:
        topic = problem.topic
        difficulty = problem.difficulty
        
        if topic not in grouped_problems:
            grouped_problems[topic] = {
                'difficulties': {},
                'total': 0
            }
        
        if difficulty not in grouped_problems[topic]['difficulties']:
            grouped_problems[topic]['difficulties'][difficulty] = []
            
        problem_data = {
            'id': problem.id,
            'name': problem.name,
            'difficulty': problem.difficulty,
            'youtube_link': problem.youtube_link,
            'practice_link': problem.practice_link,
            'is_solved': progress_dict.get(problem.id, False),
            'note': notes_dict.get(problem.id, '')
        }
        grouped_problems[topic]['difficulties'][difficulty].append(problem_data)
        grouped_problems[topic]['total'] += 1
    
    return render(request, 'user_dashboard.html', {
        'grouped_problems': grouped_problems,
        'total_problems': total_problems,
        'solved_problems': completed_problems,
        'completion_rate': completion_rate
    })

@login_required
@admin_required
def add_problem(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            topic = data.get('topic')
            difficulty = data.get('difficulty')
            name = data.get('name')
            youtube_link = data.get('youtube_link') or None
            practice_link = data.get('practice_link') or None

            if not all([topic, difficulty, name]):
                return JsonResponse({
                    'success': False,
                    'error': 'Please fill in all required fields.'
                })

            Problem.objects.create(
                topic=topic,
                difficulty=difficulty,
                name=name,
                youtube_link=youtube_link,
                practice_link=practice_link
            )
            
            return JsonResponse({'success': True})
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid request format.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({
        'success': False,
        'error': 'Invalid request method.'
    })

from django.shortcuts import get_object_or_404

@login_required
@admin_required
def edit_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    
    if request.method == 'POST':
        topic = request.POST.get('topic')
        difficulty = request.POST.get('difficulty')
        name = request.POST.get('name')
        youtube_link = request.POST.get('youtube_link') or None
        practice_link = request.POST.get('practice_link') or None

        if not all([topic, difficulty, name]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('edit_problem', problem_id=problem_id)

        try:
            problem.topic = topic
            problem.difficulty = difficulty
            problem.name = name
            problem.youtube_link = youtube_link
            problem.practice_link = practice_link
            problem.save()
            
            messages.success(request, 'Problem updated successfully.')
            return redirect('admin_dashboard')
        except Exception as e:
            messages.error(request, f'Error updating problem: {str(e)}')
            return redirect('edit_problem', problem_id=problem_id)

    return render(request, 'edit_problem.html', {'problem': problem})

@login_required
@admin_required
def delete_problem(request, problem_id):
    if request.method == 'POST':
        try:
            problem = Problem.objects.get(id=problem_id)
            # The related UserNote and UserProgress records will be automatically deleted
            # due to the CASCADE setting on the foreign key relationships
            problem.delete()
            return JsonResponse({'success': True})
        except Problem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Problem not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@user_required
@require_http_methods(["POST"])
def save_note(request, problem_id):
    try:
        data = json.loads(request.body)
        note_text = data.get('note')
        user_id = request.session['user_id']
        
        note, created = UserNote.objects.update_or_create(
            user_id=user_id,
            problem_id=problem_id,
            defaults={'note': note_text}
        )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@user_required
@require_http_methods(["POST"])
def toggle_progress(request, problem_id):
    try:
        data = json.loads(request.body)
        completed = data.get('completed', False)
        user_id = request.session['user_id']
        
        progress, created = UserProgress.objects.update_or_create(
            user_id=user_id,
            problem_id=problem_id,
            defaults={'is_completed': completed}
        )
        
        # Get updated statistics
        total_problems = Problem.objects.count()
        solved_problems = UserProgress.objects.filter(
            user_id=user_id,
            is_completed=True
        ).count()
        completion_rate = (solved_problems / total_problems * 100) if total_problems > 0 else 0
        
        return JsonResponse({
            'success': True,
            'data': {
                'total_problems': total_problems,
                'solved_problems': solved_problems,
                'completion_rate': round(completion_rate, 1)
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@user_required
def get_user_statistics(request):
    user_id = request.session['user_id']
    
    # Get total problems and completed problems
    total_problems = Problem.objects.count()
    completed_problems = UserProgress.objects.filter(
        user_id=user_id,
        is_completed=True
    ).count()
    
    # Get progress by topic
    topic_progress = Problem.objects.values('topic').annotate(
        total=Count('id'),
        completed=Count('userprogress',
            filter=models.Q(userprogress__user_id=user_id, userprogress__is_completed=True)
        )
    )
    
    # Get progress by difficulty
    difficulty_progress = Problem.objects.values('difficulty').annotate(
        total=Count('id'),
        completed=Count('userprogress',
            filter=models.Q(userprogress__user_id=user_id, userprogress__is_completed=True)
        )
    )
    
    return JsonResponse({
        'success': True,
        'data': {
            'total_problems': total_problems,
            'completed_problems': completed_problems,
            'completion_rate': (completed_problems / total_problems * 100) if total_problems > 0 else 0,
            'topic_progress': list(topic_progress),
            'difficulty_progress': list(difficulty_progress)
        }
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = User.objects.get(id=request.session['user_id'])

        if not check_password(current_password, user.password_hash):
            messages.error(request, 'Current password is incorrect')
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match')
            return redirect('change_password')

        user.password_hash = make_password(new_password)
        user.save()
        messages.success(request, 'Password changed successfully')
        return redirect('user_dashboard' if user.role == 'user' else 'admin_dashboard')

    return render(request, 'change_password.html')

@login_required
def problems(request):
    problems = Problem.objects.all()
    user_id = request.session['user_id']
    
    problems_data = []
    for problem in problems:
        progress = UserProgress.objects.filter(user_id=user_id, problem=problem).first()
        note = UserNote.objects.filter(user_id=user_id, problem=problem).first()
        problems_data.append({
            'problem': problem,
            'progress': progress,
            'note': note
        })
    
    topics = Problem.objects.values_list('topic', flat=True).distinct()
    
    context = {
        'problems_data': problems_data,
        'topics': topics
    }
    return render(request, 'problems.html', context)

@login_required
def progress(request):
    user_id = request.session['user_id']
    total_problems = Problem.objects.count()
    completed_problems = UserProgress.objects.filter(user_id=user_id, is_completed=True).count()
    
    # Calculate progress by topic
    topics = Problem.objects.values_list('topic', flat=True).distinct()
    topic_progress = []
    
    for topic in topics:
        topic_total = Problem.objects.filter(topic=topic).count()
        topic_completed = UserProgress.objects.filter(
            user_id=user_id,
            is_completed=True,
            problem__topic=topic
        ).count()
        
        topic_progress.append({
            'topic': topic,
            'completed': topic_completed,
            'total': topic_total,
            'percentage': (topic_completed / topic_total * 100) if topic_total > 0 else 0
        })
    
    context = {
        'total_problems': total_problems,
        'completed_problems': completed_problems,
        'completion_rate': (completed_problems / total_problems * 100) if total_problems > 0 else 0,
        'topic_progress': topic_progress
    }
    return render(request, 'progress.html', context)

@login_required
@admin_required
def update_problems(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            problems = data.get('problems', [])
            
            if not problems:
                return JsonResponse({
                    'success': False,
                    'error': 'No problems provided for update'
                })
            
            for problem_data in problems:
                problem_id = problem_data.pop('id', None)
                if not problem_id:
                    return JsonResponse({
                        'success': False,
                        'error': 'Problem ID is missing'
                    })
                
                try:
                    problem = Problem.objects.get(id=problem_id)
                    for field, value in problem_data.items():
                        setattr(problem, field, value)
                    problem.save()
                except Problem.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': f'Problem with ID {problem_id} not found'
                    })
                except Exception as e:
                    return JsonResponse({
                        'success': False,
                        'error': f'Error updating problem {problem_id}: {str(e)}'
                    })
            
            return JsonResponse({'success': True})
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Server error: {str(e)}'
            })
            
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

@login_required
@admin_required
def user_progress(request, user_id):
    user = get_object_or_404(User, id=user_id)
    progress_data = UserProgress.objects.filter(user=user, is_completed=True)
    notes_data = UserNote.objects.filter(user=user)
    
    total_problems = Problem.objects.count()
    completed_problems = progress_data.count()
    
    context = {
        'user': user,
        'total_problems': total_problems,
        'completed_problems': completed_problems,
        'completion_rate': (completed_problems / total_problems * 100) if total_problems > 0 else 0,
        'progress_data': progress_data,
        'notes_data': notes_data
    }
    
    return JsonResponse({
        'success': True,
        'html': render(request, 'user_progress_modal.html', context).content.decode('utf-8')
    })

@login_required
@admin_required
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            if user.role == 'admin':
                return JsonResponse({'success': False, 'error': 'Cannot delete admin users'})
            user.delete()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@admin_required
def admin_users(request):
    users = User.objects.filter(role='user')
    user_data = []
    
    for user in users:
        # Calculate progress for each user
        total_problems = Problem.objects.count()
        completed_problems = UserProgress.objects.filter(
            user=user,
            is_completed=True
        ).count()
        
        progress = (completed_problems / total_problems * 100) if total_problems > 0 else 0
        
        user_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'progress': round(progress, 1),
            'last_login': None  # You can add last_login tracking if needed
        })
    
    return render(request, 'admin_users.html', {'users': user_data})

@login_required
@user_required
def user_progress_view(request):
    user_id = request.session['user_id']
    problems = Problem.objects.all()
    user_progress = UserProgress.objects.filter(user_id=user_id)
    
    # Calculate statistics
    total_problems = problems.count()
    completed_problems = user_progress.filter(is_completed=True).count()
    remaining_problems = total_problems - completed_problems
    completion_rate = (completed_problems / total_problems * 100) if total_problems > 0 else 0
    
    # Calculate topic-wise progress
    topic_progress = {}
    for problem in problems:
        if problem.topic not in topic_progress:
            topic_progress[problem.topic] = {
                'total': 0,
                'completed': 0
            }
        topic_progress[problem.topic]['total'] += 1
        if user_progress.filter(problem=problem, is_completed=True).exists():
            topic_progress[problem.topic]['completed'] += 1
    
    return render(request, 'user_progress.html', {
        'completed_problems': completed_problems,
        'remaining_problems': remaining_problems,
        'completion_rate': completion_rate,
        'topic_progress': topic_progress
    })
