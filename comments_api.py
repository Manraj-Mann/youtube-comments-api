import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

def save_csv(name , data):
    
    # Create a Pandas DataFrame from the list of dictionaries
    playlist_df = pd.DataFrame(data)
    #  Save the DataFrame to a CSV file
    playlist_df.to_csv(f'{name}.csv', index=False)
    
    print("Stored {} as CSV !".format(name))


    
    
def fetch_playlist_details(youtube):
    
    # Call the YouTube Data API to fetch the playlist items.
    
    playlist_items = []
    next_page_token = None
    while True:
        playlist_items_response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        playlist_items += playlist_items_response["items"]
        next_page_token = playlist_items_response.get("nextPageToken")
        if not next_page_token:
            break

    # Extract the video IDs from the playlist items.
    video_ids = [item["contentDetails"]["videoId"] for item in playlist_items]

    return video_ids
    
def fetch_video_details (youtube , video_id):
    
    fetched_video_data = []
    
    video_response = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    ).execute()

    # category = video_response["items"][0]["topicDetails"]["topicCategories"][0]
    # # print("Video category: {}".format(category))
    # # print the video title.
    # print("Video title: {}".format(video_response["items"][0]["snippet"]["title"]))
    video_title = video_response["items"][0]["snippet"]["title"]
    # # print the channel name and subscriber count.
    channel_id = video_response["items"][0]["snippet"]["channelId"]
    channel_response = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    ).execute()
    
    channel_name = channel_response["items"][0]["snippet"]["title"]
    # print("Channel name: {}".format(channel_name))
    suscriber = channel_response["items"][0]["statistics"]["subscriberCount"]
    # print("Subscriber count: {}".format(suscriber))

    # # print the video length.
    duration = video_response["items"][0]["contentDetails"]["duration"]
    hours = duration.count("H")
    minutes = duration.count("M")
    seconds = duration.count("S")
    total_seconds = hours * 3600 + minutes * 60 + seconds
    # print("Video length: {}:{}:{}".format(hours, minutes, seconds))

    # # print the number of likes and comments.
    num_likes = video_response["items"][0]["statistics"]["likeCount"]
    # print("Number of likes: {}".format(num_likes))
    num_comments = video_response["items"][0]["statistics"]["commentCount"]
    # print("Number of comments: {}".format(num_comments))

    # Call the API to fetch comments.
    comments = []
    comments_response = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText"
    ).execute()

    # Add the comments from the first page to the comments list.
    for comment in comments_response["items"]:
        author = comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        likes = comment["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        text = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append({"author": author, "likes": likes, "text": text})

    
    # Fetch additional pages of comments if there are any.
    while "nextPageToken" in comments_response:
        comments_response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            pageToken=comments_response["nextPageToken"]
        ).execute()
        for comment in comments_response["items"]:
            author = comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            likes = comment["snippet"]["topLevelComment"]["snippet"]["likeCount"]
            text = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append({"author": author, "likes": likes, "text": text})  
                 
    # # print the comments.
    for comment in comments:
        # print("Comment by {} ({} likes): {}".format(comment["author"], comment["likes"], comment["text"]))
        time = "{}:{}:{}".format(hours, minutes, seconds)
        video_data = {
        "video_title": video_title,
        "channel_id": channel_id,
        "subscriber": suscriber,
        "time": time,
        "num_likes": num_likes,
        "num_comments": num_comments,
        "author": comment["author"],
        "likes": comment["likes"],
        "text": comment["text"]
        }
        fetched_video_data.append(video_data)
        
    return fetched_video_data
        
    
        
        

if __name__ == "__main__":
    
    try:
        with open('api_key.json', 'r') as f:
            creds = json.load(f)
        # replace with your API key
        API_KEY = creds["key"]
        # create YouTube API client
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        
        playlists = creds["playlists"]
        
        # making youtube object
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        comments_dataset = []
        
        print("\nProcessing Starting ..... \n\n")
        for playlist_id in playlists:
            print("\n-> Searching in playlist ID : " + playlist_id)
            for video_id in fetch_playlist_details(youtube):
                print("-----> Video : " + video_id + " done !")
                comments_dataset +=  fetch_video_details(youtube , video_id)
            print("\nPlaylist Finished ! ")
            
        print("\n")
        print("Process Finished" )
        
        print("\n")
        save_csv(creds["csv_name"], comments_dataset)
    except Exception as e : 
        print(e)

