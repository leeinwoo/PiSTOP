import pygame, sys, time


def play_sound(filename, length = 2):
    pygame.mixer.init()
    pygame.mixer.music.load(filename + ".mp3")
    pygame.mixer.music.play(length)
    time.sleep(length)
    pygame.mixer.music.stop()

play_sound("stop")
play_sound("test1")


