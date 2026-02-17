from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Note, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ContactForm, NoteForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


def welcome(request):
    return render(request, 'notes/welcome.html')

def about(request):
    return render(request, 'notes/about.html')

def home(request): 
    return HttpResponse("Hello")



class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "notes/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)



class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ["name"]
    template_name = "notes/category_form.html"
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CategoryNoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "notes/category_note_list.html"
    context_object_name = "notes"

    def get_queryset(self):
        category_id = self.kwargs["pk"]
        return Note.objects.filter(category_id=category_id, owner=self.request.user)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)  # IN RA CONSOLE
            messages.success(request, "Gửi thông tin thành công 🎉")
            return redirect("home")   # quay về trang chủ
    else:
        form = ContactForm()

    return render(request, "notes/contact_form.html", {"form": form})


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"
    paginate_by = 10

    def get_queryset(self):
        queryset = Note.objects.filter(owner=self.request.user).order_by("-id")
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = "notes/note_detail.html"
    context_object_name = "note"

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("note_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("note_list")

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy("note_list")

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
