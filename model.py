# auteur: Ben Kabongo Buzangu

""" Jeu de Domino - Model 
domino: liste de deux entiers entre 0 et 6 inclus
plateau de jeu: listes de dominos déjà posés
main: domino possédés par un joueur
un domino peut être posé sur le plateau ssi une de ses extrêmités
est égale à l'extrêmité du plateau où on le rajoute
un plateau vide accepte n'importe quel domino
les extrêmités d'un domino peuvent changer dans une main, mais
pas dans un plateau """

import random

class Domino:
	""" un domino """
	def __init__(self, ext1, ext2):
		for ext in (ext1, ext2):
			if ext < 0 or ext > 6:
				raise Exception(
					"La valeur de l'extrêmité doit se trouver entre 0 et 6"
					)
		self._domino = [ext1, ext2]

	def __eq__(self, domino):
		""" compare deux dominos """
		s1, s2 = self.get()
		d1, d2 = domino.get()
		if s1 == d1 and s2 == d2:
			return True
		return False

	def __str__(self):
		return "| {} | {} |".format(*self.get())
	
	def getSomme(self):
		""" renvoie la somme des extrêmités """
		return self._domino[0] + self._domino[1]
	
	def get(self):
		""" renvoie les valeurs du domino """
		return self._domino[0], self._domino[1]

	def getLeft(self):
		""" renvoie l'extrêmité gauche """
		return self._domino[0]

	def getRight(self):
		""" renvoie l'extrêmité droite """
		return self._domino[1]

	def reverse(self):
		""" renverse le domino """
		self._domino.reverse()

class Main:
	""" une main de domino """
	def __init__(self, plateau = None):
		self._main = list()
		self._plateau = plateau
	
	def __len__(self):
		return len(self._main)

	def __str__(self):
		return "-| {} |-".format("".join([domino.__str__() for domino in self._main]))
	
	def addDomino(self, domino):
		""" rajoute un domino dans la main """
		self._main.append(domino)

	def delDomino(self, domino):
		""" retire un domino de la liste des dominos """
		self._main.remove(domino)

	def shuffleDominos(self):
		""" mélange les dominos"""
		random.shuffle(self._main)

	def playDominoById(self, id, plateau = None):
		""" tente de jouer un domino via son id 
		La valeur du plateau peut être passée si un plateau par défaut
		n'a pas été attribué à l'objet dès son initialisation"""
		try: domino = self._main[id]
		except IndexError: return None
		else:
			_plateau = None
			if plateau is not None: _plateau = plateau
			else:
				if self._plateau is not None: _plateau = self._plateau
			if _plateau is not None:
				if _plateau.jouer(domino):
					self.delDomino(domino)
					return domino
			return None

	def playDomino(self, domino, plateau = None):
		""" tente de jouer un domino """
		try: id = self._main.index(domino)
		except ValueError: return None
		else: return self.playDominoById(id, plateau)

	def reset(self):
		""" réinitialise la main """
		self._main = list()

	def getDominos(self):
		""" renvoie les dominos d'une amin """
		return list(self._main)

	def getDominoById(self, id):
		""" retourne le domino à l'index id ssi il existe
		None sinon"""
		try: return self._main[id]
		except IndexError: return None

	def getPoints(self):
		""" compte les points de la main """
		points = 0
		for domino in self._main:
			points += domino.getSomme()
		return points
	
	def getBigDomino(self):
		""" retourne le domino ayant la plus grande valeur """
		_domino = None
		_som = 0
		for domino in self._main:
			som = domino.getSomme()
			if som > _som:
				_som = som
				_domino = domino
		return _domino

	def piocheDomino(self):
		""" piocher un domino au hasard et l'efface """
		if len(self._main) == 0:
			return None
		_domino = random.choice(self._main)
		self.delDomino(_domino)
		return _domino
	
class Plateau:
	""" plateau de jeu """
	def __init__(self):
		self._plateau = list()

	def reset(self):
		""" réinitialise le plateau de jeu """
		self._plateau = list()

	def getDominos(self):
		""" renvoie la liste des dominos du plateau """
		return self._plateau

	def __str__(self):
		return "<| {} |>".format("".join([domino.__str__() for domino in self._plateau]))
	
	def isJouableDomino(self, domino):
		""" renvoie True si un domino est jouable, False sinon"""
		# on récupère les extrêmités du domino
		if len(self._plateau) == 0:
			return True

		d_ext1, d_ext2 = domino.get()
		# on recupère les extrêmités du plateau
		# ces extrêmités sont des dominos
		p_d1_ext = self._plateau[0].getLeft()
		p_d2_ext = self._plateau[-1].getRight()

		# on vérifie si les extrêmotés coincident
		for ext in (d_ext1, d_ext2):
			if ext in (p_d1_ext, p_d2_ext):
				return True
		return False

	def jouer(self, domino):
		""" joue un domino 
		renvoie True si la tentative marche,
		False si elle échoue """
		if self.isJouableDomino(domino):
			if len(self._plateau) == 0:
				self._plateau.append(domino)
				return True
			else:
				d_ext1, d_ext2 = domino.get()
				p_d1_ext = self._plateau[0].getLeft()
				p_d2_ext = self._plateau[-1].getRight()
				if d_ext1 == p_d1_ext:
					domino.reverse()
					self._plateau = [domino] + self._plateau
					return True
				elif d_ext1 == p_d2_ext:
					self._plateau.append(domino)
					return True
				elif d_ext2 == p_d1_ext:
					self._plateau = [domino] + self._plateau
					return True
				else:
					if d_ext2 == p_d2_ext:
						domino.reverse()
						self._plateau.append(domino)
						return True
		return False

	def isJouableMain(self, main):
		""" renvoie la liste des dominos jouables d'une main """
		return [domino for domino in main.getDominos() if self.isJouableDomino(domino)]

