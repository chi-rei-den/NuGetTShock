import urllib.request
import json
import zipfile
import os
import shutil

urllib.request.urlretrieve("https://api.github.com/repos/Pryaxis/TShock/releases", "gh.json")
lj = json.loads(open("gh.json", encoding="utf-8").read())
url = lj[0]["assets"][0]["browser_download_url"]
urllib.request.urlretrieve(url, "tshock.zip")
with zipfile.ZipFile("tshock.zip", 'r') as zip_ref:
    zip_ref.extractall("target")

os.mkdir("binary")
excludes = ["Newtonsoft.Json.dll", "MySql.Data.dll", "BCrypt.Net.dll", "sqlite3.dll"]

for subdir, dirs, files in os.walk("target"):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith(".exe") or filepath.endswith(".dll"):
            if file not in excludes:
                shutil.copy(filepath, "binary" + os.sep + file)

nuspec = open("template.nuspec", encoding="utf-8").read().replace("VERSIONPLACEHOLDER", lj[0]["tag_name"]).replace("NAMEPLACEHOLDER", lj[0]["name"])

with open("tshock.nuspec", "w") as f:
    f.write(nuspec)