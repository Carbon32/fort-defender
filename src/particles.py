# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Game Particles: #

class Particles():
	def __init__(self, display : pygame.Surface):

		# Display

		self.display = display

		# Particles: 

		self.fortParticles = []
		self.enemyParticles = []
		self.groundParticles = []
		self.whiteSmokeParticles = []
		self.blackSmokeParticles = []
		self.towerParticles = []

	def circleSurface(self, radius : int, color : tuple):
		surface = pygame.Surface((radius * 2, radius * 2))
		pygame.draw.circle(surface, color, (radius, radius), radius)
		surface.set_colorkey((0, 0, 0))
		return surface

	def addGameParticle(self, particleType : str, x : int, y : int):
		particleType.lower()
		if(particleType == "fort_smoke"):

			self.fortParticles.append([[x, y], [random.randint(0, 3) / 2 - 1, -0.5], random.randint(16, 24)])

		elif(particleType == "hit"):

			if(self.display.get_height() == 720 or self.display.get_height() == 1080):

				self.enemyParticles.append([[x + 30, y + 30], [random.randint(0, 20) / 10 - 1, -2], random.randint(8, 10)])

			else:

				self.enemyParticles.append([[x + 30, y + 30], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])

		elif(particleType == "small_hit"):

			if(self.display.get_height() == 720 or self.display.get_height() == 1080):

				self.enemyParticles.append([[x + 30, y + 30], [random.randint(0, 10) / 10 - 1, -2], random.randint(2, 3)])

			else:

				self.enemyParticles.append([[x + 30, y + 30], [random.randint(0, 20) / 10 - 1, -2], random.randint(1, 2)])

		elif(particleType == "white_smoke"):

			self.whiteSmokeParticles.append([[x, y], [random.randint(0, 5) / 3 - 1, -1], random.randint(1, 3)])

		elif(particleType == "black_smoke"):

			self.blackSmokeParticles.append([[x, y], [random.randint(0, 5) / 3 - 1, -1], random.randint(3, 6)])

		elif(particleType == "ground_hit"):

			if(self.display.get_height() == 720 or self.display.get_height() == 1080):

				self.groundParticles.append([[x, y], [random.randint(0, 10) / 10 - 1, -2], random.randint(4, 6)])

			else:

				self.groundParticles.append([[x, y], [random.randint(0, 10) / 10 - 1, -2], random.randint(2, 4)])

		else:

			print(f"Cannot find {particleType} in the game particles list. The particle won't be displayed.")

	def drawGameParticles(self, particleType : str):
		if(particleType == "fort_smoke"):

			for particle in self.fortParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (138, 134, 142), [int(particle[0][1]), int(particle[0][0])], int(particle[2]))
				
				if(particle[2] <= 0):

					self.fortParticles.remove(particle)

		elif(particleType == "hit"):

			for particle in self.enemyParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (255, 165, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (255, 165, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):
					self.enemyParticles.remove(particle)

		elif(particleType == "small_hit"):

			for particle in self.enemyParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (255, 165, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (255, 165, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):
					self.enemyParticles.remove(particle)

		elif(particleType == "white_smoke"):

			for particle in self.whiteSmokeParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (128, 128, 128), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (128, 128, 128)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):
					self.whiteSmokeParticles.remove(particle)

		elif(particleType == "black_smoke"):

			for particle in self.blackSmokeParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (0, 0, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (0, 0, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):
					self.blackSmokeParticles.remove(particle)


		elif(particleType == "ground_hit"):

			for particle in self.groundParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (25, 51, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (51, 25, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):

					self.groundParticles.remove(particle)
		else:

			print(f"Cannot find {particleType} in the game particles list. The particle won't be displayed.")

	def updateParticles(self, game):

		if(game.effects):

			self.drawGameParticles("fort_smoke")
			self.drawGameParticles("hit")
			self.drawGameParticles("ground_hit")
			self.drawGameParticles("white_smoke")
			self.drawGameParticles("black_smoke") 