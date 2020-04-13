## Overview
This tool is used to compare strings between two apks.
The output of the script will be `output.md` which contains 4 sections:
1. Added - list of added keys (language independent)
2. Removed - list of removed keys (language independent)
3. Renamed - list of possibly renamed keys (language independent).
             Key is considered renamed if the same value appears in source apk and target apk, but the key is removed in the target apk. 
             This does not always mean that the key is renamed, but can give helpful hints, hence "possibly renamed".
3. Changed - list of keys for which the value has changed between two versions (checked for each language specified in the params including the default language which is in `res/values`)

## Prerequisites 
* Python 3.7 must be installed.

## How to use
Take two versions of an apk and see what has changed between two versions e.g. what is new in the latest release.

The script takes following arguments as input:
* `sourceApk` - path to the apk that is used as source (base) for comparison
* `targetApk` - path to the apk that is used as target for comparison
* `languages` - languages to compare e.g. mk, de. Default language is always compared.

Run the script and supply the arguments e.g. 
`python .\apk-strings-diff.py release-1.0.0.apk release-1.1.0.apk de mk`
