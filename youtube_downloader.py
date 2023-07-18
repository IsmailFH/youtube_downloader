import datetime
import re
import time
from time import sleep
from pytube import Playlist,YouTube
import os
import threading
from moviepy.video.io.VideoFileClip import VideoFileClip

class Youtube_downloader:
    def __int__(self):
        pass
    def pointer_file_is_exists(self,pointer_file):
        if not os.path.exists(pointer_file):
            with open(pointer_file, "w") as f:
                f.write("0")

    def read_from_file(self,pointer_file):
        with open(pointer_file, "r") as file:
            pointer = int(file.read())
        return pointer

    def make_valid_python_name(self,name):
        valid_name = ''.join(c if c.isalnum() else '_' for c in name)
        if valid_name[0].isdigit():
            valid_name = '_' + valid_name
        return valid_name

    def download_playlist(self,url,output_path,pointer_file):
        self.pointer_file_is_exists(pointer_file)
        try:
            playlist = Playlist(url)
        except:
            return "check your internet connection"
        path = output_path
        pointer = self.read_from_file(pointer_file)

        for index,video in enumerate(playlist.videos):
            if index < pointer: continue
            while True:
                try:
                    title = video.title
                    break
                except:
                    print("process failed - retry")
                    sleep(0.5)
                    video=playlist.videos[index]
                    continue
            stream = video.streams.filter(progressive=True).order_by("resolution").last()
            """Apply the given filtering criterion.
    
            fps:(optional) The frames per second.
    
            resolution:(optional) Alias to 'res'.
    
            type: (optional) Type part of the ``mime_type`` (e.g.: audio, video).
    
            subtype:(optional) Sub-type part of the ``mime_type`` (e.g.: mp4, mov).
    
            progressive:Excludes adaptive streams (one file contains both audio and video tracks).
    
            adaptive:Excludes progressive streams (audio and video are on separate tracks).
    
            only_audio:Excludes streams with video tracks.
    
            only_video:Excludes streams with audio tracks.
    
            """
            res=re.search(r'res="(\d+p)"', str(stream)).group(1)
            print("resolution: ",res)

            print(video.title, "download started ")
            stream.download(output_path=path)
            print("download completed")
            print("-"*20)

            pointer+=1
            with open(pointer_file, "w") as f:
                f.write(str(pointer))

        print("playlist download completed!")

    def download_video(self,url,output_path):
        video = YouTube(url)
        while True:
            try:
                title = video.title
                break
            except:
                print("process failed - retry")
                sleep(0.5)
                video = YouTube(url)
                continue
        print(video.title)
        stream = video.streams.filter(progressive=True).order_by("resolution").last()
        res = re.search(r'res="(\d+p)"', str(stream)).group(1)
        print("resolution: ",res)
        stream.download(output_path=output_path)
        print("download completed")


    def download_part_of_video(self,url,output_path,start_time, end_time):

        video = YouTube(url)
        while True:
            try:
                title = video.title
                length=video.length
                print("total time for video : ",datetime.timedelta(seconds=length))
                break
            except:
                print("process failed - retry")
                sleep(0.5)
                video = YouTube(url)
                continue
        print(video.title)
        stream = video.streams.filter(progressive=True).order_by("resolution").last()
        res = re.search(r'res="(\d+p)"', str(stream)).group(1)
        print("resolution: ",res)
        filename=self.make_valid_python_name(video.title)+".mp4"
        stream.download(output_path=output_path,filename=filename)
        clip = VideoFileClip(os.path.join(output_path,filename)).subclip(start_time, end_time)
        clip.write_videofile(os.path.join(output_path,filename.split(".")[0]+"segmented.mp4"))
        print("download completed")


    def download_video_as_audio(self,url,output_path):
        video = YouTube(url)
        while True:
            try:
                title = video.title
                break
            except:
                print("process failed - retry")
                sleep(0.5)
                video = YouTube(url)
                continue
        print(video.title)
        stream = video.streams.filter(only_audio=True,type="audio").last()

        stream.download(output_path=output_path,filename=self.make_valid_python_name(video.title)+".mp3")
        print("download completed")


    """traditional way"""
    def Get_playlist_time(self, url):
        start=time.time()
        try:
            playlist = Playlist(url)
        except:print("check your internet connection")

        total_duration = datetime.timedelta()
        for i in range(len(playlist.videos)):
            a=True
            while a:
                try:
                    print(playlist.videos[i].title)
                    duration_in_seconds =playlist.videos[i].length
                    duration = datetime.timedelta(seconds=duration_in_seconds)
                    total_duration += duration
                    a=False
                except:
                    a=True
                    print("error ,try again")

        total_minutes = total_duration.total_seconds() // 60
        # print("total_minutes: ",total_minutes)
        total_hours = total_duration.total_seconds() // 3600
        # print("total_hours: ",total_hours)

        return f"total_minutes: {total_minutes}\ntotal_hours: {total_hours}"

    def Get_video_time(self,playlistx, index, video, result_list):
        a = True
        while a:
            try:
                duration_in_seconds = video.length
                duration = datetime.timedelta(seconds=duration_in_seconds)
                result_list.append(duration)
                a = False
            except:
                video=playlistx.videos[index]
                a = True


    def get_time_for_video_without_thread(self,url):
        video=YouTube(url)
        a = True
        while a:
            try:

                # print(video.title)
                duration_in_seconds = video.length

                duration = datetime.timedelta(seconds=duration_in_seconds)
                return  duration
            except:
                # print("error")
                video = YouTube(url)
                a = True
                # print("error ,try again")

    def Get_playlist_time_threads(self,url):
        try:
            playlistx = Playlist(url)
        except:

            print("check your internet connection")
        threads = []
        result_list = []
        for index,video in enumerate(playlistx.videos):

            t = threading.Thread(target=self.Get_video_time, args=(playlistx, index, video, result_list))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

        total_duration = sum(result_list, datetime.timedelta())

        total_minutes = total_duration.total_seconds() // 60
        total_hours = total_duration.total_seconds() // 3600
        print(f"total_minutes: {total_minutes} , total_hours: {total_hours}")

    def Get_playlist_details(self, url):
        try:
            playlistx = Playlist(url)
        except:
            print("check your internet connection")
        print("time for playlist: ")
        self.Get_playlist_time_threads(playlistx.playlist_url)

        return f"Playlist title:: {playlistx.title}\nPlaylist owner: {playlistx.owner}\n" \
               f"Number of videos in playlist: {playlistx.length}\n Total views: {playlistx.views}"


