import requests
from bs4 import BeautifulSoup
import re
import os

def main():
  # url = input("Enter a Spotify playlist URL: ")
  # songs = getSongNames(url)
  songs = getSongNames("https://open.spotify.com/playlist/3TyT3HTSB09ptQ42emmprP?si=b38d81e7257f43af")
  links = getYoutubes(songs)
  # print(links)

def getSongNames(url):
  try:
    r = requests.get(url)
  except:
    print("Invalid url")
    exit(1)
  songnames = []
  htmlText = r.text
  soup = BeautifulSoup(htmlText, 'html.parser')
  soups = soup.find_all("li", {"class":"tracklist-row js-track-row tracklist-row--track track-has-preview"})

  # get track info
  for subsoup in soups:
    info = {}
    trackname = subsoup.find("span", {"class":"track-name"}).text
    info['trackname'] = trackname
    duration = subsoup.find("span", {"class":"total-duration"}).text
    info['duration'] = parseTime(duration)
    artists = subsoup.find_all('a')
    artists = "+".join([a.text for a in artists if a['href'][:7] == '/artist'])
    info['artists'] = artists
    songnames.append(info)
  return songnames

def getYoutubes(songs):
  for song in songs:
    # build url
    url = f"http://youtube.com/results?search_query={song['trackname']}+{song['artists']}+audio"
    r = requests.get(url)
    videos = re.findall(r"watch\?v=(\S{11})", r.text)
    for vid in videos:
      url = f"http://youtube.com/watch?v={vid}"
      # r = requests.get(url)
      print(url)
    break

def parseTime(duration):
  min, sec = duration.split(':')
  return float(min) + float(sec) / 60

if __name__ == "__main__":
  main()