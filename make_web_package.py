import os
import sys

import string
import random

# Run it as such:
# python make_web_package.py <folder> <package.pak>

def token_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

# generate random token
token = token_generator(10)

rootdir = sys.argv[1]
# open output file
dest_package = open(sys.argv[2], "wb")

# cd to the folder so we have relative paths
os.chdir(rootdir)

for root, subdirs, files in os.walk("."):
  for onefile in files:
    path = os.path.join(root, onefile)
    try:
      txt = open(path)
    except:
      # if we can't open the file, then skip it
      continue
    # Write token to mark begining of the file
    dest_package.write("--"+token+"\r\n")

    # Content location header
    dest_package.write("Content-Location: "+ os.path.normpath(path) + "\r\n")

    # Figure out the content type
    content_type = "text/plain"
    if path.endswith(".html") or path.endswith(".htm"):
      content_type = "text/html"
    if path.endswith(".js"):
      content_type = "text/javascript"
    if path.endswith(".png"):
      content_type = "image/png"
    if path.endswith(".jpg"):
      content_type = "image/jpg"
    if path.endswith(".gif"):
      content_type = "image/gif"
    if path.endswith(".svg"):
      content_type = "image/svg"
    if path.endswith(".ogg"):
      content_type = "audio/ogg"
    if path.endswith(".ogg"):
      content_type = "application/octet-stream"
    if path.endswith(".json"):
      content_type = "application/json"
    if path.endswith(".css"):
      content_type = "text/css"
    if path.endswith(".webapp"):
      content_type = "application/x-web-app-manifest+json"
    dest_package.write("Content-Type: "+content_type +"\r\n")
    dest_package.write("\r\n")
    # Write file contents
    dest_package.write(txt.read())

# Write package end line
dest_package.write("--"+token+"--")
