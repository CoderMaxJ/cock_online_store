
from django.urls import path
from .views import UploadView, RegisterAccount, LoginView,Posts,Index,PostsDetails
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
path('',Index.as_view(),name=''),
path('registration/',RegisterAccount.as_view(),name='register'),
path('login/',LoginView.as_view(),name='login'),
path('upload/',UploadView.as_view(),name='index'),
path('posts/',Posts.as_view(),name='posts'),
path('cock-details/<int:pk>/',PostsDetails.as_view(),name='cock-details'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)