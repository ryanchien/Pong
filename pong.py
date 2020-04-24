import pygame
import sys
import random
import math
from pygame.locals import *
from random import *

#Some pygame stuff
FPS=20
RUNCOUNT=0
COUNT=0
MAX=0
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20
BALLDIM=10
TRAINCOUNT=0
TOTAL=0

BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)

def increment():
	global COUNT
	global TOTAL
	COUNT=COUNT+1
	TOTAL=TOTAL+1

def runPlus():
	global RUNCOUNT
	RUNCOUNT=RUNCOUNT+1


def reset():
	global COUNT
	global MAX
	global TOTAL
	COUNT=0
	MAX=float(float(TOTAL)/float(RUNCOUNT))

#Each paddle on the board
class paddle:
	height=10
	x=0.0
	y=0.0

	def __init__(self,x,y,height):
		self.height=float(height)*float(600)
		self.x=float(x*600)
		self.y=float(y*600)

#Ball is life
class ball:
	ballX=1
	ballY=1
	velX=1
	velY=1
	radius=5

	def __init__(self,x,y,vx,vy):
		self.ballX=x
		self.ballY=y
		self.velX=vx
		self.velY=vy

#What we hope to store to train the pong AI 
class pongState:
	#A=player/wall, B=bot
	paddleA=paddle(1,2,3)
	paddleB=paddle(2,3,4)
	#the coordinates on the 12x12
	ballX=0.0
	ballY=0.0
	#X is 1 or -1
	#Y is 1,0, or -1
	velX=0.0
	velY=0.0
	#1 for bounce, -1 for lose, 0 for other
	reward=0
	#whether the state is terminal

	def __init__(self,wall,bot,x,y,velX,velY,score):
		self.paddleA=wall
		self.paddleB=bot
		#coordinates from method
		self.ballX=findCoords(x,y)[0]
		self.ballY=findCoords(x,y)[1]
		#velocity from method
		self.velX=posNegZero(velX)
		self.velY=posNegZero(velY)
		self.reward=score






#leftover method from the reference
def drawArena():
	global MAX
	global COUNT
	global RUNCOUNT
	DISPLAYSURF.fill((0,0,0))
	resultSurf = BASICFONT.render('CURRENT = %s; AVG = %s; TOTAL RUNS = %s, ' %(COUNT,MAX,RUNCOUNT), True, WHITE)
	resultUI= BASICFONT.render("P:toggle player, B:toggle scripted movement, X:speed up",True,WHITE)
	resultRect = resultSurf.get_rect()
	resultRect.topleft = (20, 0)
	result2=resultUI.get_rect()
	result2.topleft= (20,575)
	DISPLAYSURF.blit(resultSurf, resultRect)
	DISPLAYSURF.blit(resultUI,result2)


	#Draw outline of arena
	#pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    #Draw centre line[]
	#pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2),0),((WINDOWWIDTH/2),WINDOWHEIGHT), (LINETHICKNESS/4))

#0=positive,1=negative,2=zero
def posNegZero(input):
	if(input>0):
		return 0
	elif(input<0):
		return 1
	else:
		return 2

#stateList[x][y][velX][velY][Height][action]
def emptyGrid():
	statGrid=[]
	#x
	for a in range(0,12):
		grid2=[]
		#y
		for b in range(0,12):
			grid3=[]
			#velX, positive=0, negative=1
			for c in range(0,2):
				grid4=[]
				#velY positive=0,negative=1,zero=2
				for d in range(0,3):
					grid5=[]
					#positionY
					for e in range(0,12):
						grid6=[]
						for f in range(0,3):
							grid6.append(0)
						grid5.append(grid6)
					grid4.append(grid5)
				grid3.append(grid4)
			grid2.append(grid3)
		statGrid.append(grid2)
	return statGrid
#Draws the paddle



#Draws the paddl-e



def drawPaddle(paddle):
	#print(paddle.y)
	pygame.draw.rect(DISPLAYSURF, WHITE, ((paddle.x,paddle.y),(10,paddle.height)),0)

#draws the ball on the surface
def drawBall(x,y,rad):
	pygame.draw.circle(DISPLAYSURF,WHITE,(x+5,y+5),rad,0)

#Moves the ball
def moveBall(ball):
	if(math.fabs(ball.velX)>=600):
		
		if(ball.velX<-1):
			ball.velX=-30
		else:
			ball.velX=30

	if(math.fabs(ball.velY)>=600):
		print("Y is 600")
		if(ball.velY<-1):
			ball.velY=-30
		else:
			ball.velY=30
	ball.ballX=ball.ballX+ball.velX
	ball.ballY=ball.ballY+ball.velY
	#print(ball.ballX)

	return ball


#translates the paddle up
def movePlayerUp(paddle):
	if((paddle.y-24)<0):
		paddle.y=0
	else:
		paddle.y=paddle.y-24
	return paddle

def movePlayerUp2(paddle):
	if((paddle.y-12)<0):
		paddle.y=0
	else:
		paddle.y=paddle.y-12
	return paddle

