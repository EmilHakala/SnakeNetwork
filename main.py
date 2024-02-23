import pygame
import sys
import random
import math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont("monospace", 20)
WHITE = (255,255,255)

dt = 0
direction=1
last_dir=0
size=5
trail=[]
apple_x=0
apple_y=0
new=1
speed=600
player_radius = 20
score=0
bscore=0
dgreen=[29,172,19]
to_wall_x_rep = 0
to_wall_y_rep = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

#Neural network part:
weight=[]
neurons=50
bias=1
lr=1
for i in range(1, 1000):
	weight.append(random.randint(0,10))
print(weight)

def machine_input(to_wall_x,to_wall_y,d,dr,li):
	if (li==None):
		li=5

	itr=to_wall_x*weight[1]+to_wall_y*weight[2]+bias*weight[4] +li*weight[37]
	itl=to_wall_x*weight[5]+to_wall_y*weight[6]+bias*weight[8] +li*weight[38]
	itu=to_wall_x*weight[9]+to_wall_y*weight[10]+bias*weight[12] +li*weight[39]
	itd=to_wall_x*weight[13]+to_wall_y*weight[14]+bias*weight[16] +li*weight[40]
	tr=itr*weight[17]+itl*weight[18]+itu*weight[19]+itd*weight[20]+bias*weight[33]
	tl=itr*weight[21]+itl*weight[22]+itu*weight[23]+itd*weight[24]+bias*weight[34]
	tu=itr*weight[25]+itl*weight[26]+itu*weight[27]+itd*weight[28]+bias*weight[35]
	td=itr*weight[29]+itl*weight[30]+itu*weight[31]+itd*weight[32]+bias*weight[36]
	print(to_wall_x, to_wall_y)
	print("last", dr)
	if (d==1):
		if (dr==0 or dr==1):
			print("side_x")
			weight[9] += to_wall_x*lr
			weight[10] += to_wall_y*lr
			#weight[11] += r*lr
			weight[12] += bias*lr
			weight[13] += to_wall_x*lr
			weight[14] += to_wall_y*lr
			#weight[15] += r*lr
			weight[16] += bias*lr
			weight[37] += li*lr
			weight[38] += li*lr
			weight[39] += li*lr
			weight[40] += li*lr
			weight[25] += itr*lr
			weight[26] += itl*lr
			weight[27] += itu*lr
			weight[28] += itd*lr
			weight[35] += bias*lr
			weight[29] += itr*lr
			weight[30] += itl*lr
			weight[31] += itu*lr
			weight[32] += itd*lr
			weight[36] += bias*lr

		if (dr==2 or dr ==3):
			print("side y")
			weight[1] += to_wall_x*lr
			weight[2] += to_wall_y*lr
			#weight[3] += r*lr
			weight[4] += bias*lr
			weight[5] += to_wall_x*lr
			weight[6] += to_wall_y*lr
			#weight[7] += r*lr
			weight[8] += bias*lr

			weight[17] += itr*lr
			weight[18] += itl*lr
			weight[19] += itu*lr
			weight[20] += itd*lr
			weight[33] += bias*lr
			weight[21] += itr*lr
			weight[22] += itl*lr
			weight[23] += itu*lr
			weight[24] += itd*lr
			weight[34] += bias*lr

		for i in range(0,34):
			weight[i] = weight[i] / 100
	print("Network:",tr,tl,td,tu)
	if tr > tl and tr > tu and tr > td:
		return 0
	elif tl > tr and tl > tu and tl > td:
		return 1
	elif td > tl and td > tu and td > tr:
		return 2
	elif tu > tr and tu > td and tu > tl:
		return 3

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")

    #neural network controller


    if (player_pos.x < 300):
    	to_wall_x_rep = 600 - player_pos.x
    elif (player_pos.x >= 300):
    	to_wall_x_rep = player_pos.x
    if (player_pos.y < 300):
    	to_wall_y_rep = 600 - player_pos.y
    elif (player_pos.y >= 300):
    	to_wall_y_rep = player_pos.y
    #print("to death:", to_death_front, to_death_right, to_death_left)


    #direction=machine_input((to_wall_x_rep-300)/300, (to_wall_y_rep-300)/300, 0, last_dir, direction)
    print(direction)


    if (direction==0 and last_dir != 1):
    	player_pos.x += speed * dt
    	last_dir=0
    elif (direction==1 and last_dir != 0):
    	player_pos.x -= speed * dt
    	last_dir=1
    elif (direction==2 and last_dir != 3):
    	player_pos.y += speed * dt
    	last_dir=2
    elif (direction==3 and last_dir != 2):
    	player_pos.y -= speed * dt
    	last_dir=3
    elif (last_dir==0):
    	player_pos.x += speed * dt
    elif (last_dir==1):
    	player_pos.x -= speed * dt
    elif (last_dir==2):
    	player_pos.y += speed * dt
    elif (last_dir==3):
    	player_pos.y -= speed * dt

    trail.append((player_pos.x,player_pos.y))
    trail=trail[-size:]
    if (len(trail) > 1):
    	pygame.draw.lines(screen, dgreen, False, trail, 20)

    pygame.draw.circle(screen, "green", player_pos, 20)

    #print(player_pos.x)
    if (player_pos.x > 600 or player_pos.y > 600 or player_pos.x < 0 or player_pos.y < 0):
    	#machine_input(player_pos.x, player_pos.y, 1, last_dir, last_dir)
    	print("die")
    	player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    	size=5
    	score=0
    if (score>bscore):
    	bscore=score
    
    for trail_point in trail[:-5]:
    	#print(trail_point[0])
    	if (player_pos.x > trail_point[0] -5 and player_pos.x < trail_point[0] +5 and player_pos.y > trail_point[1] -5 and player_pos.y < trail_point[1] +5):
    		print("DIE")
    		player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    		size=5
    		score=0

    if (new==1):
    	apple_x=random.randint(10,590)
    	apple_y=random.randint(10,590)
    	apple_pos=[apple_x,apple_y]
    	new=0
    if (player_pos.x > apple_x + -20 and player_pos.x < apple_x +20):
    	if (player_pos.y > apple_y + -20 and player_pos.y < apple_y +20):
	    	size=size+2
	    	apple_x=random.randint(10,590)
	    	apple_y=random.randint(10,590)
	    	apple_pos=[apple_x,apple_y]
	    	score=score+1
	    	print(score)
    pygame.draw.circle(screen, "red", apple_pos, 10)

    scoretext = font.render("Score: "+str(score), 1, (255,255,255))
    bscoretext = font.render("Best Score: "+str(bscore), 1, (255,255,255))
    screen.blit(scoretext, (5, 10))
    screen.blit(bscoretext, (5, 25))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        direction=3
    if keys[pygame.K_s]:
        direction=2
    if keys[pygame.K_a]:
        direction=1
    if keys[pygame.K_d]:
        direction=0    

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()