class Jeu:
	""" jeu principal """
	def __init__(self):
		self._plateau = Plateau()
		self._mainOrdi = Main(self._plateau)
		self._mainJoueur = Main(self._plateau)
		self._pioche = Main() # main de dominos restants lors d'une distribution

	def _newDistribution(self):
		""" renvoie une nouvelle distribution de 28 dominos """
		dominos = list()
		for i in range(28):
			domino = Domino(random.randrange(0, 7), random.randrange(0, 7))
			dominos.append(domino)
		return dominos
		
	def _distribue(self, dominos):
		""" donne 8 dominos au premier joueuur
		8 au second et met le reste dans la pioche """
		dominos = list(dominos)
		self._mainOrdi.reset()
		self._mainJoueur.reset()
		self._pioche.reset()
	
		def _addRandomDomino(main):
			nonlocal dominos
			_domino = random.choice(dominos)
			dominos.remove(_domino)
			main.addDomino(_domino)

		for i in range(8):
			for main in (self._mainJoueur, self._mainOrdi):
				_addRandomDomino(main)

		for _domino in dominos:
			self._pioche.addDomino(_domino)

	def _ordi_getDomino(self):
		""" renvoie un domino au hasard parmi une liste de dominos jouables """
		_dominos = self._plateau.isJouableMain(self._mainOrdi)
		if len(_dominos) > 0: return random.choice(_dominos)
		return None

	def _ordi_getDomino2(self):
		""" renvoie le plus grand domino d'une liste de dominos jouables """
		_dominos = self._plateau.isJouableMain(self._mainOrdi)
		if len(_dominos) > 0:
			# on crée une main, pour réutiliser la méthode getBigDomino
			main = Main()
			for d in _dominos: main.addDomino(d)
			return main.getBigDomino()
		return None

	def _afficheRegles(self):
		""" affiche les règles du jeu """
		print(	"|----------------------------------------------|\n"
				"|------ Domino Games -- Règles de jeu ---------|\n"
				"|----------------------------------------------|\n"
				"| Au début de la partie, le plateau de jeu est |\n"
				"| vide. Vous avez le choix de placer n'importe |\n"
				"| quel domino pour commencer.                  |\n"
				"| Dès lors qu'il y a un domino sur le plateau  |\n"
				"| les dominos à placer sur le plateau doivent  |\n"
				"| avoir au moins une extrêmité commune avec    |\n"
				"| l'une des deux extrêmités du plateau.        |\n"
				"| Sachant que l'extrêmité droite du plateau    |\n"
				"| correspond à l'extrêmité du domino le plus   |\n"
				"| à droite ; pareil pour la gauche.            |\n"
				"| Ne vous inquiétez pas! Dans une partie simple|\n"
				"| les extrêmités d'un domino sont inter-       |\n"
				"| changeables.                                 |\n"
				"| Votre score est calculé en fonction des      |\n"
				"| valeursdes dominos que vous arrivez à placer.|\n"
				"| La partie s'arrête quand il n'y a plus aucun |\n"
				"| domino à piocher et que tous les deux joueurs|\n"
				"| ne peuvent plus jouer.                       |\n"
				"|                                              |\n"
				"| Quand c'est votre tour:                      |\n"
				"| - Tapez 'r' pour afficher les règles de jeu  |\n"
				"| - Pour pouvoir jouer un domino, tapez son    |\n"
				"|   numéro correspondant. S'il est jouable,    |\n"
				"|	 vous gagnez des points. S'il ne l'est pas, |\n"
				"| 	 dans une partie simple, vous pourrez       |\n"
				"| 	 retenter votre chance.                     |\n"
				"| - Si vous êtes dans l'incapacité de jouer,   |\n"
				"| 	 tapez 'p' pour piocher un domino, qui sera |\n"
				"| 	 rajouté à votre main.                      |\n"
				"| - Tapez 'q' pour quitter et abandonner la    |\n"
				"|   partie.                                    |\n"
				"| - Tapez 'i' pour avoir des infos sur l'auteur|\n"
				"|   du jeu.                                    |\n"
				"| Cordialement, Ben Kabongo.                   |\n"
				"|----------------------------------------------|\n"
				)

	def _afficheInfos(self):
		""" affiche les infos sur le concepteur du jeu """
		""" affiche les règles du jeu """
		print(	"|----------------------------------------------|\n"
				"|------ Domino Games -- A propos de moi--------|\n"
				"|----------------------------------------------|\n"
				"| Jeu codé par Ben Kabongo Buzangu             |\n"
				"| Etudiant en L1 Informatique de l'Unicaen     |\n"
				"| 21911598                                     |\n"
				"|----------------------------------------------|\n"
				)

	def newPart(self):
		""" lance une nouvelle partie """
		print(	"-----------------Domino Games----------------\n"
				"----- auteur : Ben Kabongo Buzangu ----------\n"
				"---------------------------------------------")
		print("Tapez 1 pour lancer une nouvelle partie : ")

		play = 0
		try: play = int(input())
		except: pass
		else:
			scoreJoueur = 0
			scoreOrdi 	= 0

			# traitements avant le lancement de la partie
			if isinstance(play, int) and play == 1:
				print("Vous êtes dans une partie facile.\n"
					"Tapez 2 pour jouer une partie difficile : ")
				difficult = input()
				try:
					if int(difficult) == 2:
						difficult = True
						print("--- Niveau de jeu : difficile ---")
				except:
					difficult = False
					print("--- Niveau de jeu : facile ---")

				print("A vos marques")
				input()
				print("Près")
				input()
				print("Go")

				self._plateau.reset()
				dominos = self._newDistribution()
				self._distribue(dominos)

			# lancement de la partie
			while play == 1:
				print("plateau : ", self._plateau)
			
				isPioche = True # on peut piocher
				quit = False	# on quitte la partie
				id = None
				domino = None

				essaie = True 	# on peut essayer
				while essaie:
					print("Votre main : ", self._mainJoueur)
					print(
						"Tapez le numéro de votre domino.\n"
						"Tapez p pour piocher un domino.\n"
						"Tapez r pour afficher les règles de jeu.\n"
						"Tapez i pour afficher les informations sur l'auteur.\n"
						"Tapez q pour quitter la partie :"
						)
					
					scan = input().strip().lower()
					# on pioche	
					if scan == "p": 
						pioche = self._pioche.piocheDomino()
						if pioche is None:
							isPioche = False
							print("Vous ne pouvez plus piocher !")
						else:
							print("Vous avez pioché ", pioche)
							self._mainJoueur.addDomino(pioche)
						essaie = False
					# on quitte la partie	
					elif scan == "q": 
						essaie = False
						quit = True
					# affiche les règles
					elif scan == "r": 
						self._afficheRegles()
						if difficult: essaie = False
					# affiche les infos
					elif scan == "i": 
						self._afficheInfos()
						if difficult: essaie = False
					# on suppose que c'est un entier	
					else:
						try:
							id = int(scan) - 1 
							if id < 0 or id > self._mainJoueur.__len__(): raise ValueError
						except ValueError:
							if difficult: essaie = False
						else: 
							# si le joueur n'a pas pioché
							if id is not None:
								domino = self._mainJoueur.playDominoById(id)
								essaie = False

				# quitter
				if quit:
					print("Tapez 'q' pour confirmer :")
					if input().strip().lower() == "q":
						break

				# si on continue
				if domino is not None:
					print("Vous avez joué :", domino)
					scoreJoueur += domino.getSomme()

				# gestion du choix de l'ordi
				
				# en fonction du niveau de difficulté, on utilise la méthode adéquate
				if not difficult: domino = self._ordi_getDomino()
				else: domino = self._ordi_getDomino2()
				
				# on pioche si l'ordi n'a pas pu trouver un domino jouable
				if domino is None:
					pioche = self._pioche.piocheDomino()
					if pioche is None:
						# On ne peut plus piocher
						isPioche = False
					else:
						# on ajoute la pioche et on passe
						self._mainOrdi.addDomino(pioche)
						print("L'ordinateur a pioché !")
				else:
					# dans le cas où il a un domino jouable
					self._mainOrdi.playDomino(domino)
					print("L'ordinateur a joué :", domino)
					scoreOrdi += domino.getSomme()

				# si on ne peut plus piocher, on quitte la partie
				if not isPioche:
					play = 0
				# si on peut continuer, on mélange les dominos et on repart
				else:
					self._mainOrdi.shuffleDominos()
					self._mainJoueur.shuffleDominos()
					print("Score | Ordi {} - {} Vous".format(scoreOrdi, scoreJoueur))
					print()

				# toutefois, si un des joueurs a placé tous ses dominos, la partie est finie
				if self._mainOrdi.__len__() == 0 or self._mainJoueur.__len__() == 0:
					break

			# la partie est terminée ou l'utilisateur a quitté la partie
			print("Score | Ordi {} - {} Vous".format(scoreOrdi, scoreJoueur))
			if scoreJoueur > scoreOrdi:
				print("Vous avez gagné !")
			elif scoreJoueur < scoreOrdi:
				print("Vous avez perdu !")
			else:
				print("Match nul")

		finally:
			print("Merci d'avoir joué ! Ciao !")

def main():
	Jeu().newPart()

if __name__ == "__main__":
	main()
