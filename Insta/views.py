from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from Insta.models import Post, InstaUser, Like, Follow, Comment

from django.contrib.auth.mixins import LoginRequiredMixin
from Insta.forms import CustomUserCreationForm
# from django.contrib.auth.forms import UserCreationForm


# Create your views here.
class HelloWorld(TemplateView):
    template_name = 'test.html'


class PostsView(ListView):
    model = Post
    queryset = Post.objects.order_by('-posted_on')
    template_name = 'index.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'image']
    login_url = 'login'
    success_url = reverse_lazy('post')

    def form_valid(self, form):
        user = self.request.user
        form.instance.author_id = user.pk
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post')


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")


class UserProfile(DetailView):
    model = InstaUser
    template_name = 'user_detail.html'


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comments']
    success_url = 'post'
    login_url = 'login'
    template_name = 'comment_create.html'
    

@ajax_request
def addLike(request):
    if not request.user.is_authenticated:
        return {
            'result': -1,
        }
    post_pk = request.POST.get('post_id')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0
    return {
        'result': result,
        'post_pk': post_pk
    }

@ajax_request
def addFollow(request,pk):
    print("Now in addFollow function") 
    # print("Request is")
    # print(request)
    # print("pk is")
    # print(pk)
    if not request.user.is_authenticated:
        return {
            'result': -1
        }
    thePk = None
    followType = None
    if(request.method == 'POST'):
        thePk = request.POST.get('followed_pk')
        followType = request.POST.get('type')
    if thePk is None or followType is None:
        return {
            'result': -2
        }
    try:
        follow = Follow(follower=request.user, followed=InstaUser.objects.get(pk=thePk))
        follow.save()
        print("New follow object saved!")
        result = 1
    except Exception as e:
        follow = Follow.objects.get(follower=request.user, followed=InstaUser.objects.get(pk=thePk))
        follow.delete()
        print("Follow object deleted!")
        result = 0
    return {
        'result': result,
        'followed_pk': thePk
    }

    