from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profiles/<str:username>",views.profile, name="profile"),
    path("following/<str:user_id>", views.follow, name= "following"),

    # API  routes
    path("newPost", views.compose, name="compose"),
    path("post/<int:id>", views.get_post, name="get_post"),
    path("edit", views.compose, name="compose"),
    path("like/<int:post_id>", views.likes, name="likes"),
    path("follow/<int:user_id>",views.follow, name="follow"),

    
]
