## Overview
This tool is used to compare strings between two apks.
The output of the script will be `output.md` which contains 4 sections:
1. Added - list of added keys (language independent)
2. Removed - list of removed keys (language independent)
3. Renamed - list of possibly renamed keys (language independent).
             Key is considered renamed if the same value appears in source apk and target apk, but the key is removed in the target apk. 
             This does not always mean that the key is renamed, but can give helpful hints, hence "possibly renamed".
3. Changed - list of keys for which the value has changed between two versions (checked for each language specified)

## Prerequisites 
* `apktool` must be set up. See: https://ibotpeaches.github.io/Apktool/. You only need to setup the `apktool.jar` file 
and not the wrapper scripts. See https://ibotpeaches.github.io/Apktool/install/ for instructions.

* Python 3.7 must be installed. You can install it using the official `NCA Python Installer`.

## How to use
After you integrate the latest product release, build an apk and compare the previous release against the new apk to see what has changed.

The script takes following arguments as input:
* `sourceApk` - path to the apk that is used as source (base) for comparison
* `targetApk` - path to the apk that is used as target for comparison
* `languages` - languages to compare, excluding the default language of the app e.g. mk, de

Run the script and supply the arguments e.g. 
`python .\compare-strings.py ndb-app-1.22.0-whitelabel-dev.apk ndb-app-1.29.0-dev.apk de mk`