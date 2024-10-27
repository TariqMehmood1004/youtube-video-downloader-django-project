from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from yt_dlp import YoutubeDL
import os
import logging

def index(request):
    return render(request, 'index.html')



def url_to_video_download(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        if not video_url:
            return HttpResponseBadRequest("No video URL provided.")

        try:
            # Define the options for yt-dlp
            ydl_opts = {
                'format': 'bestvideo[height<=1080]+bestaudio/best',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'prefer_ffmpeg': True,
                'merge_output_format': 'mp4',
                'progress_hooks': [lambda d: logging.info(f"Downloaded {d['downloaded_bytes'] / 1024 / 1024:.2f} MB")],
                'progress_hooks': [lambda d: logging.info(f"Downloaded {d['downloaded_bytes'] / 1024 / 1024:.2f} MB")],
                'logger': logging.getLogger(),
                'outtmpl': '/media/downloads/%(title)s.%(ext)s',
                'writethumbnail': True
            }

            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                video_title = info_dict.get('title', 'downloaded_video')
                video_path = ydl.prepare_filename(info_dict)

            # Serve the video file as response
            with open(video_path, 'rb') as video_file:
                response = HttpResponse(video_file.read(), content_type="video/mp4")
                response['Content-Disposition'] = f'attachment; filename="{video_title}.mp4"'

            os.remove(video_path)  # Clean up after download
            return response

        except Exception as e:
            return HttpResponseBadRequest(f"Error downloading video: {str(e)}")
    else:
        return HttpResponseBadRequest("Invalid request method.")

