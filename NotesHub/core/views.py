from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *

from .utils import *
import os

@login_required(login_url='login')
def index(request):
    query = request.GET.get('query', '')
    if query:
        courses = Course.objects.filter(
            course_name__icontains=query) | Course.objects.filter(
            description__icontains=query)
    else:
        courses = Course.objects.all()
    
    return render(request, 'home.html', {'courses': courses})
# def index(request):    
#     courses = Course.objects.all()

#     # Pass courses to the template context
#     return render(request, 'home.html', {'courses': courses})

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


@login_required(login_url='login')
def notesView(request, course_code):
    # Fetch the course using the course_code from the URL
    course = get_object_or_404(Course, course_code=course_code)
    
    # Fetch all notes related to the course
    notes = Notes.objects.filter(course=course)
    
    # Pass the course and its notes to the template context
    # return render(request, 'course_notes.html', {'course': course, 'notes': notes})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'query' in request.GET:
        query = request.GET.get('query', '').strip()
        # Filter notes based on title or description containing the search term
        filtered_notes = notes.filter(
            title__icontains=query
        ) | notes.filter(description__icontains=query)
        
        # Serialize the filtered notes for the response
        notes_data = list(filtered_notes.values('id', 'title', 'description', 'user__username', 'thumbnail_url'))
        return JsonResponse({'notes': notes_data})
    
    # Pass the course and its notes to the template context for initial load
    return render(request, 'course_notes.html', {'course': course, 'notes': notes})


@login_required(login_url='login')
def search_courses(request):
    query = request.GET.get('query', '')
    if query:
        courses = Course.objects.filter(
            course_name__icontains=query) | Course.objects.filter(
            description__icontains=query)
    else:
        courses = Course.objects.all()

    # Serialize courses to return as JSON
    courses_data = [
        {
            'course_code': course.course_code,
            'short_name': course.short_name,
            'course_name': course.course_name,
            'thumbnail_url': '/static/images/notes.png',  # Add a real thumbnail URL
        }
        for course in courses
    ]
    
    return JsonResponse({'courses': courses_data})

@login_required(login_url='login')
def search_bookmarks(request):
    
    user = request.user
    bookmarked_notes = Notes.objects.filter(bookmark__user=user).distinct()
    

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'query' in request.GET:
        query = request.GET.get('query', '').strip()
        # Filter notes based on title or description containing the search term
        filtered_notes = bookmarked_notes.filter(
            title__icontains=query
        ) | bookmarked_notes.filter(description__icontains=query)
        
        # Serialize the filtered notes for the response
        notes_data = list(filtered_notes.values('id', 'title', 'description', 'user__username', 'thumbnail_url'))
        return JsonResponse({'notes': notes_data})
    
    # Pass the course and its notes to the template context for initial load
    return render(request, 'bookmarks.html', {'notes': bookmarked_notes})

@login_required(login_url='login')
def analyticsView(request, type, id):

    data = {
        'view_count': 50,
        'total_time_spent': 120,
        'downloaded_times': 10,
        'upvotes': 20,
        'downvotes': 2,
        'bookmark_count':7,
        'avg_time_per_view': 1,
        'engagement_rate': 1,
        'upvote_ratio': 1,
        'user_engagement': [],
        'user_time_view': []
    }

    if type == 'note':
        # note = get_object_or_404(Notes, id=int(id))

        # engagement_rate = (note.upvotes + note.bookmark_count) / note.view_count * 100
        # upvote_ratio = note.upvotes / (note.upvotes + note.downvotes)
        # avg_time_per_view = note.total_time_spent / note.view_count

        data['title'] = 'Notes Analytics'
        # data['view_count'] = note.view_count
        # data['total_time_spent'] = note.total_time_spent
        # data['downloaded_times'] = note.downloaded_times
        # data['upvotes'] = note.upvotes
        # data['downvotes'] = note.downvotes
        # data['bookmark_count'] = note.bookmark_count
        # data['engagement_rate'] = engagement_rate
        # data['upvote_ratio'] = upvote_ratio
        # data['avg_time_per_view'] = avg_time_per_view

    elif type == 'user':

        # user = get_object_or_404(User, username=id)
        #TODO: group by date also for better analytics
        # notes = Notes.objects.filter(user=user).order_by('created_at').values()
        
        data['title'] = 'User Analytics'
        # data['view_count'] = notes.aaggregate(Sum('view_count'))
        # data['total_time_spent'] = notes.aaggregate(Sum('total_time_spent'))
        # data['downloaded_times'] = notes.aaggregate(Sum('downloaded_times'))
        # data['upvotes'] = notes.aaggregate(Sum('upvotes'))
        # data['downvotes'] = notes.aaggregate(Sum('downvotes'))
        # data['bookmark_count'] = notes.aaggregate(Sum('bookmark_count'))

        # engagement_rate = (data['upvotes'] + data['bookmark_count']) / data['view_count'] * 100
        # upvote_ratio = data['upvotes'] / (data['upvotes'] + data['downvotes'] + 1) # +1 to handle divide by zero exception
        # avg_time_per_view = data['total_time_spent'] / data['view_count']

        # data['engagement_rate'] = engagement_rate
        # data['upvote_ratio'] = upvote_ratio
        # data['avg_time_per_view'] = avg_time_per_view

        # for note in notes:
        #     data['view_count'] += note.view_count
        #     data['total_time_spent'] += note.total_time_spent
        #     data['downloaded_times'] += note.downloaded_times
        #     data['upvotes'] += note.upvotes
        #     data['downvotes'] = note.downvotes
        #     data['bookmark_count'] = note.bookmark_count

        #     data['user_engagement'].append({
        #         'label': note.created_at.strftime('%Y-%m-%d'),
        #         'x': note.view_count,
        #         'y': getEngagementRate(note)
        #     })

        #     data['user_time_view'].append({
        #         'labels': note.created_at.strftime('%Y-%m-%d'),
        #         'data': getAvgTimePerView(note)
        #     })
        # data['engagement_rate'] = (data['upvotes'] + data['bookmark_count']) / data['view_count'] * 100 if data['view_count'] > 0 else 0
        # data['upvote_ratio'] = data['upvotes'] / (data['upvotes'] + data['downvotes']) if data['upvotes'] + data['downvotes'] > 0 else 0
        # data['avg_time_per_view'] = data['total_time_spent'] / data['view_count']


    return render(request, 'analytics.html', {'data': data})