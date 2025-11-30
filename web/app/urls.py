
from django.urls import path
from .views import UploadView, RegisterAccount, LoginView,Posts,Index,PostsDetails,React,CommentCreateView,GetComments
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
path('',Index.as_view(),name=''),
path('registration/',RegisterAccount.as_view(),name='register'),
path('login/',LoginView.as_view(),name='login'),
path('upload/',UploadView.as_view(),name='index'),
path('posts/',Posts.as_view(),name='posts'),
path('cock-details/<int:pk>/',PostsDetails.as_view(),name='cock-details'),
path('react/',React.as_view(),name='react'),
path('comment/<int:id>/',CommentCreateView.as_view(),name='comment'),
path('comments/<int:id>/',GetComments.as_view(),name='comments'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)