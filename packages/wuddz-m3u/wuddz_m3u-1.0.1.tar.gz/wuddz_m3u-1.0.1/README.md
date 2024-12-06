<h1 align="center">Wuddz M3U Checker/Downloader/Maker/Parser & XPSF To M3U Converter</h1>

## Description
 - A Cool & Simple Python M3U Playlist Checker/Downloader/Maker/Parser & XPSF To M3U Playlist Converter.

## Prerequisites
 - Python : 3.7

## Installation
Install using [PyPI](https://pypi.org/project/wuddz-m3u):
```
pip install wuddz-m3u
```
Install locally by cloning or downloading and extracting the repo, then cd into 'dist' directory and execute:
```
pip install wuddz_m3u-1.0.1.tar.gz
```
Then to run it, execute the following in the terminal:
```
wudz-m3u
```

### Usage
Parse .m3u Playlist(s) In 'C:\TV' Directory For Billions Season 5 & Create Playlist(s):
```
wudz-m3u -f "C:\TV" -t "Billions S05" -p
```
Parse .m3u Playlist(s) In 'C:\TV' Directory For Group Title Series & Create Playlist(s):
```
wudz-m3u -f "C:\TV" -g "Series" -p
```
Create .m3u Playlist With Titles & Links In Specified Files (*Specify Titles,Links In That Order):
```
wudz-m3u -f "C:\Titles.txt,C:\Links.txt" -c
```
Create .m3u Playlist Series Title 'House' Starting From Season 2 Episode 1, Episodes Per Season 10 With Links In Links.txt File.
```
wudz-m3u -f "C:\Links.txt" -t House -s 2 -a 10
```
Convert 'file.xpsf' XPSF To 'file.m3u' M3U Playlist In C:\Users Directory
```
wudz-m3u -f "C:\file.xpsf" -v -o C:\Users
```
Check & Download Legit M3u Urls From 'valid.txt' To Output Folder As Local Playlist Files & Legit Urls In 'm3u_valid.txt'.
```
wudz-m3u -l "C:\valid.txt" -d
```

### Library
Convert '/home/ubuntu/Documents/file.xpsf' XPSF Playlist To M3U Playlist In '/home/ubuntu/Desktop' Directory.
```
>>> from wuddz_m3u import m3u
>>> m = m3u.M3U()
>>> m.__convert('/home/ubuntu/Documents/file.xpsf', '/home/ubuntu/Desktop')
```
Parse M3U Playlist File '/home/ubuntu/Documents/sub.m3u' For Series House Of Cards & Create Playlist In '/home/ubuntu/Desktop/TV' Directory.
```
>>> from wuddz_m3u import m3u
>>> playlist = '/home/ubuntu/Documents/sub.m3u'
>>> output = '/home/ubuntu/Desktop/TV'
>>> title = 'House Of Cards'
>>> m = m3u.M3U()
>>> m.__search(playlist,output,t=title)
```

## Contact Info:
 - Email:     wuddz_devs@protonmail.com
 - Github:    https://github.com/wuddz-devs
 - Telegram:  https://t.me/wuddz_devs
 - Youtube:   https://youtube.com/@wuddz-devs
 - Reddit:    https://reddit.com/user/wuddz-devs

### Buy Me A Coffee!!
![Alt Text](https://raw.githubusercontent.com/wuddz-devs/wuddz-devs/main/assets/eth.png)
 - ERC20:    0xbF4d5309Bc633d95B6a8fe60E6AF490F11ed2Dd1

![Alt Text](https://raw.githubusercontent.com/wuddz-devs/wuddz-devs/main/assets/btc.png)
 - BTC:      bc1qa7ssx0e4l6lytqawrnceu6hf5990x4r2uwuead

![Alt Text](https://raw.githubusercontent.com/wuddz-devs/wuddz-devs/main/assets/ltc.png)
 - LTC:      LdbcFiQVUMTfc9eJdc5Gw2nZgyo6WjKCj7

![Alt Text](https://raw.githubusercontent.com/wuddz-devs/wuddz-devs/main/assets/doge.png)
 - DOGE:     DFwLwtcam7n2JreSpq1r2rtkA48Vos5Hgm

![Alt Text](https://raw.githubusercontent.com/wuddz-devs/wuddz-devs/main/assets/tron.png)
 - TRON:     TY6e3dWGpqyn2wUgnA5q63c88PJzfDmQAD

#### Enjoy my awesome creativity!!
#### Peace & Love Always!!
