from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from .forms import SignUpForm
from .models import Article, Roles


@login_required
def home(request):
    if request.user.role == Roles.EDITOR:
        return redirect("news_app:editor_dashboard")
    elif request.user.role == Roles.JOURNALIST:
        return redirect("news_app:journalist_dashboard")
    return redirect("news_app:reader_dashboard")


@login_required
def reader_dashboard(request):
    pubs = request.user.reader_subscriptions_publishers.all()
    journos = request.user.reader_subscriptions_journalists.all()
    articles = (Article.objects.filter(approved=True, publisher__in=pubs) |
                Article.objects.filter(approved=True, journalist__in=journos)).distinct().order_by("-created_at")
    return render(request, "news_app/reader_dashboard.html", {"articles": articles})


@login_required
def journalist_dashboard(request):
    articles = Article.objects.filter(journalist=request.user).order_by("-created_at")
    return render(request, "news_app/journalist_dashboard.html", {"articles": articles})


@login_required
def editor_dashboard(request):
    pending = Article.objects.filter(approved=False).order_by("created_at")
    return render(request, "news_app/editor_dashboard.html", {"pending": pending})


@login_required
@permission_required("news_app.change_article", raise_exception=True)
def approve_article(request, pk):
    if request.user.role != Roles.EDITOR:
        return HttpResponseForbidden("Editors only")
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.approved = True
        article.save()
        messages.success(request, "Article approved and notifications sent.")
        return redirect("news_app:editor_dashboard")
    return render(request, "news_app/approve_article.html", {"article": article})


def signup(request):
    from django.shortcuts import render, redirect
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            role = form.cleaned_data["role"]
            group = Group.objects.get(name=role)
            user.groups.add(group)

            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "news_app/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "news_app/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')

