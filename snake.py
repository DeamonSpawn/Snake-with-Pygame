import pygame
import time
import random
from collections import namedtuple

pygame.init()
exitstatus = False
display_width = 600
display_height = 600
white =(255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
shift_up = -10
shift_down = +10
shift_left = -10
shift_right = +10
largeText = pygame.font.Font('freesansbold.ttf',90)
smallText = pygame.font.Font('freesansbold.ttf',24)
temp = namedtuple('point',['x','y'])
blocks = namedtuple('blocks',['sblock','gblock','nblock'])
mode = namedtuple('mode',['status','reserved'])
def message_display(text,font,x,y):
	textSurface = font.render(text, True, white)
	textRect = textSurface.get_rect()
	textRect.center =(x,y)
	gameDisplay.blit(textSurface,textRect)
	pygame.display.update()
def blockgenerator():
	sblock = temp(random.randrange(0,display_width,10),random.randrange(0,display_width,10))
	gblock = temp(random.randrange(0,display_width,10),random.randrange(0,display_width,10))
	nblock = temp(random.randrange(0,display_width,10),random.randrange(0,display_width,10))
	all_blocks = blocks(sblock,gblock,nblock)
	return all_blocks

def draw_blocks(block,color):
	pygame.draw.rect(gameDisplay,color,(block.x,block.y,10,10), 1)
	pygame.display.update()

def initialdata():
	blocks = blockgenerator()
	current_head = temp((display_width/2 + 10) ,(display_height/2) )
	start_mid = temp((display_width/2) , (display_height/2))
	current_mid = [start_mid] 
	current_tail = temp((display_width/2 - len(current_mid)*10) , (display_height/2) )
	snake_info = mode('normal',[current_head,start_mid,current_tail])
	lastevent_type = "initial"
	lastevent = "idle"
	print("initial")
	print(snake_info.reserved)
	return current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent

def draw_snake(head,mid,tail,snake_info):
	pygame.draw.rect(gameDisplay,yellow,(head.x,head.y,10,10), 1)
	if snake_info.status == 'normal':
		color = white
	if snake_info.status == 'grow':
		color = green
	if snake_info.status == 'shrink':
		color = red
	for midobj in mid:
		pygame.draw.rect(gameDisplay,color,(midobj.x,midobj.y,10,10), 1)
	pygame.draw.rect(gameDisplay,color,(tail.x,tail.y,10,10), 1)
	pygame.display.update()

def rules(event,head,mid,tail,blocks,snake_info):
	direct = namedtuple('move',['x','y'])
	back_up =((mid[0].x == head.x) and (mid[0].y == head.y+shift_up))
	back_down =((mid[0].x == head.x) and (mid[0].y == head.y+shift_down))
	back_right =((mid[0].x == head.x+shift_right) and (mid[0].y == head.y))
	back_left =((mid[0].x == head.x+shift_left) and (mid[0].y == head.y))
	
	direction =direct(0,0)
	tail = snake_info.reserved[len(snake_info.reserved)-2]
	mid = snake_info.reserved[0:len(snake_info.reserved)-2]
	print(event)
	if event.key == pygame.K_UP and not back_up:
		print("pressed up")#
		head = temp((head.x),(head.y + shift_up))
		direction = direct(0,shift_up)
		#define if up is pressed
	elif event.key == pygame.K_DOWN and not back_down:
		print("pressed down")
		head = temp((head.x),(head.y + shift_down)) 
		direction = direct(0,shift_down)
		#define if down is pressed
	elif event.key == pygame.K_LEFT and not back_left:
		print("pressed left")
		print("runing loop == 2")
		head = temp((head.x + shift_left),(head.y))
		direction = direct(shift_left,0)
		#define if left is pressed
	elif event.key == pygame.K_RIGHT and not back_right:
		print("pressed right")
		head = temp((head.x + shift_right),(head.y))
		direction = direct(shift_right,0)
	else:
		if(event.key == pygame.K_RIGHT):
			direction = direct(shift_left,0)
		if(event.key == pygame.K_LEFT):
			direction = direct(shift_right,0)
		if(event.key == pygame.K_UP):
			direction = direct(0,shift_down)
		if(event.key == pygame.K_DOWN):
			direction = direct(0,shift_up)
		head = temp((head.x + direction.x),(head.y + direction.y))
		#prevent slithering back
	snake_info = mode(snake_info.status,[head]+mid+[tail])
	if head.x not in range(0,600) or head.y not in range(0,600) or head in snake_info.reserved[1:]:
		print("GAME OVER")
		gameDisplay.fill(black)
		message_display("GAME OVER",largeText,(display_width/2),(display_height/2))
		time.sleep(2)
		load_game()
	if head == blocks.nblock:
		if snake_info.status == 'grow' or snake_info.status =='normal':
			oldhead = head
			head = temp((head.x + direction.x),(head.y + direction.y))
			mid= [oldhead]+mid
			blocks = blockgenerator()
			snake_info = mode(snake_info.status,[head]+mid+[tail])
		if snake_info.status == 'shrink':
			if len(mid) > 1:
				tail = snake_info.reserved[len(snake_info.reserved)-2]
				mid = snake_info.reserved[1:len(snake_info.reserved)-2]
				head = snake_info.reserved[0]
				snake_info = mode('shrink',[head]+mid+[tail])
			blocks = blockgenerator()
	if head == blocks.sblock:
		if len(mid) > 1:
			tail = snake_info.reserved[len(snake_info.reserved)-2]
			mid = snake_info.reserved[1:len(snake_info.reserved)-2]
			head = snake_info.reserved[0]
			snake_info = mode('shrink',[head]+mid+[tail])
		blocks = blockgenerator()
	if head == blocks.gblock:
			oldhead = head
			head = temp((head.x + direction.x),(head.y + direction.y))
			mid= [oldhead]+mid
			blocks = blockgenerator()
			snake_info = mode('grow',[head]+mid+[tail])
	return head,mid,tail,blocks,snake_info

def get_keyboard_event(eventtype,event,head,mid,tail,blocks,snake_info):
	if eventtype == pygame.KEYDOWN or eventtype == pygame.KEYUP:
		head,mid,tail,blocks,snake_info = rules(event,head,mid,tail,blocks,snake_info)
	print("exit eventhandler")
	return head,mid,tail,blocks,snake_info,eventtype

def end_game():
	pygame.quit()
	quit()

def renderdisplay(head,mid,tail,blocks,snake_info):
	draw_snake(head,mid,tail,snake_info)
	draw_blocks(blocks.sblock,red)
	draw_blocks(blocks.gblock,green)
	draw_blocks(blocks.nblock,blue)
	pygame.event.set_blocked(pygame.MOUSEMOTION)
	pygame.event.set_blocked(pygame.WINDOWEVENT)
def eventhandler(current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent):	
		lastevent = lastevent
		gameDisplay.fill(black)		
		head,mid,tail = current_head,current_mid,current_tail
		#event handler - grabs all events
		for event in pygame.event.get():			
			lastevent = event
			#quiting the game 
			if event.type == pygame.QUIT:
				end_game()
			#keypress events
			if (event.type == pygame.KEYDOWN):
				head,mid,tail,blocks,snake_info,lastevent_type = get_keyboard_event(pygame.KEYDOWN,event,head,mid,tail,blocks,snake_info)
				print(len(mid))
				print("HMT")
				print(head,mid,tail)
				print("RESERVED")
				print(snake_info.reserved)
				# render new frame check flip() as alternative
				renderdisplay(head,mid,tail,blocks,snake_info)
			if (event.type == pygame.KEYUP):
				head,mid,tail,blocks,snake_info,lastevent_type = get_keyboard_event(pygame.KEYUP,event,head,mid,tail,blocks,snake_info)
				print(len(mid))
				print("HMT")
				print(head,mid,tail)
				print("RESERVED")
				print(snake_info.reserved)
			if lastevent_type == 'initial':
				# render new frame check flip() as alternative
				renderdisplay(head,mid,tail,blocks,snake_info)
				# fps
			clock.tick(10)
		return head,mid,tail,blocks,snake_info,lastevent_type,lastevent

def snake_driver(current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent):
	oldevent = lastevent_type
	current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent = eventhandler(current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent)
	newevent = lastevent_type
	if(oldevent != 'initial'):
		if (oldevent == newevent):
			if newevent == pygame.KEYDOWN:
				pass
			if newevent == pygame.KEYUP:
				current_head,current_mid,current_tail,blocks,snake_info,lastevent_type = get_keyboard_event(pygame.KEYUP,lastevent,current_head,current_mid,current_tail,blocks,snake_info)
				renderdisplay(current_head,current_mid,current_tail,blocks,snake_info)
				clock.tick(10)
				current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent = eventhandler(current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent)
	return current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent

def game_loop(current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent):
	while not exitstatus:
		current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent = snake_driver(current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent)		

def frame_generator():
		current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent = initialdata() 
		game_loop(current_head,current_mid,current_tail,blocks,snake_info,lastevent_type,lastevent)

def load_game():
	gameDisplay.fill(black)
	message_display("SNAKE",largeText,(display_width/2),(display_height/2))
	message_display("by DaemonSpawn",smallText,(display_width/2),(display_height/2+45))
	time.sleep(2)
	frame_generator()

gameDisplay = pygame.display.set_mode((display_width,display_height)) 
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
load_game()


