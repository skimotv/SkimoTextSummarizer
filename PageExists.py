import urllib.request,urllib.error
  
def pageExists(page):
  url = 'https://en.wikipedia.org/wiki/' + page
  headers = {}
  headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
  try:
    request = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(request)
  except urllib.error.HTTPError as e:
    return(False)
  else:
   return(True)

print(pageExists('deep_learning'))
print(pageExists('abcefg'))
