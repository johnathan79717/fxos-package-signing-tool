import os
import sys
import subprocess

import string
import random

import json
import hashlib
import base64

# Run it as such:
# python make_web_package.py <folder> <package.pak>

def token_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

# generate random token
token = token_generator(10)

rootdir = sys.argv[1]
# open output file
dest_package = open(sys.argv[2], "wb")

script_dir = os.getcwd()
# cd to the folder so we have relative paths
os.chdir(rootdir)

paths = []
for root, subdirs, files in os.walk("."):
  for onefile in files:
    path = os.path.join(root, onefile)
    paths.append(path)

# the manifest has to be the first resource
try:
  manifest_index = paths.index('./manifest.webapp');
except:
  print("manifest.webapp not found");
  raise
manifest_path = paths[manifest_index]
del paths[manifest_index]

#calculate hashes
resources = []
for path in paths:
  try:
    txt = open(path)
  except:
    continue
  sha256 = hashlib.sha256()
  sha256.update(txt.read())
  # we don't want the "./" prefix of each path
  resources.append({
    'src': path[2:],
    'integrity': base64.b64encode(sha256.digest())
    })
  txt.close()

tmp_manifest_path = 'manifest.webapp.tmp'
# read manifest and add the resource hashes to it
# write to a temporary location so that the signing tool can read it
with open(manifest_path, 'r') as manifest_file, open(tmp_manifest_path, 'w') as tmp_manifest:
  manifest_object = json.load(manifest_file)
  manifest_object['moz-resources'] = resources
  manifest_string = json.dumps(manifest_object, indent=2) + '\r\n'
  tmp_manifest.write(manifest_string)

def write_package(path, txt):
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
  dest_package.write(txt)

# create_test_files.sh will calculate signatures in testValidSignedManifest/manifest.sig
subprocess.call([os.path.join(script_dir, 'create_test_files.sh'), tmp_manifest_path])
subprocess.call(['rm', tmp_manifest_path])
signature_path = os.path.join(script_dir, 'testValidSignedManifest/manifest.sig');
with open(signature_path, 'r') as signature_file:
  signature = base64.b64encode(signature_file.read())
  dest_package.write('manifest_signature: ' + signature + '\r\n')
  write_package(manifest_path, manifest_string)

for path in paths:
  try:
    txt = open(path)
  except:
    # if we can't open the file, then skip it
    continue
  write_package(path, txt.read())

# Write package end line
dest_package.write("--"+token+"--")

dest_package.close()
