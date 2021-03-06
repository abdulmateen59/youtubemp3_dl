from tkinter import Tk
import threading
import time
import youtube_dl
MAX_YOUTUBE_DL_THREADS = 4


root = Tk()
root.withdraw()
linkBuffer = []
semaphor = threading.Semaphore(0)
maxthreads = threading.BoundedSemaphore(MAX_YOUTUBE_DL_THREADS)

def getClipboard(): 		
    x = root.clipboard_get()
    return x

def watch_clipboard():
    print("I started watching the links")	
    new = getClipboard()

    while True:
        old = getClipboard()
        while old == new:
            new = getClipboard()
            time.sleep(0.1)
        if "www.youtube.com" in new:
            save_link(new)
            semaphor.release()


def save_link(link):
    linkBuffer.append(link)


class LinksWatcher:
    def __init__(self):
        self.watcher()

    def watcher(self):
        print("The program is listening to new links ...")
        while True:
            semaphor.acquire()
            maxthreads.acquire()
            link = linkBuffer.pop(0)
            tr = threading.Thread(target=self.download, args=([link]))
            tr.start()
    def download(self, link):
        print("Link detected ...")
        print("O video " + link + " will be downloaded")
        opts = {
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        youtube_dl.YoutubeDL(opts).download([link])
        maxthreads.release()

print("The program will start")
print("Ctrl+C url for the download")


links_watcher  =  threading.Thread(target=LinksWatcher)
links_watcher.start()

watch_clipboard()



