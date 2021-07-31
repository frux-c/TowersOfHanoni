"""
 *CS1101 or CS1301
 *Instructor: Dr.Urenda
 *Author: Abel Chaka
 *MADE THE GAME FOR FUN TOO :)
"""
import pygame as pg
import os, sys
import random


WIDTH, HEIGHT = 900,500

WIN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Towers of Hanoni")
# LOAD ASSESTS 
BACKGROUND = pg.image.load(os.path.join('Assets','bg.jpg'))

# LOAD FONT 
pg.font.init()
MOVES_COUNT = pg.font.SysFont('comicsans',40)
WINNER = pg.font.SysFont('comicsans',100)

# RGB COLORS
COLOR_RED = (247,17,17)
COLOR_BLUE = (3,102,252)
COLOR_GREEN = (26,255,0)
COLOR_ORANGE = (255,119,0)
COLOR_PURPLE = (195,0,255)
COLOR_GOLD = (184,95,7)
COLOR_PINK  = (212,44,148)
COLOR_GREY = (200,200,200)

class Disk:
	DISK_WIDTH = 35
	DISK_HEIGHT = 30
	def __init__(self,location : tuple, diameter : int, color : tuple):
		self.location = location
		self.diameter = diameter
		self.color = color
		self.click = False
		self.rectangle = pg.Rect(self.location,(self.DISK_WIDTH * self.diameter, self.DISK_HEIGHT))
		self.image = pg.Surface(self.rectangle.size).convert()
		self.image.fill(color)

	def smallerThan(self,disk):
		return self.diameter < disk.diameter

	def getCenter(self):
		return self.rectangle.center

	def setCenter(self, center):
		self.rectangle.center = center

	def draw(self, WIN):
		if self.click:
			self.rectangle.center = pg.mouse.get_pos()
		WIN.blit(self.image,self.rectangle)

