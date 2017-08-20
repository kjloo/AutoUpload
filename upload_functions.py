import urlparse
import os
import StringIO

from PIL import Image

def parse_query_string(url):
    query = urlparse.parse_qs(urlparse.urlparse(url).query)
    return dict((key, value[0]) for key, value in query.iteritems())

def process_photos(bots, src, dst):
    for filename in os.listdir(src):
        if not filename.endswith(".JPG"):
            continue
        for bot in bots:
            bot.upload_photo(os.path.join(src, filename))
        move_photo(filename, src, dst)

def move_photo(filename, src, dst):
    src_file = os.path.join(src, filename)
    dst_file = os.path.join(dst, filename)
    os.rename(src_file, dst_file)

def int_to_megabytes(value):
    return value * 1024 * 1024

def compress_image(photo):
    # Need to optimize compression
    file_size = os.path.getsize(photo)
    max_size = int_to_megabytes(5)
    output = StringIO.StringIO()
    quality = 100
    while True:
        image = Image.open(photo)
        image.save(output, 'JPEG', quality=quality)
        file_size = len(output.getvalue())
        print file_size
        quality -= 10
        if (file_size < max_size):
            break
        else:
            # Clear output buffer
            output.truncate(0)
    return output, file_size
    
