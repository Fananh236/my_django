from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Static pages
    path("home/", views.home, name="home"),
    path("welcome/", views.welcome, name="welcome"),
    path("about/", views.about, name="about"),

    # Category
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path(
        "categories/<int:pk>/notes/",
        views.CategoryNoteListView.as_view(),
        name="category_notes",
    ),
    path("categories/create/", views.CategoryCreateView.as_view(), name="category_create"),

    # Notes CRUD
    path("notes/", views.NoteListView.as_view(), name="note_list"),
    path("notes/create/", views.NoteCreateView.as_view(), name="note_create"),
    path("notes/<int:pk>/", views.NoteDetailView.as_view(), name="note_detail"),
    path("notes/<int:pk>/edit/", views.NoteUpdateView.as_view(), name="note_update"),
    path("notes/<int:pk>/delete/", views.NoteDeleteView.as_view(), name="note_delete"),

    # Contact
    path("contact/", views.contact, name="contact"),

    # Auth
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
]
