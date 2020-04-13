import argparse
import os
import sys
import re
import io

from pathlib import Path

OUTPUT_FILE_NAME = "output.md"
DEFAULT_LANGUAGE = "default"

def deletePreviousOutput():
  if os.path.exists(OUTPUT_FILE_NAME): 
    os.remove(OUTPUT_FILE_NAME)

def decodeApk(apk):
  decodedApkFolder = Path(apk).stem
  # -f - force overwrite if output already exists
  # -s - don't decode the source code
  # -o - change the output path
  os.system("java -jar apktool.jar d -f -s -o %s %s" % (decodedApkFolder, apk))
  return decodedApkFolder

def readStringsXmlFromDecodedApk(decodedApkFolder, language):
  result = {}

  if language is DEFAULT_LANGUAGE:
    stringsXmlFile = os.path.join(decodedApkFolder, 'res', "values", 'strings.xml')
  else:
    stringsXmlFile = os.path.join(decodedApkFolder, 'res', f"values-{language}", 'strings.xml')

  keyRegex = re.compile('(?<=\").*?(?=\")') # take everything between '" "'
  valueRegex = re.compile('(?<=>).*?(?=<)') # take everything between '> <'

  with io.open(stringsXmlFile, encoding="utf8") as file:
    for line in file:
      keyMatch = re.search(keyRegex, line)
      valueMatch = re.search(valueRegex, line)
      if keyMatch and valueMatch:
        # '#' gets escaped when decoding the apk. here we remove the escape character
        result[line[keyMatch.start():keyMatch.end()]] = line[valueMatch.start():valueMatch.end()].replace(r"\#","#")

  return result

def findRenamedStrings(sourceApkStrings, targetApkStrings):
  renamedStrings = []

  removedKeys = findRemovedStrings(sourceApkStrings, targetApkStrings)

  for key, value in sourceApkStrings.items():
    if value in targetApkStrings.values() and key in removedKeys:
        renamedStrings.append(key) 
  
  return renamedStrings

def findChangedStrings(sourceApkStrings, targetApkStrings):  
  changedStrings = []

  for key, value in sourceApkStrings.items():
    if key in targetApkStrings:
      if targetApkStrings[key] != value:
        changedStrings.append(key)

  return changedStrings

def findAddedStrings(sourceApkStrings, targetApkStrings):
  addedStrings = []

  for key in targetApkStrings:
    if key not in sourceApkStrings:
      addedStrings.append(key)
  
  return addedStrings

def findRemovedStrings(sourceApkStrings, targetApkStrings):
  removedStrings = []

  for key in sourceApkStrings:
    if key not in targetApkStrings:
      removedStrings.append(key) 

  return removedStrings

def compareStringsAndWriteOutput(decodedSourceApkFolder, decodedTargetApkFolder, languages):
  sourceApkDefaultStrings = readStringsXmlFromDecodedApk(decodedSourceApkFolder, DEFAULT_LANGUAGE)
  targetApkDefaultStrings = readStringsXmlFromDecodedApk(decodedTargetApkFolder, DEFAULT_LANGUAGE)

  with io.open(OUTPUT_FILE_NAME, "a", encoding="utf8") as output:
    print("Checking for added strings...")
    output.write("## Added\n")
    for string in findAddedStrings(sourceApkDefaultStrings, targetApkDefaultStrings):
      output.write(f"* {string}\n")

    print("Checking for removed strings...")
    output.write("\n## Removed\n")
    for string in findRemovedStrings(sourceApkDefaultStrings, targetApkDefaultStrings):
      output.write(f"* {string}\n")

    print("Checking for changed keys...")
    output.write("\n## Possibly Renamed\n")
    for string in findRenamedStrings(sourceApkDefaultStrings, targetApkDefaultStrings):
      output.write(f"* {string}\n")

    print("Checking for changed values...")
    output.write("\n## Changed\n")
    output.write(f"Language|Key|{decodedSourceApkFolder}|{decodedTargetApkFolder}\n")
    output.write("---|---|---|---\n")

    for language in languages:
      print(f"Comparing language '{language}'...")

      sourceApkStrings = readStringsXmlFromDecodedApk(decodedSourceApkFolder, language)
      targetApkStrings = readStringsXmlFromDecodedApk(decodedTargetApkFolder, language)
      
      for string in findChangedStrings(sourceApkStrings, targetApkStrings):
        output.write(f"{language}|`{string}`|{sourceApkStrings[string]}|{targetApkStrings[string]}\n")
  
#############

parser = argparse.ArgumentParser()
parser.add_argument('sourceApk', help='apk to use as the base for comparison', metavar='FILE')
parser.add_argument('targetApk', help='apk to compare against', metavar='FILE')
parser.add_argument('languages', help='list of languages to compare except for the default language e.g. de, mk. leave empty for default language only', nargs='*')

args = parser.parse_args()
args.languages.insert(0, DEFAULT_LANGUAGE) # always compare default language which is in 'res/values'

deletePreviousOutput()

decodedSourceApkFolder = decodeApk(args.sourceApk)
decodedTargetApkFolder = decodeApk(args.targetApk)

compareStringsAndWriteOutput(decodedSourceApkFolder, decodedTargetApkFolder, args.languages)