#translates the paddle passed in down
def movePlayerDown(paddle):
	if((paddle.y+paddle.height+24)>=600):
		paddle.y=600-paddle.height
	else:
		paddle.y=paddle.y+24
	return paddle


def movePlayerDown2(paddle):
	if((paddle.y+paddle.height+12)>=600):
		paddle.y=600-paddle.height
	else:
		paddle.y=paddle.y+12
	return paddle


#action=0,1,2 0=still 1=up 2=down
def botMove(paddle,action):
	if(action==1):
		return movePlayerUp(paddle)
	elif(action==2):
		return movePlayerDown(paddle)
	else:
		#no change
		return paddle





#Finds the coordinates of the ball on the imaginary grid of a board
#Anything outside the edge will be in the nearest edge one 0 or 11
def findCoords(ballX,ballY):

	x=int(ballX/50)
	y=int(ballY/50)
	if(x<0):
		x=0
	elif x>11:
		x=11
	if(y<0):
		y=0
	elif y>11:
		y=11
	#print(x,y)
	return (x,y)


#Bouncing check stuff and update ball,paddle,matrix stuff
def checkBallColl(wall,bot,ball,state,defState,utilMatrix,freqGrid):
	#if ball is past the left edge
		#if ball hits the top of the screen	
	#bot takes best movement from current state in matrix
	global TRAINCOUNT
	padheight=findCoords(0,bot.y)[1]
	
	#the current weight values
	weightCheck=utilMatrix[int(state.ballX)][int(state.ballY)][int(state.velX)][int(state.velY)][padheight]
	#current frequencys
	freqCheck=freqGrid[int(state.ballX)][int(state.ballY)][int(state.velX)][int(state.velY)][padheight]
	#get the index of the best action (0,1,2)
	for a in range(0,3):
		if(freqCheck[a]<=5):
			weightCheck[a]=1000






	bestAction=weightCheck.index(max(weightCheck))
	#decrement the value of the best action slightly so other actions will betried
	utilMatrix[int(state.ballX)][int(state.ballY)][int(state.velX)][int(state.velY)][padheight][bestAction]=float(utilMatrix[int(state.ballX)][int(state.ballY)][int(state.velX)][int(state.velY)][padheight][bestAction]-0.1)
	#move the bot paddle
	frequency=1+freqGrid[int(state.ballX)][int(state.ballY)][int(state.velX)][int(state.velY)][padheight][bestAction]
	#print(frequency)


	bot=botMove(bot,bestAction)

	#the value we use to improve matrix
	score=0

	if ball.ballY+5<0:
		ball.velY=-1*ball.velY
		ball.ballY=-1*ball.ballY
	#if ball hits the bottom of the screen
	elif ball.ballY+5>600:
		ball.ballY=1200-ball.ballY
		ball.velY=-1*ball.velY

	#The left guy's paddle, ignore scoring for now
	elif ball.ballX+5<15:
		#Is ball past the top of the left paddle
		if ball.ballY+5>wall.y:
			#is ball above the bottom of the left paddle
			if ball.ballY+5<(wall.y+wall.height+1):
				#Collision
				ball.velX=-1*ball.velX
				ball.ballX=-1*ball.ballX
			#Reset if past the paddle
			else:
				#reset=ball passed
				print("reset from the left under the paddle at "+str(ball.ballX)+" ,"+str(ball.ballY))
				ball.ballX=300
				ball.ballY=300
				ball.velX=0.03*600
				ball.velY=0.01*600

		#If the ball is above the left paddle
		else:
			print("reset from the left above the paddle at "+str(ball.ballX)+" ,"+str(ball.ballY))
			ball.ballX=300
			ball.ballY=300
			ball.velX=0.03*600
			ball.velY=0.01*600
	
	#Right side (Bot) Collision
	elif ball.ballX+5>585:
		#is the ball is past the top of the paddle
		if ball.ballY+5>bot.y:
			#is the ball above the bottom of the paddle
			if ball.ballY+5<(bot.y+bot.height+1):
				#ballX=2*paddleX(590) -ballX
				#print("Collision at "+str(ball.ballX)+" ,"+str(ball.ballY))
				#print("velocity changed to "+str(ball.velX)+" ,"+str(ball.velY))
				ball.ballX=(2*590)-ball.ballX
				#velX=-velX+ U (rand[-0.015,0.015])
				#When multiplying U by 600 to fit our scale, it breaks
				ball.velX=(-1*ball.velX)+float(6*(randint(-15,15)/1000))
				#velY= velY+ V (rand[-.03,.03])
				#Same with this guy for V
				ball.velY=(ball.velY+float(6*(randint(-30,30)/1000)))
				score=1
				increment()
			#if ball is past the top of the paddle but also the bottom
			else:
			#	print("reset from the right under the paddle at "+str(ball.ballX)+" ,"+str(ball.ballY))
				ball.ballX=300
				ball.ballY=300
				ball.velX=0.03*600
				ball.velY=0.01*600
				score=-1
				runPlus()
				reset()
		else:
		#	print("reset from the right above the paddle at "+str(ball.ballX)+" ,"+str(ball.ballY))
			ball.ballX=300
			ball.ballY=300
			ball.velX=0.03*600
			ball.velY=0.01*600
			score=-1
			runPlus()
			reset()

	#Update the score in util matrix for current state, 
	#do the appropriate move
	#make current state the state that you use to update
	

	#the new Height of the y
	padheight2=findCoords(0,bot.y)[1]
	
	#Not a terminal State
	if(score>=0):
		#next state
		newState= pongState(bot,wall,ball.ballX,ball.ballY,ball.velX,ball.velY,score)
	#Terminal State:
	else:	
		newState=defState





	learnRate=float(100/float(frequency+100))
	discountFactor=float(0.5)
	
	#gets the current value of the best one(for readability)
	newVal=utilMatrix[int(state.ballX)][int(state.ballY)][int(state.velX)][int(state.velY)][padheight][bestAction]
	
	#get number of occurences of the state,action pair
	
	#updates the current utlilty matrix
	#max value of the next State
	nextMax=max(utilMatrix[int(newState.ballX)][int(newState.ballY)][int(newState.velX)][int(newState.velY)][padheight2])
	newVal=float(newVal+learnRate*float(score+(discountFactor*nextMax)-newVal))

	#print(newVal)
	TRAINCOUNT=TRAINCOUNT+1
	
	utilMatrix[int(state.ballX)][int(state.ballY)][int(state.velX)][int(state.velY)][padheight][bestAction]=newVal
	state=newState
	#update the frequency counter for the state/action pair
	freqGrid[int(state.ballX)][int(state.ballY)][int(state.velX)][int(state.velY)][padheight][bestAction]=frequency

	return (ball,bot,state,utilMatrix,freqGrid)

