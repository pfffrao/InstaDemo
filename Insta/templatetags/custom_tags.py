from django import template
# from django.urls import NoReverseMatch, reverse
from Insta.models import Like, Follow
from InstaDemo.settings import STATICFILES_DIRS
import os


register = template.Library()


@register.simple_tag
def has_user_liked_post(post, user):
    try:
        like = Like.objects.get(user=user, post=post)
        if like:
            return "fa-heart"
    except:
        return "fa-heart-o"


@register.simple_tag
def is_following(follower, followed):
    try:
        following = followed.followed.filter(follower=follower)
        if following:
            return True
        else:
            return False
    except:
        return False


@register.simple_tag
def get_posts(user):
    return user.my_posts.filter()


def has_user_followed(follower, followed):
    try:
        follow = followed.followed.filter(follower=follower)
        if follow:
            return True
        else:
            return False
    except:
        return False


register.filter('checkFollow', has_user_followed)


def post_filter(post_list, user):
    if not user.is_authenticated:
        return post_list
    filtered = []
    for post in post_list:
        if user.is_following(post.author) or post.author is user:
            filtered.append(post)
    return filtered


register.filter('post_filter', post_filter)

@register.simple_tag
def get_local_assets(static_path):
    path_prefix = STATICFILES_DIRS[0]
    print("path_prefix:" + path_prefix)
    return os.path.join(path_prefix, static_path)