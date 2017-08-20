AutoUpload is an API that polls the local disk for photos and uploads them to Twitter and Flickr.

The purpose of the application is to allow for a DIY photo booth in which the photos are automatically uploaded for guests to download.

In addition, photos are posted with a hashtag that allows it to be found by Twitter Slideshow Applications.

To run, the user needs to create Twitter and Flickr API keys and fill in the constants.py file with local configurations.

Known Issues:
 - Twitter terms of service prevents "bots" from uploading. This causes the Twitter account to be locked after Twitter detects that automatic uploads are occurring.