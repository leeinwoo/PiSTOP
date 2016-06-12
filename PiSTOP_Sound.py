import pygame, sys, time


def play_sound(length = 1):
    pygame.mixer.init()
    pygame.mixer.music.load("./sound/" + filename + ".mp3")
    pygame.mixer.music.play(length)
    time.sleep(length)
    pygame.mixer.music.stop()

def play_sound4(length = 4):
    pygame.mixer.init()
    pygame.mixer.music.load("./sound/" + filename + ".mp3")
    pygame.mixer.music.play(length)
    time.sleep(length)
    pygame.mixer.music.stop()

def set_filename(fn):
    global filename
    filename = fn
