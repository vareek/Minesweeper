import pygame
import random

pygame.init()
x_size = 10
y_size = 7
bombCount = 3
dis = pygame.display.set_mode((50*x_size,50*y_size))
pygame.display.update()
pygame.display.set_caption("Minesweeper")
fps = pygame.time.Clock()
font_style = pygame.font.SysFont(None,50)
#Setup

clueColor=[
    (250,30,0),
    (205,190,0),
    (50,250,0),
    (0,30,200),
    (200,30,200),
    (50,30,0),
    (200,230,0),
    (160,50,20)] 

for x in range (x_size):
    for y in range(y_size):
        pygame.draw.rect(dis,(130,200+40*((x+y)%2),150),(50*x, 50*y, 48,48))

flag = []
bomb = []
revealed= []
while len(bomb) < bombCount:
    x= random.randint(0,x_size-1)
    y= random.randint(0,y_size-1)
    if [x,y] not in bomb:
        bomb.append([x,y])
print(bomb)
directions = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]

clue = []
for b in bomb:
    for (dx,dy) in directions:
        clue.append([b[0]+dx,b[1]+dy])
print(f"clue:{clue}")

def reveal(x_pos,y_pos):# Draw the square that got click
    dark = 150-20*((x_pos+y_pos)%2)
    pygame.draw.rect(dis,(dark,dark,dark),(50*x_pos, 50*y_pos, 48,48))
    if [x_pos,y_pos] in bomb:
        pygame.draw.circle(dis,(0,0,0),(25+50*x_pos, 25+50*y_pos), 13)
    elif [x_pos,y_pos] in clue:
        clueText=clue.count([x_pos,y_pos])
        dis.blit(font_style.render(str(clueText),False, clueColor[clueText-1]),(15+50*x_pos, 15+50*y_pos))

def searchBlank(x_pos,y_pos,mem,done):
    directions = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    mem.append([x_pos,y_pos])
    for (dx,dy) in directions:
        if x_pos+dx > x_size-1 or x_pos+dx <0 or y_pos+dy >y_size-1 or y_pos+dy<0:
            pass
        elif ([x_pos+dx,y_pos+dy] not in clue) and ([x_pos+dx,y_pos+dy] not in mem) and ([x_pos+dx,y_pos+dy] not in flag):
            mem.append([x_pos+dx,y_pos+dy])
    done.append([x_pos,y_pos])
    for (x1,y1) in mem:
        if [x1,y1] not in done:
            searchBlank(x1,y1,mem,done)
    return mem

def searchClue(mem):
    done = []
    directions = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    for (x_pos,y_pos) in mem:
        for (dx,dy) in directions:
            if x_pos+dx > x_size-1 or x_pos+dx <0 or y_pos+dy >y_size-1 or y_pos+dy<0:
                pass
            elif ([x_pos+dx,y_pos+dy] in clue) and ([x_pos+dx,y_pos+dy] not in done):
                done.append([x_pos+dx,y_pos+dy])
                reveal(x_pos+dx,y_pos+dy)
                revealed.append([x_pos+dx,y_pos+dy])
#Playing
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_pos = pygame.mouse.get_pos()
            print(start_pos)
            x_pos = int(start_pos[0]/50)
            y_pos = int(start_pos[1]/50)
            print(f"{x_pos},{y_pos}")
            if [x_pos,y_pos] in bomb:
                pygame.draw.circle(dis,(0,0,0),(25+50*x_pos, 25+50*y_pos), 13)
            elif [x_pos,y_pos] in clue:
                dark = 150-20*((x_pos+y_pos)%2)
                pygame.draw.rect(dis,(dark,dark,dark),(50*x_pos, 50*y_pos, 48,48))
                clueText=clue.count([x_pos,y_pos])
                print(clueText)
                dis.blit(font_style.render(str(clueText),False, clueColor[clueText-1]),(15+50*x_pos, 15+50*y_pos))
                revealed.append([x_pos,y_pos])
            else:
                blank = searchBlank(x_pos,y_pos,[],[])
                for (x1,y1) in blank:
                    reveal(x1,y1)
                    revealed.append([x1,y1])
                searchClue(blank)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            start_pos = pygame.mouse.get_pos()
            x_pos = int(start_pos[0]/50)
            y_pos = int(start_pos[1]/50)
            if [x_pos,y_pos] in flag:
                pygame.draw.rect(dis,(130,200+40*((x_pos+y_pos)%2),150),(50*x_pos, 50*y_pos, 48,48))
                flag.remove([x_pos,y_pos])
            elif [x_pos,y_pos] in revealed:
                pass
            else:
                flag.append([x_pos,y_pos])
                pygame.draw.polygon(dis,(250,0,0),[(6+x_pos*50,1+y_pos*50),(41+x_pos*50,17+y_pos*50)
                    ,(7+x_pos*50,34+y_pos*50),(6+x_pos*50,46+y_pos*50)], width=0)
                flag.sort()
                bomb.sort()
                if flag == bomb:
                    print("WIN") 

           

    #color test
    """
    for i in range (1,9):
        dis.blit(font_style.render(str(i),False, clueColor[i-1]),(15+50*i, 15+50*1))
    """              
    pygame.display.update()
    pygame.display.flip()
    fps.tick(60)

pygame.quit()
