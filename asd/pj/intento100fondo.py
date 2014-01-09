import pygame, sys, random, math
from pygame.locals import *

width=640
height=420

class Milestone(pygame.sprite.Sprite):
    def __init__(self, posx, pj):
        self.posx = posx
        self.distancia = pj.rect.centerx - posx
        
    def update(self,pj):
        self.distancia = pj.rect.centerx - self.posx

class Burbuja(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('burbuja1.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.vivo = True
        self.speed = 0.3
        
    def angulo(self, pj):
        return math.degrees(math.acos(((self.rect.centerx * pj.rect.centerx) + (self.rect.centery * pj.rect.centery))/(math.sqrt(self.rect.centerx**2 + self.rect.centery**2) * math.sqrt(pj.rect.centerx**2 + pj.rect.centery**2))))

    def update(self, pj, time, proyectil):
        if self.vivo:
            if self.rect.top <= 0:
                self.rect.top = 0
                self.speed *= -1 
            if self.rect.bottom >= height:
                self.rect.bottom = height
                self.speed *= -1 
            self.rect.centery += self.speed*time
            
            r = random.randint(0,1)
            if r == 1 and proyectil.wait:
                proyectil.wait = False 
             
            if pygame.sprite.collide_rect(pj, self) and pj.attacking:
                self.muerte()
                
    def muerte(self):
        self.vivo = False
        self.image = pygame.image.load('vacio.png')
     
class Proyectil(pygame.sprite.Sprite):
    def __init__(self,burbuja):
        pygame.sprite.Sprite.__init__(self)
        self.wait = True
        self.image = pygame.image.load('vacio.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = burbuja.rect.centerx
        self.rect.centery = burbuja.rect.centery
        self.speed = 0.5
        
    def update(self, pj, time, burbuja, angle, vx, vy):
        if self.wait:
            self.rect.centery = burbuja.rect.centery
        if not self.wait:
            self.image = pygame.image.load('proyectil.png')
            #self.rect.centerx -= self.speed*math.cos(angle)*time
            #self.rect.centery += self.speed*math.sin(angle)*time
            self.rect.centerx += vx*self.speed*time
            self.rect.centery += vy*self.speed*time
            if self.rect.top <= 0 or self.rect.bottom >= height or self.rect.left <= 0 or self.rect.right >= width:
                self.desaparicion(burbuja)
    
    def desaparicion(self, burbuja):
        self.wait = True
        self.image = pygame.image.load("vacio.png")
        self.rect.centery = burbuja.rect.centery
        self.rect.centerx = burbuja.rect.centerx
              
class Slime(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('slime.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.speed = 0.1
        self.vivo = True
        self.right = False
        self.left = False
    
    def update(self, pj, time):
        if self.vivo:
            if pj.rect.centerx - self.rect.centerx > 0:
                self.right = True
                self.left = False
            if pj.rect.centerx - self.rect.centerx < 0:
                self.left = True
                self.right = False
            if self.left:
                self.rect.centerx -= self.speed*time
            if self.right:
                self.rect.centerx += self.speed*time
            if pygame.sprite.collide_rect(pj, self) and pj.attacking:
                self.muerte()
            
    
    def muerte(self):
            self.vivo = False
            self.image = pygame.image.load('vacio.png')
        
class BB(pygame.sprite.Sprite):
    def __init__(self, position):
        self.sheet = pygame.image.load('stk_and_soap_mace.png')
        self.sheet.set_clip(pygame.Rect(341, 10, 69, 67))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.xvel=0
        self.yvel=0
        self.frame = 0

        self.left_states={ 0: (341, 10, 69, 67)}
        self.bu_states={0: (416,10,69,67)}

        
    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]
 
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect


    def update(self, left,bu,right):
        if left:
            self.clip(self.left_states)
            self.xvel=-5
        if bu:
            self.clip(self.bu_states)

        if right:
            self.xvel=5
            self.clip(self.left_states)
        if not (right or left):
            self.xvel=0
        if self.xvel==0 and not bu:
            self.clip(self.left_states[0])
        self.rect.x+=self.xvel   
        self.bu=False    
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        
    def handle_event(self):
        left=bu=right=False
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        while pygame.event.get(): pass
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            game_over = True
        
        if event.type == pygame.KEYDOWN:

            if key[pygame.K_a]:
                left=True
            if key[pygame.K_f]:
                bu=True
            if key[pygame.K_d]:
                right=True

        if event.type == pygame.KEYUP:  
 

            if event.key == pygame.K_a:
                left=False
            if event.key==pygame.K_f:
                bu=False
            if event.key==pygame.K_d:
                right=False
        self.update(left,bu,right)

        
##################################################
      
class PJ(pygame.sprite.Sprite):
    def __init__(self, position):
        self.sheet = pygame.image.load('stk_and_soap_mace.png')
        self.sheet.set_clip(pygame.Rect(6, 52, 30, 50))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.xvel=0
        self.yvel=0
        self.onGround=False
        self.attacking = False
        self.frame = 0
        self.alt=position[1]

        self.right_states={ 0: (6, 52, 30, 50),
                           1: (49, 52, 30, 50),
                           2: (86, 52, 30, 50),
                           3: (123, 52, 35, 50),
                           4: (167, 52, 35, 50),
                           5: (215, 52, 30, 50)}
        self.left_states={ 0: (6, 52, 30, 50),
                           1: (49, 52, 30, 50),
                           2: (86, 52, 30, 50),
                           3: (123, 52, 35, 50),
                           4: (167, 52, 35, 50),
                           5: (215, 52, 30, 50)}
        self.upright_states={ 0: (16, 216, 32, 45),
                              1: (59, 216, 32, 45),
                              2: (103, 216, 32, 45),
                              3: (145, 216, 32, 45)}
        self.attackright_states={0: (24, 372, 43, 53),
                                 #1: (68, 372, 60, 53),
                                 #2: (132, 372, 60, 53),
                                 1: (195, 372, 60, 53),
                                 2: (255, 372, 60, 53)}
        
    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]
 
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect


    def update(self, up,right, left,attack):
        if attack:
            self.clip(self.attackright_states)
            self.attacking = True
        if self.rect.y==self.alt-10:
            self.onGround=True
        if up:
            if self.onGround:
                self.yvel=-30
            else:
                pass
        if right and self.onGround:
            if not attack:
                self.clip(self.right_states)
            self.xvel= 5
            if attack:
                self.clip(self.attackright_states)
        if left and self.onGround:
            self.clip(self.left_states)
            self.xvel= -5
        if not self.onGround:
            
            self.yvel+=5

            if self.yvel<-4:
                self.clip(self.upright_states[0])
            elif self.yvel<4:
                self.clip(self.upright_states[1])
            elif self.yvel<12:
                self.clip(self.upright_states[2])
            elif self.yvel<20:
                self.clip(self.upright_states[3])
            if self.yvel>30:
                self.yvel=30
                
        if not (right or left):
            self.xvel=0
        if self.onGround and self.xvel==0 and not attack:
            self.clip(self.right_states[1])
        self.rect.x+=self.xvel
        self.rect.y+=self.yvel
        self.onGround=False
        if self.rect.y>=self.alt-10:
            self.onGround=True
            self.rect.y=self.alt-10

        self.image = self.sheet.subsurface(self.sheet.get_clip())

        
    def handle_event(self,key):
        right=up=left=attack=False
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        if key[pygame.K_RIGHT]:
            right=True
        if key[pygame.K_UP]:
            up=True
        if key[pygame.K_LEFT]:
            left=True
        if key[pygame.K_k]:
            attack=True

        self.update(up,right,left,attack)
        
class Fondo(pygame.sprite.Sprite):
    def __init__(self,imagen,left,top):
        self.image = pygame.image.load(imagen)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
    
    def mov(self,PJ,keys,time,fondo2):

        if PJ.rect.x >= width/2 and keys[K_RIGHT]:
            self.rect.left -= 0.5 * time
        if self.rect.left < 0 and keys[K_RIGHT] and PJ.rect.right == width/2:
            fondo2.rect.left = self.rect.right

def velocidad(pj, burbuja):
    x1 = pj.rect.centerx - burbuja.rect.centerx
    y1 = pj.rect.centery - burbuja.rect.centery
    norm = math.sqrt(x1**2 + y1**2)
    x2 = x1/norm
    y2 = y1/norm
    return x2, y2

def texto(texto, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font("times.ttf", 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

def main():

    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    player = PJ((0, height-60))
    fondo1=Fondo("fondo1.png",0,0)
    fondo2=Fondo("fondo2.png",width,0)
    fondo3=Fondo("fondo3.png",width*2,0)
    posx, posx_rect = texto(str(player.rect.centerx), width/2, height/2,[0,0,0])
    slime = Slime(width/2, height-30)
    burbuja = Burbuja(width*2/3, height/2)
    proyectil = Proyectil(burbuja)
    angle = 0
    vx = vy = 0
    
    while True:
        
        time=clock.tick(60)
        key=pygame.key.get_pressed()
        posx, posx_rect = texto(str(player.rect.centerx), width/2, height/2,[0,0,0])
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                sys.exit()
        if fondo1.rect.right>=0:
            fondo1.mov(player,key,time,fondo2)
        if fondo1.rect.right<=0:
            fondo1.rect.left=width*2

        if fondo2.rect.right>=0:
            fondo2.mov(player,key,time,fondo3)
        if fondo2.rect.right<=0:
            fondo2.rect.left=width*2

        if fondo3.rect.right>=0:
            fondo3.mov(player,key,time,fondo1)
        if fondo3.rect.right<=0:
            fondo3.rect.left=width*2    
        player.handle_event(key)
        
        if slime.vivo:
            slime.update(player, time)
        if burbuja.vivo:  
            if proyectil.wait:
                angle = burbuja.angulo(player)
                vx, vy = velocidad(player, burbuja)
            burbuja.update(player, time, proyectil)
            proyectil.update(player, time, burbuja, angle, vx, vy)
        player.attacking = False
        
        background=pygame.image.load(fondo).convert()
        screen.blit(background,(0,0))
        screen.blit(fondo1.image,(fondo1.rect.left,fondo1.rect.top))
        screen.blit(fondo2.image,(fondo2.rect.left,fondo2.rect.top))
        screen.blit(fondo3.image,(fondo3.rect.left,fondo3.rect.top))
        screen.blit(slime.image, slime.rect)
        screen.blit(burbuja.image, burbuja.rect)
        screen.blit(proyectil.image, proyectil.rect)
        screen.blit(player.image, player.rect)
        screen.blit(posx, posx_rect)

        pygame.display.flip()
        clock.tick(15)
    return 0

if __name__ == '__main__':
    pygame.init()
    main()
    pass
