from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

def auth_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            # Try to get user by email
            try:
                username = User.objects.get(email=email).username
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('face_analyzer:home')
                else:
                    messages.error(request, 'Invalid credentials')
            except User.DoesNotExist:
                messages.error(request, 'User not found')
            
        elif action == 'signup':
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return redirect('face_analyzer:auth')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('face_analyzer:auth')
            
            # Create new user
            try:
                username = email.split('@')[0]  # Use part before @ as username
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=full_name.split()[0],
                    last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
                )
                login(request, user)
                return redirect('face_analyzer:home')
            except Exception as e:
                messages.error(request, str(e))
    
    return render(request, 'face_analyzer/auth.html')

def logout_view(request):
    logout(request)
    return redirect('face_analyzer:auth')
