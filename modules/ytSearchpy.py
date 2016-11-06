#!/usr/bin/python

# https://developers.googleblog.com/2016/03/introducing-google-api-console.html
# https://github.com/youtube/api-samples/blob/master/python/search.py
# https://console.developers.google.com/apis/api/youtube/overview?project=ytplay-140505
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import urllib
import json as j
import os
import sys


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = os.environ['YT_API_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(title, maxresult=5):
  urls = []
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)


  # Call the search.list method to retrieve results matching the specified
  # query term.
  #options.q = urllib.quote_plus(options.q)
  title = urllib.quote_plus(title)
  print 'Title is ',title
  search_response = youtube.search().list(
    q=title,
    part="id,snippet",
    maxResults=maxresult,
    type="video",
    videoEmbeddable="true",
    relevanceLanguage="en"
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    #print
    #print search_result
    #  print j.loads(search_result)
    if search_result["id"]["kind"] == "youtube#video":
      urls.append( (search_result["snippet"]["title"], search_result["id"]["videoId"])  )
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

  #print videos
  #print "Videos:\n", "\n".join(videos), "\n"
  #print "Channels:\n", "\n".join(channels), "\n"
  #print "Playlists:\n", "\n".join(playlists), "\n"
  return urls


def find_video(e1, e2):
    query= e1 +" " + e2 + " differences"
    out = youtube_search(query, 10)
    output = []
    done = False
    for u in out:
        title = u[0].lower()
        e1matched, e2matched, diffMatched, vsMatched = False,False,False,False
        if title.find(e1) != -1: e1matched=True
        if title.find(e2) != -1: e2matched=True
        if title.find('difference') != -1: diffMatched=True
        if title.find('vs') != -1: vsMatched=True
        if e1matched and e2matched:
            if diffMatched or vsMatched:
                final = u
                done = True
                break

    pre = "https://www.youtube.com/embed/"
    suf = "?rel=0"
    if done:

        output.append( (e1, pre + final + suf) )
        output.append( (e2, pre + final + suf) )
        print 'matched', final
    else:
        print "nothing matched"
        # go to find 2 video
        out = youtube_search('description of '+e1, 1)
        output.append( (e1, pre + out[0][1] + suf) )
        out = youtube_search('description of '+e2, 1)
        output.append( (e2, pre + out[0][1]+ suf) )
    return output

if __name__ == "__main__":
#  argparser.add_argument("--q", help="Search term", default="Google")
#  argparser.add_argument("--max-results", help="Max results", default=5)
#  args = argparser.parse_args()
#  args.q=title

  try:
    e1 = 'india'.lower()
    e2 = 'indonesia'.lower()
    print find_video(e1,e2);

  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

#def main(*args, **kwargs):
#from subprocess import call
#
#def get_call_array(command=command,**kwargs):
#    callarray = [command]
#    for k, v in self.kwargs.items():
#    callarray.append("--" + k)
#    if v:
#    callarray.append(str(v))
#    return callarray
#
#    main(get_call_array("ytSearch",height=5,width=10,trials=100,verbose=None))
#
#    #main(3, {'--q':"india usa"})

