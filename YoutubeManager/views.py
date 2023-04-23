from django.shortcuts import render
from pytube import YouTube
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def downloadVideo(request):
    criteria = json.loads(request.body.decode('utf-8'))
    stream = list(filter(
        lambda link: link.video_codec==criteria["video"] and 
                    link.audio_codec==criteria["audio"] and 
                    link.resolution==criteria["resolution"],
        list(YouTube(criteria["url"]).streams)
    ))
    if stream:
        stream[0].download("C:\\Users\\Anubhav.Sharma\\OneDrive - Brillio\\Pictures\\music")
    return render(request, "home.html")

def showHomePage(request):
    if request.method == "POST":
        return render(request, "home.html", {
            "search_url": request.POST.get("search_url"),
            "all_videos":searchForYoutubeVideos(request.POST.get("search_url"))
        })
    return render(request, "home.html")

def searchForYoutubeVideos(search_url):
    all_links = YouTube(search_url).streams
    return [{
        "resolution": link.resolution,
        "url": link.url,
        "title": link.title,
        "audio_codec": link.audio_codec,
        "video_codec": link.video_codec,
        "type": link.type
    } for link in all_links]
    