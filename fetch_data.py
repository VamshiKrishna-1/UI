import pandas as pd
import re
import numpy as np
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from IPython.display import JSON



class Trending():
    def __init__(self):
        self.api_key = "AIzaSyCnXp_Hyf27VWDlhQfyW0axonuKfmX-6IA"
        self.allIds = None

    def getIdsFromResponse(Response):
        all_ids = []
        for item in Response["items"]:
            all_ids.append(item["id"])
        
        return all_ids


    def getAllIds(self):

        if self.allIds != None:
            return self.allIds

        else:
            api_service_name = "youtube"
            api_version = "v3"

            # Get credentials and create an API cl, recordingDetails, snippetient
            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey= self.api_key)

            request = youtube.videos().list(
                part="id",
                chart="mostPopular",
                maxResults = 50
            )
            response = request.execute()

            all_ids = Trending.getIdsFromResponse(response)

            next_page_token = response.get("nextPageToken")

            while next_page_token:
                request = youtube.videos().list(
                    chart="mostPopular",
                    part="id",
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                all_ids.extend(Trending.getIdsFromResponse(response))
                next_page_token = response.get("nextPageToken")

            return all_ids
    
    def isTrending(self, vid_id):
        if self.allIds == None:
            self.allIds = self.getAllIds()

        if vid_id in self.allIds:
            return True
        else:
            return False

    def extractVideoId(url):
        regex = r"(?<=v=)[\w-]+|(?<=be/)[\w-]+"
        match = re.search(regex, url)
        if match:
            return match.group(0)
        else:
            return None
        
    def getVideoInfo(self, vid_id):
        api_service_name = "youtube"
        api_version = "v3"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=self.api_key)

        request = youtube.videos().list(
            part="snippet,contentDetails,statistics,status",
            id=vid_id
        )
        response = request.execute()

        # Extract the desired values from the response
        title = response['items'][0]['snippet']['title']
        published_at = response['items'][0]['snippet']['publishedAt']
        channel_id = response['items'][0]['snippet']['channelId']
        channel_title = response['items'][0]['snippet']['channelTitle']
        category_id = response['items'][0]['snippet']['categoryId']
        description = response['items'][0]['snippet']['description']
        tags = response['items'][0]['snippet']['tags'] if 'tags' in response['items'][0]['snippet'] else []
        
        # Check if the video is trending
        trending_date = None
        view_count_trending = None
        like_count_trending = None
        comment_count_trending = None
        video_category_id = response['items'][0]['snippet']['categoryId']
        if video_category_id == "17":
            # Get the trending date
            trending_date = response['items'][0]['snippet']['publishedAt']
            
            # Get the number of views, likes, and comments on the day the video started trending
            view_count_trending = response['items'][0]['statistics']['viewCount']
            like_count_trending = response['items'][0]['statistics']['likeCount']
            comment_count_trending = response['items'][0]['statistics']['commentCount']
            
        # Get the current number of views, likes, and comments
        view_count_current = response['items'][0]['statistics']['viewCount']
        like_count_current = response['items'][0]['statistics']['likeCount']
        comment_count_current = response['items'][0]['statistics']['commentCount']

        # Return the extracted values as a dictionary
        return {
            "title": title,
            "published_at": published_at,
            "channel_id": channel_id,
            "channel_title": channel_title,
            "category_id": category_id,
            "description": description,
            "trending_date": trending_date,
            "tags": tags,
            "view_count_trending": view_count_trending,
            "view_count_current": view_count_current,
            "like_count_trending": like_count_trending,
            "like_count_current": like_count_current,
            "comment_count_trending": comment_count_trending,
            "comment_count_current": comment_count_current,
        }


    


if __name__ == "__main__":
    x = Trending()
    print(Trending.extractVideoId("https://www.youtube.com/watch?v=wFU1rF6DfWs"))





