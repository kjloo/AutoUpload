#!/bin/python
import os
import random
import time
import webbrowser
import calendar
import hmac
import urllib2
import base64
from hashlib import sha1

# install requests
import requests

# import constants
from constants import *
from upload_functions import *
from upload_server import *

class RestApi:
    def __init__(self, rest):
        self.rest = rest
        self.rest_info = master_dict[rest]

    def oauth_encode(self, url):
        special_char = ['_', '-', '.', '~']
        return ''.join([i if (i in special_char or i.isalnum()) else '%' + i.encode('hex').upper() for i in url])

    def generate_nonce(self, length=8):
        """
        Generate random number string
        """
        return ''.join([str(random.randint(0, 9)) for i in range(length)])

    def get_query_string(self, parameters):
        tag = DELIMITER.join([key + '=' + urllib2.quote(parameters[key], '') for key in sorted(parameters)])
        return tag

    def get_signature(self, http_request, url, tag, token_secret):
        tag = self.oauth_encode(tag)
        raw = DELIMITER.join([http_request, url, tag])
        key = self.rest_info[SECRET] + DELIMITER + token_secret
        hashed = hmac.new(key, raw, sha1)
        signature = hashed.digest().encode("base64").rstrip('\n')
        return signature

    def get_signature_url(self, url, parameters, token_secret="", http_request=GET_REQUEST):
        http_url = self.oauth_encode(url)
        parameters['oauth_consumer_key'] = self.rest_info[KEY]
        parameters['oauth_nonce'] = self.generate_nonce()
        parameters['oauth_signature_method'] = ENCODING_METHOD
        parameters['oauth_timestamp'] = str(calendar.timegm(time.gmtime()))
        parameters['oauth_version'] = VERSION
        tag = self.get_query_string(parameters)
        signature = self.get_signature(http_request, http_url, tag, token_secret)
        url = url + QUERY + tag + '&oauth_signature=' + urllib2.quote(signature, '')
        return url

    def get_request_url(self):
        url = self.rest_info[REQUEST_API]
        parameters = {}
        parameters['oauth_callback'] = CALLBACK_URL
        request = self.get_signature_url(url, parameters)
        return request

    def get_access_url(self, query, token):
        url = self.rest_info[ACCESS_API]
        parameters = {}
        parameters['oauth_token'] = query['oauth_token']
        parameters['oauth_verifier'] = query['oauth_verifier']
        access = self.get_signature_url(url, parameters, token['oauth_token_secret'])
        return access


    def get_rest_url(self, parameters, request=POST_REQUEST):
        token = self.access_token
        url = self.rest_info[REST_API]
        parameters['oauth_token'] = token['oauth_token']
        rest = self.get_signature_url(url, parameters, token['oauth_token_secret'], request)
        return rest
    
    def test_rest(self, method, request=GET_REQUEST):
        url = self.rest_info[REST_API]
        parameters = {}
        parameters['nojsoncallback'] = '1'
        parameters['format'] = 'json'
        parameters['oauth_token'] = token['oauth_token']
        parameters['method'] = method
        url = self.get_rest_url(parameters, request)

    def get_upload_url(self, parameters={}):
        token = self.access_token
        url = self.rest_info[UPLOAD_API]
        parameters['oauth_token'] = token['oauth_token']
        upload = self.get_signature_url(url, parameters, token['oauth_token_secret'], POST_REQUEST)
        return upload

    def upload_photo(self, photo):
        url = self.get_upload_url()
        query = parse_query_string(url)
        url = self.rest_info[UPLOAD_API]
        files = {"photo": open(photo, "rb")}
        r = requests.post(url, data=query, files=files)
        print r.text

    def get_oauth_token(self, url):
        oauth = {}
        data = urllib2.urlopen(url).read()
        data = data.split(DELIMITER)
        oauth = dict(pair.split(EQUALS) for pair in data)
        return oauth

    def get_user_authorization(self):
        request_url = self.get_request_url()
        request_token = self.get_oauth_token(request_url)
        token = "oauth_token=" + request_token['oauth_token']
        permissions = "perms=write"
        url = self.rest_info[AUTH_API] + QUERY + token + DELIMITER + permissions
        return url, request_token

    def get_access_token(self, query, request_token):
        access_url = self.get_access_url(query, request_token)
        access_token = self.get_oauth_token(access_url)
        return access_token

    def authorize_user(self):
        url, request_token = self.get_user_authorization()
        webbrowser.open(url)
        server_class = RestServer
        httpd = server_class((HOST_NAME, PORT), RestHandler)
        #httpd.allow_reuse_address = True
        httpd.handle_request()
        httpd.server_close()
        self.access_token = self.get_access_token(httpd.storage.query, request_token)

class TwitterRestApi(RestApi):

    def __init__(self, rest):
        RestApi.__init__(self, rest)

    def post_status(self, media_id):
        parameters = {}
        parameters['status'] = HASHTAG
        parameters['media_ids'] = media_id
        url = self.get_rest_url(parameters, POST_REQUEST)
        query = parse_query_string(url)
        url = self.rest_info[REST_API]
        r = requests.post(url, data=query)
        
    def post_media(self, parameters):
        url = self.get_upload_url(parameters)
        query = parse_query_string(url)
        url = self.rest_info[UPLOAD_API]
        r = requests.post(url, data=query)
        return r

    def media_init(self, file_size):
        parameters = {}
        parameters['command'] = INIT
        parameters['total_bytes'] = str(file_size)
        parameters['media_type'] = MIME
        r = self.post_media(parameters)
        return r.json()['media_id_string']

    def media_append(self, media_id, photo):
        # Use base64 encoding. Raw Binary does not seem to work
        #encoded = base64.b64encode(open(photo, 'rb').read())
        encoded = base64.b64encode(photo.getvalue())
        parameters = {}
        parameters['command'] = APPEND
        parameters['media_id'] = media_id
        parameters['media_data'] = encoded
        parameters['segment_index'] = '0'
        r = self.post_media(parameters)

    def media_finalize(self, media_id):
        parameters = {}
        parameters['command'] = FINALIZE
        parameters['media_id'] = media_id
        r = self.post_media(parameters)
        print r.text
        
    def upload_photo(self, photo):
        # Max Upload size is 5MB
        small_photo, file_size = compress_image(photo)
        media_id = self.media_init(file_size)
        self.media_append(media_id, small_photo)
        self.media_finalize(media_id)
        self.post_status(media_id)

        
if __name__ == '__main__':
    flickr_bot = RestApi(FLICKR)
    twitter_bot = TwitterRestApi(TWITTER)
    bots = [flickr_bot, twitter_bot]
    for bot in bots:
        bot.authorize_user()

    while True:
        try:
            process_photos(bots, SRC, DST)
        except:
            print "Could Not Process Photos. Try Again."
        time.sleep(1)
