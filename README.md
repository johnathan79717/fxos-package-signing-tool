# fxos-package-signing-tool
A tool to make and sign packaged apps for Firefox OS.

##Setup
###Clone the scripts:
```
git clone https://github.com/johnathan79717/fxos-package-signing-tool.git
```

###Install NSS tools
The scripts will use nss tools and libraries, namely `certutil`, `libplc4.dylib`, and `libmozglue.dylib`. What you need to do depends on your platform.

####Ubuntu
```
sudo apt-get install libnss3-tools
```

####Mac OS X
If you have a build of gecko, then you have the files you need. Do the following to make `certutil` and the dylibs reachable, assuming `~/lib` doesn't exist.

```
export PATH $PATH:<path-to-objdir-gecko>/dist/bin
ln -s <path-to-objdir-gecko>/dist/lib ~/lib
ln -s <path-to-objdir-gecko>/dist/lib/libmozglue.dylib ~/lib
```

####Generate a key pair, and create certificates and signingDB:
```
cd fxos-package-signing-tool
./create_test_files.sh --regenerate-test-certs
```

## Usage
Make sure you have a JSON file named `manifest.webapp` in `<app_folder>`.
Run
```
python make_web_package.py <app_folder> <package_name>
```

The resource hashes will be inserted to the manifest, and the signature will be generated.

Note that this package won't be verified by firefox nightly because the key-pair you generated won't match the one in mozilla-central.
