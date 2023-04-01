# YouTube Playlist Comments API

This Python API allows you to easily retrieve comments from one or more YouTube playlists using the YouTube Data API, and save the data to a CSV file for further analysis or processing. With this API, you can quickly gather valuable insights into the engagement and sentiment of your audience, and use that information to optimize your content and grow your channel.

Using the API is simple and straightforward. All you need to do is provide your YouTube API key, one or more playlist IDs, and a name for the CSV file where the comments data will be saved. The API will take care of the rest, fetching the comments data and saving it to the specified CSV file for easy access and analysis.

Some of the key features of the YouTube Playlist Comments API include:

- Easy authentication with your YouTube API key
- Flexible support for one or more playlist IDs
- Automatic pagination for handling large datasets
- Robust error handling for handling API errors and exceptions
- Simple and intuitive API interface for easy integration with your existing Python codebase

Whether you're a content creator, marketer, or analyst, the YouTube Playlist Comments API is a powerful tool that can help you gain deeper insights into your YouTube audience, and make data-driven decisions to improve your content and grow your channel. Try it out today and see the difference for yourself!

![YouTube Playlist Comments API](ec_191219_m.jpg)

## Installation

Run the following command in command promp or terminal : 

```gitbash 
git clone https://github.com/Manraj-Mann/youtube-comments-api.git
```
```bash
cd youtube-comments-api
```
To use this API, you'll need to install the following packages:

- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`
- `google-api-python-client`
- `pandas`

You can install these packages using pip:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pandas
```
## Usage

To use the API, you'll need to provide your YouTube API key, one or more playlist IDs, and a name for the CSV file where the comments data will be saved.
This data is stored in api_key.json file : 

Initially it will look like : 

```json
{
    "key" : "<Replace API Key here >",
    "playlists" : ["<Playlist ID 1>" ,"<Playlist ID 2>"],
    "csv_name" : "<<CSV Filename>>"
}
```
After adding the credentials and details it will look like : 
```json
{
    "key" : "AIzaSyBbbaBy_EWgyZhU1QcVLdRjXMPmV5OmAtU",
    "playlists" : ["PLWKjhJtqVAbmGw5fN5BQlwuug-8bDmabi" ,"PLWKjhJtqVAbm5dir5TLEy2aZQMG7cHEZp"],
    "csv_name" : "freecodecamp_comments"
}
```
**Note** : You can add any number of playlist ID's in the list.

## Running the API

Open the command promp or terminal and run the following in same directory : 

```bash
python comments_api.py
```

