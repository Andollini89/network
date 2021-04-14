import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.signals import user_logged_in
from django.core.checks import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import *

@login_required(login_url="login")
def index(request):
   
    posts = Post.objects.all().order_by("-date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "posts": page_obj,
    })

@login_required(login_url="login")
def compose(request):
   
    if request.method == "POST":
        data =json.loads(request.body)
        user = User.objects.get(username=request.user)
        new_post = Post(creator=user, post_body=data["body"].strip(), date=datetime.datetime.now())
        new_post.save()
        print(new_post)
        return JsonResponse({"message": new_post.id})
    elif request.method == "PUT":
        data =json.loads(request.body)
        post = Post.objects.get(pk= data["id"])
        post.post_body = data["body"]
        post.save()
        print(post.post_body)
        return JsonResponse({"message":"post modified"})
    elif request.method == "DELETE":
        data = json.loads(request.body)
        post = Post.objects.get(pk=data["id"])
        post.delete()
        return JsonResponse({"message": "post deleted"})
    else:
        return JsonResponse({"error": "Bad request"}, status=404)

def get_post(request,id):

    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "post does not exist"})

    return JsonResponse(post.serialize())

@login_required(login_url="login")
def profile(request, username):

    user = User.objects.get(username= username)
    posts = Post.objects.filter(creator=user.id).order_by("date").reverse()
    followers = Follower.objects.filter(followed= user).count()
    followed = Follower.objects.filter(follower= user).count()
    try:
        f_un_f = Follower.objects.get(follower=request.user, followed= user)
        if f_un_f:
            f_un_f = "Unfollow"
    except:
        f_un_f = "Follow"
    print(posts)

    return render(request, "network/profile.html",{
        "posts": posts,
        "username": user,
        "followers": followers,
        "followed": followed,
        "f_un_f": f_un_f,
    })
@login_required(login_url="login")
def likes(request, post_id):

    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(username= request.user)
        post = Post.objects.get(pk=post_id)

        try:
            already_like = Like.objects.get(liker=user, post=post,like=True)
            if already_like:
                already_like.delete()
                return JsonResponse({"message": "like removed",
                            "likes": -1})
        except:
            pass

        likes = Like(liker=user, post=post, like=data["like"])
        post.likes.add(user)
        likes.save()
        post.save()
        print(data, likes)
        return JsonResponse({"message": "like added",
                            "likes": 1})
    else:
        likes = Like.objects.filter(post=post_id).count()
        print(likes)
        return JsonResponse({"results": likes})
@login_required(login_url="login")
def follow(request,user_id):

    if request.method == "POST":
        data = json.loads(request.body)
        follower = User.objects.get(username= request.user)
        followed = User.objects.get(pk=user_id)

        if follower == followed:
            return JsonResponse({"error": "user can't follow himself"})
        try:
            already_follower = Follower.objects.get(follower=follower, followed=followed, follow=True)
            if already_follower:
                already_follower.delete()
                return JsonResponse({"message": "follow removed",
                                    "follow": False})
        except:
            pass
        follow = Follower(follower= follower, followed= followed, follow= data["follow"])
        follow.save()
        return JsonResponse({"result":"follow added", "follow": True})
    else:
        posts = []
        user = User.objects.get(username= request.user)
        follows = Follower.objects.filter(follower= user)
        all_posts = Post.objects.all().order_by("-date")
        for post in all_posts:
            for follow in follows:
                if post.creator == follow.followed:
                    posts.append(post)

        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html",{
            "posts": page_obj,
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
