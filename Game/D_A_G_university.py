import sys, Menu
import pygame
import Etapa

#############Clase para el launcher###########
class Start:
    
    def __init__(self):
        pass
    def Go(self,ArcadeServiceInterface):
        try:
            return 0
        except Exception:
            return -1
###############################################


def Map(level,stage): #Elige mapa de acuerdo a nivel
    return 'Maps/'+str(level)+'_'+str(stage)+'.txt'
def Fondo(level,stage):
    return 'Images/Others/'+str(level)+'_'+str(stage)+'.png'
def Character(level,stage,personaje):   #Elige Personaje y vestimenta de acuerdo a pj y nivel
    if personaje==3:
        return 'Images/Sticks/'+str(level)+'_'+str(stage)+'.png'
    elif personaje==1:
        return 'Images/Woman/'+str(level)+'_'+str(stage)+'.png'
    elif personaje==2:
        return 'Images/Man/'+str(level)+'_'+str(stage)+'.png'
def menu(resolution, joystick):    #Despliega menu que solo retorna valores de personje (depende de cuantos sean) y muestra creditos y cierra juego
    pygame.mixer.init()
    pygame.mixer.music.load("Music/Menu.mp3")
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode(resolution, 0, 32) 
    menu_items_2 = ('Woman','Man','Stick','Quit')
    pygame.display.set_caption('D_A_G')
    while True:
        Menu.GameMenu(screen,resolution, ((resolution[0])/10)).run(joystick)
        gm2 = Menu.CharMenu(screen, menu_items_2,resolution, ((resolution[0])/10)).run(joystick)
        if gm2<len(menu_items_2):
            break
        elif gm2==len(menu_items_2):
            pygame.quit()
    return int(gm2)

def game(resolution): #Hace correr los codigos
    pygame.init()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    character=menu(resolution, joystick)  #Para seleccionar personaje
    Character(1,1,character)   #para seleccionar vestimenta de personaje
    jugar = True

    lives = [4]
    nivel = 1
    while(jugar):
        if Etapa.Juego(resolution,Character(1,1,character),nivel, lives[0], joystick)==True:
            pygame.time.delay(2000)
            nivel += 1
        else:
            pygame.quit()

def main():
    game((500,500))
if __name__ == '__main__': main()

