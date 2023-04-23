from django.shortcuts import render
from pytube import YouTube
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def downloadVideo(request):
    criteria = json.loads(request.body.decode('utf-8'))
    if criteria["video"]=='None': criteria["video"]=None
    if criteria["audio"]=='None': criteria["audio"]=None 
    if criteria["resolution"]=='None': criteria["resolution"]=None
    stream = list(filter(
        lambda link: link.video_codec==criteria["video"] and 
                    link.audio_codec==criteria["audio"] and 
                    link.resolution==criteria["resolution"],
        list(YouTube(criteria["url"]).streams)
    ))
    if stream:
        stream[0].download("C:\\Users\\Anubhav.Sharma\\Downloads\\Music\\")
    else:
        raise Exception("Video not found Audio: {} Video: {} Resolution: {} ".format(
            criteria["audio"],
            criteria["video"],
            criteria["resolution"]
        )) 
    return render(request, "home.html")

def showHomePage(request):
    if request.method == "POST":
        return render(request, "home.html", {
            "search_url": request.POST.get("search_url"),
            "filter_criteria": request.POST.get("filter_criteria"),
            "all_videos":searchForYoutubeVideos(request.POST.get("search_url"), request.POST.get("filter_criteria"))
        })
    return render(request, "home.html")

def searchForYoutubeVideos(search_url, filter_criteria):
    all_links = list(YouTube(search_url).streams)
    
    if filter_criteria=="audio": all_links = list(filter(lambda link: not link.video_codec and link.audio_codec, all_links))
    elif filter_criteria=="audio_video": all_links = list(filter(lambda link: link.video_codec and link.audio_codec, all_links))
    elif filter_criteria=="video": all_links = list(filter(lambda link: link.video_codec and not link.audio_codec, all_links))
    
    return [{
        "resolution": link.resolution,
        "url": link.url,
        "title": link.title,
        "audio_codec": link.audio_codec,
        "video_codec": link.video_codec,
        "type": link.type
    } for link in all_links]
    