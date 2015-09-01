# fxos-package-signing-tool
A tool to make and sign packaged apps for Firefox OS.

##Setup
Clone the scripts:
```
git clone https://github.com/johnathan79717/fxos-package-signing-tool.git
```
Create certificates and database:
```
cd fxos-package-signing-tool
./create_test_files.sh --regenerate-test-certs
```

## Usage
Each time you want to generate a package, run
```
python make_web_package.py <app_folder> <package_name>
```
