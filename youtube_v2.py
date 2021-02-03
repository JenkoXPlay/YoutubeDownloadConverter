from pytube import Playlist, YouTube
from pytube.cli import on_progress
import os, re, glob
from moviepy.editor import *
from tkinter import *

# Fonction pour convertir mp4 en mp3
def convertToMp3(mp4_file, mp3_file):
    videoclip = VideoFileClip(mp4_file)

    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3_file)

    audioclip.close()
    videoclip.close()

# alertError
def alertError(msg):
    alertError = Label(frame, text=msg, fg='red')
    alertError.pack()

# fonction traitement
def telechargement():
    # champs vide ou non
    if urlInput.get() == "":
        alertError("L'URL est vide !")
    elif urlInput.get() == "URL de la vidéo ou playlist Youtube":
        alertError("L'URL Youtube n'est pas bonne !")
    else :
        # L'url est remplie on continue le process
        # On vérifie s'il s'agit d'une playlist ou d'une simple vidéo
        isPlaylist = False
        if re.match(".*(playlist).*", urlInput.get()):
            isPlaylist = True
        
        # On indique qu'il s'agit d'une playlist
        if isPlaylist:
            p = Playlist(urlInput.get())
            pTitle = p.title

        # Création des dossiers
        if isPlaylist:
            if not os.path.exists("Playlists/" + pTitle):
                os.makedirs("Playlists/" + pTitle)
                # convertContent == True donc on converti en mp3 donc création du dossier mp4 et mp3
                if convertContent.get() == 1:
                    if not os.path.exists("Playlists/" + pTitle + "/mp4"):
                        os.makedirs("Playlists/" +  pTitle + "/mp4")
                    if not os.path.exists("Playlists/" +  pTitle + "/mp3"):
                        os.makedirs("Playlists/" +  pTitle + "/mp3")
        else:
            if not os.path.exists("VideoYoutube"):
                os.makedirs("VideoYoutube")
            if not os.path.exists("MusicYoutube"):
                os.makedirs("MusicYoutube")

        # Téléchargement de la playlist
        if isPlaylist:
            for url in p.video_urls:
                try:
                    video = YouTube(url, on_progress_callback=on_progress)
                    # convertContent == True alors on télécharge dans le dossier mp4
                    if convertContent.get() == 1:
                        video.streams.get_highest_resolution().download('./Playlists/' + pTitle + "/mp4")
                    else:
                        video.streams.get_highest_resolution().download('./Playlists/' + pTitle)
                    print("Téléchargement en cours : " + video.title + " -> ")
                except:
                    print("Téléchargement échoue")
            
            alertSuccessDL = Label(frame, text="Téléchargement terminé !", fg='green')
            alertSuccessDL.pack()
            
            #Conversion en mp3
            if convertContent.get() == 1:
                videos = glob.glob("Playlists/" + pTitle + "/mp4/*.mp4")
                for video in videos:
                    video = video.replace(".mp4","")
                    mp4_file = r'./' + video + '.mp4'
                    video = video.replace("mp4","mp3")
                    mp3_file = r'./' + video + '.mp3'

                    convertToMp3(mp4_file, mp3_file)
                
                alertSuccessConvert = Label(frame, text="Conversion terminée !", fg='green')
                alertSuccessConvert.pack()

        else:
            try:
                # Téléchargement de la musique
                music = YouTube(url, on_progress_callback=on_progress)
                music.streams.get_highest_resolution().download('VideoYoutube')
                print("Téléchargement en cours : " + music.title + " -> ")

                # Conversion en mp3
                if convertContent:
                    mp4_file = r'./VideoYoutube/' + music.title + '.mp4'
                    mp3_file = r'./MusicYoutube/' + music.title + '.mp3'
                    convertToMp3(mp4_file, mp3_file)
            except:
                print("Une erreur est survenue !")

# Fenetre
window = Tk()

# Personnalisation de la fenetre
window.title("Youtube Download Converter - YDC | V1.1")
window.geometry("600x200")
window.minsize(600, 200)
window.maxsize(600, 200)

# Creation de la frame
frame = Frame(window)

# Contenu de la fenetre
labelTitle = Label(frame, text="Youtube Download Converter", font=("Courrier", 16))
labelTitle.pack()

# champs input
urlInput = Entry(frame)
urlInput.insert(0, 'URL de la vidéo ou playlist Youtube')
urlInput.pack()

# bouton radio mp4 ou mp3
convertContent = IntVar()
btnMp4 = Radiobutton(frame, text="mp4", variable=convertContent, value=0)
btnMp3 = Radiobutton(frame, text="mp3", variable=convertContent, value=1)
btnMp4.pack()
btnMp4.select()
btnMp3.pack()

# Bouton
btnDownload = Button(frame, text="Téléchargement",  font=("Courrier"), command=telechargement)
btnDownload.pack()

# Ajout de la frame a la fenetre
frame.pack(expand=YES)

# Afficher la fenetre
window.mainloop()