KEY = 'key'
SECRET = 'secret'
REQUEST_API = 'request'
AUTH_API = 'auth'
ACCESS_API = 'access'
REST_API = 'rest'
UPLOAD_API = 'upload'

FLICKR = 'flickr'
TWITTER = 'twitter'

flickr_dict = {
    KEY: 'FILL_ME',
    SECRET: 'FILL_ME',
    REQUEST_API: 'http://www.flickr.com/services/oauth/request_token',
    AUTH_API: 'https://www.flickr.com/services/oauth/authorize',
    ACCESS_API: 'https://www.flickr.com/services/oauth/access_token',
    REST_API: 'https://api.flickr.com/services/rest',
    UPLOAD_API: 'https://up.flickr.com/services/upload',
}
twitter_dict = {
    KEY: 'FILL_ME',
    SECRET: 'FILL_ME',
    REQUEST_API: 'https://api.twitter.com/oauth/request_token',
    AUTH_API: 'https://api.twitter.com/oauth/authorize',
    ACCESS_API: 'https://api.twitter.com/oauth/access_token',
    REST_API: 'https://api.twitter.com/1.1/statuses/update.json',
    UPLOAD_API: 'https://upload.twitter.com/1.1/media/upload.json'
}
master_dict = {
    FLICKR: flickr_dict,
    TWITTER: twitter_dict
}

HOST_NAME = 'localhost'
PORT = 8080

GET_REQUEST = 'GET'
POST_REQUEST = 'POST'
ENCODING_METHOD = 'HMAC-SHA1'
VERSION = '1.0'
CALLBACK_URL = 'http://127.0.0.1:8080'

DELIMITER = '&'
EQUALS = '='
QUERY = '?'
MIME = 'image/jpeg'

# User Specific Data
HASHTAG = '#ChingandLooSayIDo'
SRC = '/Users/kaleb-johnloo/Documents/Code/Camera'
DST = '/Users/kaleb-johnloo/Documents/Code/Pictures'

# Twitter Upload States
INIT = 'INIT'
APPEND = 'APPEND'
FINALIZE = 'FINALIZE'
