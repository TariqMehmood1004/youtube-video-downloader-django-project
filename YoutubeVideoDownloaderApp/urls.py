from django.urls import path
from . import views

app_name = 'YoutubeVideoDownloaderApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.url_to_video_download, name='url_to_video_download'),
]
