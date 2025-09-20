from django.urls import path
from . import views

app_name = "news_app"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path('signup/', views.signup, name='signup'),
    path("logout/", views.logout_view, name="logout"),
    path("reader/", views.reader_dashboard, name="reader_dashboard"),
    path("journalist/", views.journalist_dashboard, name="journalist_dashboard"),
    path("editor/", views.editor_dashboard, name="editor_dashboard"),
    path("editor/approve/<int:pk>/", views.approve_article, name="approve_article"),
]
