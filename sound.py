import pygame
import time
 
pygame.init()
#���� �ε�
pygame.mixer.music.load('���� ���ϸ�')
#�ε� �� ���� ���
pygame.mixer.music.play()
time.sleep(10)
#���� ����
pygame.mixer.music.stop()