def main():
    ballX=300
    ballY=300
    velX=0.03*600
    velY=0.01*600
    pongball=ball(ballX,ballY,velX,velY)

    bot=paddle(.98333333333,0.45,0.2)
   # bot=paddle(.98333333,0,)
    wall=paddle(0,0,1)
    

    #Use a super big multidimensional array to act similar to the example from class
    #idea: 
    #stateList[x coord][y coord][velX][velY][Height][Action]
    #x/y coord is the 0-11 value given from findCoords, which is converted in the state constructor
    #velX/Y: 0:positive 1:negative 2:zero
    #Height is obtained by using findCoords on the paddle to get its Y value on the 0-11 grid
    #Action is 0:stay still, 1 move up, 2 move down
    #stateList[0:11][0:11][0:1][0:2][0:11][0:2]
    pFlag=1
    botFlag=-1
    fpsflag=1
    stateGrid=emptyGrid()
    freqGrid=emptyGrid()
    state=pongState(bot,wall,ballX,ballY,velX,velY,300-bot.height/2)
    currState=state
    #the default height for the bot
    defHeight=findCoords(0,bot.y)[1]
    stateGrid[int(state.ballX)][int(state.ballY)][int(state.velX)][int(state.velY)][defHeight][0]
  #  print(stateGrid[int(state.ballX)][int(state.ballY)][int(state.velX)][int(state.velY)][defHeight])
   # print(stateGrid[int(state.ballX)][int(state.ballY)][int(state.velX)][int(state.velY)])
   # print(stateGrid[int(state.ballX)][int(state.ballY)][int(state.velX)])

    
    pygame.init()
    global DISPLAYSURF
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE=20
    BASICFONT=pygame.font.Font('freesansbold.ttf',BASICFONTSIZE)
    FPSCLOCK=pygame.time.Clock()
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    drawArena()
    global FPS
    while True: #main game loop



		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		drawArena()
		FPS=20
		pressed=pygame.key.get_pressed()
		if pressed[pygame.K_s]:
			wall=movePlayerDown(wall)
		if pressed[pygame.K_w]:
			wall=movePlayerUp(wall)
		if pressed[pygame.K_p]:
			if(pFlag==1):
				wall.y=100
				wall.height=0.2*(600)
				pFlag=0
			else:
				wall.y=0
				wall.height=600
				pFlag=1
		if pressed[pygame.K_b]:
			botFlag=botFlag*-1
		if pressed[pygame.K_x]:
				FPS=10000


		








		drawPaddle(bot)
		drawPaddle(wall)

		
	

		pongball=moveBall(pongball)
		if(botFlag==1):
			if(pongball.ballY<wall.y-12):
				wall=movePlayerUp2(wall)
			elif(pongball.ballY>wall.y+12):
				wall=movePlayerDown2(wall)



		results=checkBallColl(wall,bot,pongball,currState,state,stateGrid,freqGrid)
		pongBall=results[0]
		bot=results[1]
		currState=results[2]
		stateGrid=results[3]
		freqGrid=results[4]
		#print(freqGrid)
		
		
		drawBall(int(pongball.ballX),int(pongball.ballY),10)
		#print(ball.ballX)
		FPSCLOCK.tick(FPS)
		pygame.display.update()






main()


