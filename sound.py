import pygame
import time
 
pygame.init()
#파일 로드
pygame.mixer.music.load('사운드 파일명')
#로드 된 파일 재생
pygame.mixer.music.play()
time.sleep(10)
#사운드 정지
pygame.mixer.music.stop()
