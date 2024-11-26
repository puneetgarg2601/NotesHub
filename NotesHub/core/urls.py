# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Example route
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('logout/', views.logoutView, name='logout'),
    path('create-note/', views.createNoteView, name='create-note'),
    path('analytics/<str:type>/<str:id>/', views.analyticsView, name='analytics'),
    path('search/', views.search_courses, name='search_courses'),
    path('course/<str:course_code>/notes/', views.notesView, name='course_notes'),
    path('bookmarks/', views.search_bookmarks, name='bookmark'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),
    path('toggle_like/<int:note_id>/', views.toggle_like, name='toggle_like'),
    path('toggle_dislike/<int:note_id>/', views.toggle_dislike, name='toggle_dislike'),
    path('toggle_bookmark/<int:note_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('track-time/', views.track_time_view, name='track_time'),
    path('increment-download-count/<int:note_id>/', views.increment_download_count, name='increment_download_count'),
]
