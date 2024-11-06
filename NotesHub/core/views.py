from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .utils import *
import os

def index(request):
    return render(request, 'home.html')

def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data.get('last_name', ''),
                email=form.cleaned_data['email']
            )
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            print(user)
            messages.success(request, "Registration successful.")
            return redirect('login')  # Replace 'login' with the name of your login view
        
        else:
            messages.error(request, "Please correct the errors below.")
    
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect('index')  
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please fill out all fields.")
    
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logoutView(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

@login_required(login_url='login')
def createNoteView(request):
    form = CreateNoteForm()

    if request.method == 'POST':
        form = CreateNoteForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['file']
            filepath = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(filepath, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)


            # TODO: put inside try catch block
            download_url, thumbnail_url, preview_url = uploadToDrive(filepath, file.name)
            print(download_url, thumbnail_url, preview_url)
            if not download_url:
                messages.error(request, "File upload to google drive failed.")
                return redirect('create-note')
            
            courseCode = form.cleaned_data['course_code']
            course = Course.objects.get(course_code=courseCode)
            
            note = Notes.objects.create(
                title = form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                user=request.user,
                course=course,
                download_url=download_url,
                preview_url=preview_url,
                thumbnail_url=thumbnail_url
            )

            os.remove(filepath) # remove uploaded file from temp storage
            
            note.save()

            messages.success(request, "Note created successfully.")
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CreateNoteForm()

    return render(request, 'create_note.html', {'form': form})

