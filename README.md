# fxos-package-signing-tool
A tool to make and sign packaged apps for Firefox OS.

## Usage
If you are using it for the first time, signingDB doesn't exist yet. You have to run
```
./create_test_files.sh --regenerate-test-certs
```
A certificate will be generated and be used to sign your manifest later.

Then, each time you want to generate a package, run
```
python make_web_package.py <app_folder> <package_name>
```
