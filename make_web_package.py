import os
import sys
import subprocess

import string
import random

import json
import hashlib
import base64

import uuid

# Run it as such:
# python make_web_package.py <folder> <package.pak>

def token_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

# generate random token
token = token_generator(10)

if len(sys.argv) <= 1:
    print("usage: python make_web_package.py <app-folder> <package-name>");
    exit(1);

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

def header(path):
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
    content_type = "image/svg+xml"
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

  # Content location header
  ret = "Content-Location: "+ os.path.normpath(path) + "\r\n"
  ret += "Content-Type: "+content_type +"\r\n"
  ret += "\r\n"
  return ret

#calculate hashes
resources = []
for path in paths:
  try:
    txt = open(path)
  except:
    continue
  sha256 = hashlib.sha256()
  sha256.update(header(path))
  sha256.update(txt.read())
  # we don't want the "./" prefix of each path
  resources.append({
    'src': path[2:],
    'integrity': base64.b64encode(sha256.digest())
    })
  txt.close()

new_manifest_path = os.path.join(script_dir, 'manifest.webapp')
# read manifest and add the resource hashes to it
# write to a temporary location so that the signing tool can read it
with open(manifest_path, 'r') as manifest_file, open(new_manifest_path, 'w') as new_manifest:
  manifest_object = json.load(manifest_file)
  manifest_object['moz-resources'] = resources
  if 'package-identifier' not in manifest_object:
      manifest_object['package-identifier'] = str(uuid.uuid4())
  manifest_string = json.dumps(manifest_object, indent=2, separators=(',',': '))
  new_manifest.write(header(manifest_path) + manifest_string)

def write_package(path, txt):
  # Write token to mark begining of the file
  dest_package.write("--"+token+"\r\n")

  dest_package.write(header(path))

  # Write file contents
  dest_package.write(txt)

  dest_package.write("\r\n")

# create_test_files.sh will calculate signatures in testValidSignedManifest/manifest.sig
subprocess.call([os.path.join(script_dir, 'create_test_files.sh'), new_manifest_path])
# subprocess.call(['rm', new_manifest_path])
signature_path = os.path.join(script_dir, 'testValidSignedManifest/manifest.sig');
with open(signature_path, 'r') as signature_file:
  signature = base64.b64encode(signature_file.read())
  dest_package.write('manifest-signature: ' + signature + '\r\n')
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