class Towers:
	DISK_HEIGHT = 30
	HEIGHT = 350
	WIDTH = 30
	TOWER_SPACING = 300 # px 
	STARTING_POS = (TOWER_SPACING // 2) - WIDTH
	def __init__(self,disks):
		self.disks = disks+1 if disks < 7 else 7
		self.towerA = []
		self.towerB = []
		self.towerC = []
		self.TOWER_A = pg.Rect((self.STARTING_POS,HEIGHT-self.HEIGHT),(self.WIDTH,self.HEIGHT))
		self.TOWER_B = pg.Rect((self.STARTING_POS + self.TOWER_SPACING,HEIGHT-self.HEIGHT),(self.WIDTH,self.HEIGHT))
		self.TOWER_C = pg.Rect((self.STARTING_POS + self.TOWER_SPACING * 2, HEIGHT-self.HEIGHT), (self.WIDTH,self.HEIGHT))
		self.imageA = pg.Surface(self.TOWER_A.size).convert()
		self.imageB = pg.Surface(self.TOWER_B.size).convert()
		self.imageC = pg.Surface(self.TOWER_C.size).convert()
		self.selected_disk = None
		self.starting_tower = None
		self.starting_tower_list = None
		self.STC = None
		self.moves = 0

		self.fill_tower()

	def fill_tower(self):
		rand_tower = random.randint(1,3)
		colors = [COLOR_RED,COLOR_BLUE,COLOR_GREEN,COLOR_ORANGE,COLOR_PURPLE,COLOR_GOLD,COLOR_PINK]
		self.starting_tower = random.choices([self.TOWER_A,self.TOWER_B,self.TOWER_C],k=1)[0]
		if self.starting_tower == self.TOWER_A:
			self.towerA = [Disk((0,0),i,(colors[i-1])) for i in range(len(colors[:self.disks]),1,-1)]
			self.starting_tower_list = self.towerA.copy()
			self.STC = self.towerA

		elif self.starting_tower == self.TOWER_B:
			self.towerB = [Disk((0,0),i,(colors[i-1])) for i in range(len(colors[:self.disks]),1,-1)]
			self.starting_tower_list = self.towerB.copy()
			self.STC = self.towerB

		elif self.starting_tower == self.TOWER_C:
			self.towerC = [Disk((0,0),i,(colors[i-1])) for i in range(len(colors[:self.disks]),1,-1)]
			self.starting_tower_list = self.towerC.copy()
			self.STC = self.towerC

		for spacing,disk in enumerate(max(self.towerA,self.towerB,self.towerC),start=1):
			disk.setCenter((self.starting_tower.centerx,HEIGHT-(spacing * self.DISK_HEIGHT)))
	def allign_disks(self):
		for spacing, disk in enumerate(self.towerA,start=1):
			if not disk.click:
				disk.setCenter((self.TOWER_A.centerx,HEIGHT-(spacing * self.DISK_HEIGHT)))
		for spacing,disk in enumerate(self.towerB,start=1):
			if not disk.click:
				disk.setCenter((self.TOWER_B.centerx,HEIGHT-(spacing * self.DISK_HEIGHT)))
		for spacing,disk in enumerate(self.towerC,start=1):
			if not disk.click:
				disk.setCenter((self.TOWER_C.centerx,HEIGHT-(spacing * self.DISK_HEIGHT)))

	def check_move(self):
		for disk in self.towerA:
			if not disk.click:
				# TOWER A -> TOWER A
				if disk.getCenter()[0] <= 300:
					pass
				# TOWER A -> TOWER B
				elif disk.getCenter()[0] > 300 and disk.getCenter()[0] <= 600:
					if len(self.towerB) == 0:
						temp = self.towerA[-1]
						self.towerA.pop(-1)
						self.towerB.append(temp)
						self.moves += 1
					else:
						if disk.smallerThan(self.towerB[-1]):
							temp = self.towerA[-1]
							self.towerA.pop(-1)
							self.towerB.append(temp)
							self.moves += 1
				# TOWER A -> TOWER C
				elif disk.getCenter()[0] > 600 and disk.getCenter()[0] <= 900:
					if len(self.towerC) == 0:
						temp = self.towerA[-1]
						self.towerA.pop(-1)
						self.towerC.append(temp)
						self.moves += 1
					else:
						if disk.smallerThan(self.towerC[-1]):
							temp = self.towerA[-1]
							self.towerA.pop(-1)
							self.towerC.append(temp)
							self.moves += 1

		for disk in self.towerB:
			if not disk.click:
				# TOWER B -> TOWER A
				if disk.getCenter()[0] <= 300:
					if len(self.towerA) == 0:
						temp = self.towerB[-1]
						self.towerB.pop(-1)
						self.towerA.append(temp)
						self.moves += 1
					else:
						if disk.smallerThan(self.towerA[-1]):
							temp = self.towerB[-1]
							self.towerB.pop(-1)
							self.towerA.append(temp)
							self.moves += 1
				# TOWER B -> TOWER B
				elif disk.getCenter()[0] > 300 and disk.getCenter()[0] <= 600:
					pass
				# TOWER B -> TOWER C
				elif disk.getCenter()[0] > 600 and disk.getCenter()[0] <= 900:
					if len(self.towerC) == 0:
						temp = self.towerB[-1]
						self.towerB.pop(-1)
						self.towerC.append(temp)
						self.moves += 1
					else:
						if disk.smallerThan(self.towerC[-1]):
							temp = self.towerB[-1]
							self.towerB.pop(-1)
							self.towerC.append(temp)
							self.moves += 1

		for disk in self.towerC:
			if not disk.click:
				# TOWER C -> TOWER A
				if disk.getCenter()[0] <= 300:
					if len(self.towerA) == 0:
						temp = self.towerC[-1]
						self.towerC.pop(-1)
						self.towerA.append(temp)
						self.moves += 1
					else:
						if disk.smallerThan(self.towerA[-1]):
							temp = self.towerC[-1]
							self.towerC.pop(-1)
							self.towerA.append(temp)
							self.moves += 1
				# TOWER C -> TOWER B
				elif disk.getCenter()[0] > 300 and disk.getCenter()[0] <= 600:
					if len(self.towerB) == 0:
						temp = self.towerC[-1]
						self.towerC.pop(-1)
						self.towerB.append(temp)
						self.moves += 1
					else:
						if disk.smallerThan(self.towerB[-1]):
							temp = self.towerC[-1]
							self.towerC.pop(-1)
							self.towerB.append(temp)
							self.moves += 1
				# TOWER C -> TOWER C
				elif disk.getCenter()[0] > 600 and disk.getCenter()[0] <= 900:
					pass

	def check_mouse(self,event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.pos[0] <= 300:
				if len(self.towerA) != 0:
					if self.towerA[-1].rectangle.collidepoint(event.pos):
						self.selected_disk = self.towerA[-1]
			elif event.pos[0] > 300 and event.pos[0] < 600:
				if len(self.towerB) != 0:
					if self.towerB[-1].rectangle.collidepoint(event.pos):
						self.selected_disk = self.towerB[-1]
			elif event.pos[0] > 600 and event.pos[0] <= 900:
				if len(self.towerC) != 0:
					if self.towerC[-1].rectangle.collidepoint(event.pos):
						self.selected_disk = self.towerC[-1]
			if self.selected_disk is not None:
				self.selected_disk.click = True
		if event.type == pg.MOUSEBUTTONUP:
			if self.selected_disk is not None:
				self.selected_disk.click = False

	def check_win(self):
		for tower in [self.towerA,self.towerB,self.towerC]:
			if tower != self.STC:
				if len(tower) == self.disks-1:
					return True
		return False

	def draw(self,WIN):
		self.imageA.fill(COLOR_GREY)
		self.imageB.fill(COLOR_GREY)
		self.imageC.fill(COLOR_GREY)
		WIN.blit(self.imageA, self.TOWER_A)
		WIN.blit(self.imageB, self.TOWER_B)
		WIN.blit(self.imageC, self.TOWER_C)
		for disk in self.towerA:
			disk.draw(WIN)
		for disk in self.towerB:
			disk.draw(WIN)
		for disk in self.towerC:
			disk.draw(WIN)
		move_text = MOVES_COUNT.render(f"Moves : {self.moves}", 1, COLOR_GREEN)
		WIN.blit(move_text, (10,10))

def main():
	run = True
	clock = pg.time.Clock()
	tower = Towers(10)

	while run:
		clock.tick(240)
		WIN.blit(BACKGROUND, (0,0))
		tower.draw(WIN)
		tower.check_move()
		tower.allign_disks()
		for event in pg.event.get():
			# QUIT WINDOW
			if event.type == pg.QUIT:
				run = False
				pg.quit(); sys.exit()
			tower.check_mouse(event)
		if tower.check_win():
			pg.display.update()
			winner = WINNER.render(f"GAME WON IN {tower.moves} MOVES", 1, COLOR_GREEN)
			WIN.blit(winner, (WIDTH//2 - winner.get_width() // 2,HEIGHT // 2 - winner.get_height() // 2))
			pg.display.update()
			pg.time.delay(5000)
			run = False
			main()
		pg.display.update()
if __name__ == '__main__':
	main()