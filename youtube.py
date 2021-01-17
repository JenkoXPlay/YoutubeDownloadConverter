from pytube import Playlist, YouTube
from pytube.cli import on_progress
import os, re, glob
from moviepy.editor import *

# Fonction pour convertir mp4 en mp3
def convertToMp3(mp4_file, mp3_file):
    videoclip = VideoFileClip(mp4_file)

    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3_file)

    audioclip.close()
    videoclip.close()

print("##== Youtube Download Converter ==##")
print("-- Version 1.0 -- Développé par Maxime Lefebvre --")

# Récupération URL Youtube
url = input("URL Youtube = ")

# On vérifie s'il s'agit d'une playlist ou d'une simple vidéo
isPlaylist = False
if re.match(".*(playlist).*", url):
    isPlaylist = True

# Verification pour la conversion en mp3
goToMp3 = False
convertMp3 = input("Convertir en mp3 ? (o/n) : ")
if convertMp3 == "o":
    goToMp3 = True

# On indique qu'il s'agit d'une playlist
if isPlaylist:
    p = Playlist(url)
    pTitle = p.title

# Création des dossiers
if isPlaylist:
    if not os.path.exists("Playlists/" + pTitle):
        os.makedirs("Playlists/" + pTitle)
        if goToMp3:
            if not os.path.exists("Playlists/" + pTitle + "/mp4"):
                os.makedirs("Playlists/" +  pTitle + "/mp4")
            if not os.path.exists("Playlists/" +  pTitle + "/mp3"):
                os.makedirs("Playlists/" +  pTitle + "/mp3")
else:
    if not os.path.exists("VideoYoutube"):
        os.makedirs("VideoYoutube")
    if not os.path.exists("MusicYoutube"):
        os.makedirs("MusicYoutube")

if isPlaylist:
    # Téléchargement de la playlist
    for url in p.video_urls:
        try:
            video = YouTube(url, on_progress_callback=on_progress)
            if goToMp3:
                video.streams.get_highest_resolution().download('./Playlists/' + pTitle + "/mp4")
            else:
                video.streams.get_highest_resolution().download('./Playlists/' + pTitle)
            print("Téléchargement en cours : " + video.title + " -> ")
        except:
            print("Téléchargement échoue")

    #Conversion en mp3
    if goToMp3:
        videos = glob.glob("Playlists/" + pTitle + "/mp4/*.mp4")
        for video in videos:
            video = video.replace(".mp4","")
            mp4_file = r'./' + video + '.mp4'
            video = video.replace("mp4","mp3")
            mp3_file = r'./' + video + '.mp3'

            convertToMp3(mp4_file, mp3_file)
else:
    try:
        # Téléchargement de la musique
        music = YouTube(url, on_progress_callback=on_progress)
        music.streams.get_highest_resolution().download('VideoYoutube')
        print("Téléchargement en cours : " + music.title + " -> ")

        # Conversion en mp3
        if goToMp3:
            mp4_file = r'./VideoYoutube/' + music.title + '.mp4'
            mp3_file = r'./MusicYoutube/' + music.title + '.mp3'
            convertToMp3(mp4_file, mp3_file)
    except:
        print("Une erreur est survenue !")