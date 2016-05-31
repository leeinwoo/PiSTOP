import pygame, sys, time


def play_sound(filename, length = 1):
    pygame.mixer.init()
    pygame.mixer.music.load("./sound/" + filename + ".mp3")
    pygame.mixer.music.play(length)
    time.sleep(length)
    pygame.mixer.music.stop()
