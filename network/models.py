from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass

# model for post
class Post(models.Model):
    # telx field
    post_body = models.TextField(max_length=500)
    # date field
    date = models.DateTimeField(auto_now_add=True)
    # user field
    creator = models.ForeignKey("User", on_delete=models.CASCADE, related_name="creator")

    likes = models.ManyToManyField("User", default=None, related_name="likes")
    
    def serialize(self):
        return {
            "body": self.post_body.replace("\n","<br>"),
            "date":self.date.strftime('%b %d %Y, %I:%M %p'),
            "creator":self.creator.username,

        }
    def __str__(self):
        return f"{self.creator} posted {self.post_body[:50]}... on {self.date.strftime('%b %d %Y, %I:%M %p')}"

# model for follows
class Follower(models.Model):
    # follower referece
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follower")
    # followed reference
    followed = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followed")
    # follows
    follow = models.BooleanField(default=False)

    def serialize(self):
        return {
            "follower": self.follower.id,
            "followed": self.followed.id,
            "follow": self.follow
        }

    def __str__(self):
        if self.follow:
            return f"{self.follower} Follow {self.followed}"
        else:
            return f"{self.follower} Un-follow {self.followed}"

# model for like
class Like(models.Model):
    # user reference
    liker = models.ForeignKey("User", on_delete=models.CASCADE, related_name="liker")
    # post reference
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post")
    # like boolean field
    like = models.BooleanField(default=False)

    def serialize(self):
        return {
            "liker":self.liker.id,
            "post": self.post.id,
            "like": self.like
        }

    def __str__(self):
        if self.like:
            return f"{self.liker} Likes {self.post.post_body}"
        else:
            return f"{self.liker} Un-likes {self.post.post_body}"