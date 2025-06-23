from django.shortcuts import redirect

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('signin')  # redirect if not logged in
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('role') not in ['admin', 'superadmin']:
            return redirect('signin') 
        return view_func(request, *args, **kwargs)
    return wrapper

def user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('role') != 'user':
            return redirect('signin')
        return view_func(request, *args, **kwargs)
    return wrapper
