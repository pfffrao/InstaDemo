from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
import datetime


# Create your models here.
class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to='static/images/profiles',
        format='JPEG',
        options={'quality': 90},
        blank=True,
        null=True
    )
    registered_on = models.DateTimeField(auto_now_add=True)

    def get_following(self):
        following = Follow.objects.filter(follower=self)
        return following

    def get_followers(self):
        follower = Follow.objects.filter(followed=self)
        return follower

    def is_followed_by(self, user):
        follower = Follow.objects.filter(followed=self)
        return follower.filter(follower=user).exists()

    def is_following(self, user):
        following = Follow.objects.filter(follower=self)
        return following.filter(followed=user).exists()


class Post(models.Model):
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to='static/images/posts',
        format='JPEG',
        options={'quality': 90},
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='my_posts')
    
    posted_on = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("post_detail", args=str(self.id))

    def get_like_count(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    commentor = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    comments = models.CharField(max_length=140)
    datetime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.commentor + " commented on " + self.date + self.comments

class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes')
    user = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='likes')

    class Meta:
        unique_together = ["post", "user"]

    def __str__(self):
        return self.user.username + ' likes ' + self.post.title


class Follow(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    follower = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='follower')
    followed = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='followed'
    )

    class Meta:
        unique_together = ['follower', 'followed']

    def __str__(self):
        return self.follower.username + ' followed ' + self.followed.username
