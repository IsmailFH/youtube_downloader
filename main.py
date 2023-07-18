from youtube_downloader import *
youtube_downloader=Youtube_downloader()

"""
download_playlist : parm (url,output_path,pointer_file)
download_video : parms (video url , output path)
download_part_of_video:  parms (url,output_path,start_time, end_time)
download_video_as_audio: parms (url,output_path)
playlist_time_calculation_threads: parm (url) 
get_playlist_details: parm (url)
"""


if __name__=="__main__":
    choose=input("what you want \n1-download video\n2-download playlist\n3-download audio from video\n"
                 "4-Get playlist time")
    if int(choose)==1 or choose=="video":
        part_or_all=input("part of video or whole video (1 or 2)")
        if int(part_or_all)==1:
            youtube_downloader.download_part_of_video("", "", (0, 2, 0), (0, 5, 0))
        elif int(part_or_all)==2:
            youtube_downloader.download_video("", "")
        else:
            print("choose valid input")

    elif int(choose)==2 or choose=="playlist":
        youtube_downloader.download_playlist("", "", "")

    elif int(choose)==3 or choose=="audio":
        youtube_downloader.download_video_as_audio("","")

    elif int(choose)==4 or choose=="Get playlist time":
        with_details=input("Do you just want time (1) or with additional details(2)?")
        if int(with_details)==1:
            print(youtube_downloader.Get_playlist_time_threads(""))
        elif int(with_details)==2:
            print(youtube_downloader.Get_playlist_details(""))
        else:
            print("choose valid input")


