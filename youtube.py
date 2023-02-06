import json
from flask import Flask, render_template, current_app, request
import requests
#from isodate import parse_duration

YOUTUBE_API_KEY = "AIzaSyDJmXeAfnBfI0uHHiG-J75DoJVgVbsDOLw"

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods = ['GET','POST'])
def index():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []

    if request.method == 'POST':

        search_param = {
            'key' : YOUTUBE_API_KEY,
            'q' : request.form.get('search'),
            'part' : 'snippet' ,
            'maxResults' : 9 ,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_param)

        res = r.json()['items']

        video_ids = []

        for i in res:
            video_ids.append(i['id']['videoId'])
        
        #print(video_ids)

        video_params = {
            'key' : YOUTUBE_API_KEY,
            'id' : ','.join(video_ids),
            'part' : 'snippet,contentDetails,statistics',
            'maxResults' : 9 
        }
        rv = requests.get(video_url ,params=video_params)

        result_vid = rv.json()['items']
        videos = []
        for i in result_vid:
            video_data = {
                'id' : i['id'],
                'url' : 'https://www.youtube.com/watch?v=' + str(i['id']),
                'duration' : i['contentDetails']['duration'],
                'title' : i['snippet']['title'],
                'viewCount' : i['statistics']['viewCount'],
                'likeCount' : i['statistics']['likeCount'],
                'commentCount' : i['statistics']['commentCount'],
                #'tags' : i['snippet']['tags']
            }
            videos.append(video_data)

    return render_template('index.html', videos = videos)
