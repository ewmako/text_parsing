import urllib

with open("sejm.html", "r") as myfile:
  filecontents=myfile.read().replace("\n", "")

# get urls
urls = []
while True:
  ksiazka_idx = filecontents.find(".pdf")
  if ksiazka_idx == -1:
    break
  http_idx = filecontents.rfind("http",0, ksiazka_idx)
  urls.append(filecontents[http_idx:ksiazka_idx+11])
  filecontents = filecontents[ksiazka_idx+11:]

# download files
for url in urls:
  slash_idx = url.rfind("/")
  filename = url[slash_idx+1:]
  urllib.urlretrieve(url, filename)
