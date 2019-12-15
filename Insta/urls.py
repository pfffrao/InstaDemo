from django.urls import include, path
from Insta.views import HelloWorld

urlpatterns = [
    path('', HelloWorld.as_view(), name='helloworld')
]