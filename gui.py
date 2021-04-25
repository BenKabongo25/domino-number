# auteur: Ben Kabongo Buzangu
# 15 novembre 2019
# jeu de domino graphique

import tkinter
import model
import random

_font = ("Sergio UI", 10, "bold")

def _setVariableDominoValue(variable, domino):
	""" modifie la valeur d'une variable tkinter en
	lui donnant la valeur du domino """
	variable.set("{} | {}".format(*domino.get()))

class DominoView(tkinter.Label):
	""" version gui de model.Domino
	modélisé par un label dont on détermine la couleur à souhait"""

	def __init__(self, master, domino, couleur = "white"):
		tkinter.Label.__init__(self, master)
		
		self._domino = domino
		self._var = tkinter.StringVar()
		self.update()

		self.config(textvariable = self._var, font = _font, 
			background = couleur, borderwidth = 2, width = 3, height = 1)

	def update(self):
		""" mis à jour de la valeur """
		_setVariableDominoValue(self._var, self._domino)
		
	def reverse(self):
		""" conséquence graphique de la modification des place """
		self._domino.reverse()
		self.update()

class MainView(tkinter.Frame):
	""" équivalent graphique de model.Main """
	def __init__(self, master, main: model.Main):
		tkinter.Frame.__init__(self, master)
		self._main = main

		# id du label domino affiché
		self._id = 0
		self._idVar = tkinter.StringVar(master = self, value = "0 / 0")
		tkinter.Label(self, textvariable = self._idVar, font = _font).pack(side = "left")

		tkinter.Button(self, text = "<<", font = _font, width = 2, height = 1,
			background = "black", foreground = "white", activebackground = "white",
			activeforeground = "black", relief = "flat", overrelief = "flat",
			command = self.setPrevious).pack(side = "left")

		# frame interne
		self._frame = tkinter.Frame(self, width = 4, height = 2, background = "white")
		self._frame.pack(side = "left")

		tkinter.Button(self, text = ">>", font = _font, width = 2, height = 1,
			background = "black", foreground = "white", activebackground = "white",
			activeforeground = "black", relief = "flat", overrelief = "flat",
			command = self.setNext).pack(side = "right")

		# équivalent de self._main en label
		self._mainDominosLabels = list()
		self.update()

	def _set(self, id):
		""" modifie le label affiché par une nouvelle id """
		try: label = self._mainDominosLabels[id]
		except IndexError: pass
		else:
			for c in self._frame.winfo_children(): c.pack_forget()
			self._id = id
			self._idVar.set("{} / {}".format(id + 1, len(self._main)))
			label.pack()

	def setPrevious(self, event = None):
		""" affiche l'item précédent """
		if self._id >= 1: self._set(self._id - 1)
		else: self._set(len(self._main) - 1)

	def setNext(self, event = None):
		""" affiche l'item suivant """
		if self._id < len(self._main): self._set(self._id + 1)
		else: self._set(0)

	def getId(self):
		return self._id

	def update(self):
		""" mis à jour de la main """
		self._mainDominosLabels = list()
		for domino in self._main.getDominos():
			self._mainDominosLabels.append(DominoView(self._frame, domino, "white"))
		if len(self._mainDominosLabels) > 0: self._set(0)
		
class PlateauView(tkinter.Canvas):
	""" équivalent graphique de model.Plateau """
	def __init__(self, master, plateau, couleur):
		tkinter.Canvas.__init__(self, master, background = couleur,
			width = 300, height = 250, relief = "groove")
		self._plateau = plateau

	def update(self):
		""" mis à jour des labels """
		for c in self.winfo_children():
			c.place_forget()

		x = -25
		dominos = self._plateau.getDominos()
		for i in range(len(dominos)):
			colors = ["red", "blue", "orange", "gray", "navy", "white", "olive", "wheat",
			"royal blue", "light blue", "light gray"]
			dominoView = DominoView(self, dominos[i], random.choice(colors))
			y = ((i + 1) // 10) * 30 + 5
			x += 30
			if (i + 1) % 10 == 0: x = 5
			dominoView.place(x = x, y = y)
			
def centrer(window):
	""" méthode de centrage des fenêtres """
	window.update_idletasks()
	w, h = window.winfo_width(), window.winfo_height()
	x = (window.winfo_screenwidth() // 2) - (w // 2)
	y = (window.winfo_screenheight() // 2) - (h // 2)
	window.geometry("{}x{}+{}+{}".format(w, h, x, y))

class Application(tkinter.Tk):

	def __init__(self):
		tkinter.Tk.__init__(self)
		
		self.title("Dominos Games 1.0 - Ben Kabongo")
		self.resizable(False, False)
		self.tk_setPalette(background = "wheat")
		self.minsize(450, 300)
		centrer(self)

		self._initMenu()
		self._initValues()
		self._initContent()
		self._binding()
		
	def _initMenu(self):
		menubar = tkinter.Frame(self, background = "wheat", relief = "groove", height = 30)
		menubar.pack(side = "top", fill = "x")

		partie_menubutton = tkinter.Menubutton(menubar, text = "Partie", underline = 0,
			font = _font, background = "white")
		partie_menubutton.pack(side = "left", padx = 1)
		partie_menu = tkinter.Menu(master = partie_menubutton, tearoff = 0)
		partie_menu.add_command(label = "Partie facile",
								accelerator = "control+n",
								command = self._newPartieFacile,
								font = _font)
		partie_menu.add_command(label = "Partie difficile",
								accelerator = "control+d",
								command = self._newPartieDifficile,
								font = _font)
		partie_menu.add_separator()
		partie_menu.add_command(label = "Quitter",
								accelerator = "control+q",
								command = self.destroy,
								font = _font)
		partie_menubutton.config(menu = partie_menu)

		actions_menubutton = tkinter.Menubutton(menubar, text = "Actions", underline = 0,
			font = _font, background = "white")
		actions_menubutton.pack(side = "left", padx = 1)
		actions_menu = tkinter.Menu(master = actions_menubutton, tearoff = 0)
		actions_menu.add_command(label = "Jouer",
								accelerator = "control+j",
								command = self._joueurPlay,
								font = _font)
		actions_menu.add_command(label = "Piocher",
								accelerator = "control+p",
								command = self._joueurPioche,
								font = _font)
		actions_menubutton.config(menu = actions_menu)

		plus_menubutton = tkinter.Menubutton(menubar, text = "Plus", underline = 0,
			font = _font, background = "white")
		plus_menubutton.pack(side = "left", padx = 1)
		plus_menu = tkinter.Menu(master = plus_menubutton, tearoff = 0)
		plus_menu.add_command(label = "Règles de jeu",
							accelerator = "alt+r",
							command = self._afficheRegles,
							font = _font)
		plus_menu.add_command(label = "Commandes de jeu",
							accelerator = "alt+c",
							command = self._afficheCommandes,
							font = _font)
		plus_menu.add_separator()
		plus_menu.add_command(label = "A propos de moi",
							accelerator = "alt+i",
							command = self._afficheInfos,
							font = _font)
		plus_menubutton.config(menu = plus_menu)

	def _initValues(self):
		self._plateauModel 		= model.Plateau()
		self._mainOrdiModel 	= model.Main(self._plateauModel)
		self._mainJoueurModel 	= model.Main(self._plateauModel)
		self._piocheModel 		= model.Main()
		
		# on peut piocher ?
		self._isPioche = False
		# niveau de difficulté
		self._difficult = 0

	def _initContent(self):
		content = tkinter.Frame(self)
		content.pack(side = "top", fill = "both", expand = True)

		left = tkinter.Frame(content, background = "#222")
		left.pack(side = "left")

		self._plateauView = PlateauView(left, self._plateauModel, "#222")
		self._plateauView.pack(fill = "y")

		right = tkinter.Frame(content)
		right.pack(side = "right", padx = 4, fill = "y")

		self._mainJoueurView = MainView(right, self._mainJoueurModel)
		self._mainJoueurView.pack(pady = 2, padx = 2)

		controls = tkinter.Frame(right)
		controls.pack(pady = 2, padx = 2)

		tkinter.Button(controls, text = "Jouer", font = _font, width = 6, height = 1,
			background = "royal blue", foreground = "white", activebackground = "white",
			activeforeground = "royal blue", relief = "flat", overrelief = "flat",
			command = self._joueurPlay).pack(side = "left", padx = 2)

		tkinter.Button(controls, text = "Piocher", font = _font, width = 6, height = 1,
			background = "green", foreground = "white", activebackground = "white",
			activeforeground = "green", relief = "flat", overrelief = "flat",
			command = self._joueurPioche).pack(side = "left", padx = 2)

		tkinter.Label(right, text = "Scores", font = _font, relief = "groove").pack(padx = 2)

		scores = tkinter.Frame(right, relief = "groove")
		scores.pack(padx = 2)

		tkinter.Label(scores, text = "Ordinateur", 
			font = _font).grid(row = 0, column = 0, sticky = "e")
		self._scoreOrdiVar = tkinter.StringVar(self, value = "0")
		tkinter.Label(scores, textvariable = self._scoreOrdiVar, 
			font = _font, background = "white").grid(row = 0, column  = 1, sticky = "e")
	
		tkinter.Label(scores, text = "Vous",
			font = _font).grid(row = 1, column = 0, sticky = "e")
		self._scoreJoueurVar = tkinter.StringVar(self, value = "0")
		tkinter.Label(scores, textvariable = self._scoreJoueurVar,
			font = _font, background = "white").grid(row = 1, column  = 1, sticky = "e")

		self._statusVar = tkinter.StringVar(self)
		tkinter.Label(self, textvariable = self._statusVar, font = _font,
			relief = "groove").pack()

	def _binding(self):
		self.bind("<Control-n>", self._newPartieFacile) 	# nouvelle partie f
		self.bind("<Control-N>", self._newPartieFacile)
		self.bind("<Control-d>", self._newPartieDifficile) 	# nouvelle partie d
		self.bind("<Control-D>", self._newPartieDifficile)

		self.bind("<Control-q>", self.destroy) 		# quitter
		self.bind("<Control-Q>", self.destroy)
	
		self.bind("<Alt-r>", self._afficheRegles)	# affiche les règles
		self.bind("<Alt-R>", self._afficheRegles)
		self.bind("<Alt-c>", self._afficheCommandes)# affiche les commandes
		self.bind("<Alt-C>", self._afficheCommandes)
		self.bind("<Alt-i>", self._afficheInfos)	# affiche les infos
		self.bind("<Alt-I>", self._afficheInfos)

		self.bind("<Control-j>", self._joueurPlay)	# jouer
		self.bind("<Control-J>", self._joueurPlay)
		self.bind("<Control-p>", self._joueurPioche)# piocher
		self.bind("<Control-P>", self._joueurPioche)
		self.bind("<Key-Left>", self._mainJoueurView.setPrevious)	# domino précédent
		self.bind("<Key-Right>", self._mainJoueurView.setNext)

	# ----------------------------------------- méthodes de contrôle d'état

	def _newDistribution(self):
		""" renvoie une nouvelle distribution de 28 dominos """
		dominos = list()
		for i in range(28):
			domino = model.Domino(random.randrange(0, 7), random.randrange(0, 7))
			dominos.append(domino)
		return dominos
		
	def _distribue(self, dominos):
		""" donne 8 dominos au premier joueuur
		8 au second et met le reste dans la pioche """
		dominos = list(dominos)
		self._plateauModel.reset()
		self._mainOrdiModel.reset()
		self._mainJoueurModel.reset()
		self._piocheModel.reset()
	
		def _addRandomDomino(main):
			nonlocal dominos
			_domino = random.choice(dominos)
			dominos.remove(_domino)
			main.addDomino(_domino)

		for i in range(8):
			for main in (self._mainJoueurModel, self._mainOrdiModel):
				_addRandomDomino(main)

		for _domino in dominos:
			self._piocheModel.addDomino(_domino)
		
		self._plateauView.update()
		self._mainJoueurView.update()

	def _ordi_getDomino(self):
		""" renvoie un domino au hasard parmi une liste de dominos jouables """
		_dominos = self._plateauModel.isJouableMain(self._mainOrdiModel)
		if len(_dominos) > 0: return random.choice(_dominos)
		return None

	def _ordi_getDomino2(self):
		""" renvoie le plus grand domino d'une liste de dominos jouables """
		_dominos = self._plateauModel.isJouableMain(self._mainOrdiModel)
		if len(_dominos) > 0:
			# on crée une main, pour réutiliser la méthode getBigDomino
			main = model.Main()
			for d in _dominos: main.addDomino(d)
			return main.getBigDomino()
		return None

	# ----------------------------------------- méthodes de contrôle graphique

	def _newPartie(self, difficult = 0):
		""" nouvelle partie """
		self._scoreOrdiVar.set(0)
		self._scoreJoueurVar.set(0)
		
		dominos = self._newDistribution()
		self._distribue(dominos)
		self._isPioche = True

		self._difficult = 0
		name = ("facile", "difficile")
		self._statusVar.set("Nouvelle partie {}".format(name[difficult]))

	def _newPartieFacile(self, event = None):
		""" nouvelle partie facile """
		self._newPartie(0)

	def _newPartieDifficile(self, event = None):
		""" nouvelle partie difficile """
		self._newPartie(1)
		
	def destroy(self, event = None):
		""" quitter la partie """
		self._statusVar.set("Ciao !")
		self.after(1000, lambda: tkinter.Tk.destroy(self))

	def _ordiPlay(self):
		""" l'ordinateur tente de placer un domino """
		# en fonction du niveau de difficulté, on utilise la méthode adéquate
		if self._difficult == 0: domino = self._ordi_getDomino()
		else: domino = self._ordi_getDomino2()
		
		# on pioche si l'ordi n'a pas pu trouver un domino jouable
		if domino is None:
			pioche = self._piocheModel.piocheDomino()
			if pioche is None:
				# On ne peut plus piocher
				self._isPioche = False
			else:
				# on ajoute la pioche et on passe
				self._mainOrdiModel.addDomino(pioche)
				self._statusVar.set("L'ordinateur a pioché !")
		else:
			# dans le cas où il a un domino jouable
			self._mainOrdiModel.playDomino(domino)
			self._plateauView.update()
			self._statusVar.set("L'ordinateur a joué {}".format(domino))
			self._scoreOrdiVar.set(int(self._scoreOrdiVar.get()) + domino.getSomme())
		self._check()

	def _joueurPlay(self, event = None):
		""" le joueur tente de placer un domino """
		id = self._mainJoueurView.getId()
		domino = self._mainJoueurModel.playDominoById(id)
		# si la pièce a bel et bien été placée
		if domino:
			self._mainJoueurView.update()
			self._plateauView.update()
			self._statusVar.set("Vous avez joué {}".format(domino))
			self._scoreJoueurVar.set(int(self._scoreJoueurVar.get()) + domino.getSomme())
		else:
			# si la difficulté est faible, le joueur peut recommencer
			# après une tentative ratée
			if self._difficult == 0:
				self._statusVar.set("Choisissez une autre valeur !")
				return
		self._ordiPlay()

	def _joueurPioche(self, event = None):
		""" le joueur pioche un nouveau domino """
		pioche = self._piocheModel.piocheDomino()
		if pioche is None:
			self._isPioche = False
			self._statusVar.set("Vous ne pouvez plus piocher !")
		else:
			self._statusVar.set("Vous avez pioché {}".format(pioche))
			self._mainJoueurModel.addDomino(pioche)
			self._mainJoueurView.update()
		self._ordiPlay()

	def _check(self):
		""" vérifie si la partie est en condition de continuer
		et effectue les modifications nécessaires à chaque tour """
		scoreOrdi 	= self._scoreOrdiVar.get()
		scoreJoueur = self._scoreJoueurVar.get()
		# self._statusVar.set("Scores : Ordi {} - {} Vous".format(scoreOrdi, scoreJoueur))

		finish = False
		
		# si on ne peut plus piocher, on quitte la partie
		if not self._isPioche:
			finish = True
		# si on peut continuer, on mélange les dominos et on repart
		else:
			self._mainOrdiModel.shuffleDominos()
			self._mainJoueurModel.shuffleDominos()
			self._mainJoueurView.update()

		# toutefois, si un des joueurs a placé tous ses dominos, la partie est finie
		if self._mainOrdiModel.__len__() == 0 or self._mainJoueurModel.__len__() == 0:
			finish = True
		
		# la partie est terminée ou l'utilisateur a quitté la partie
		if finish:
			if scoreJoueur > scoreOrdi:
				self._statusVar.set("Vous avez gagné !")
			elif scoreJoueur < scoreOrdi:
				self._statusVar.set("Vous avez perdu !")
			else:
				self._statusVar.set("Match nul !")

	def _affiche(self, title, text):
		""" affichage d'une nouvelle fenêtre """
		top = tkinter.Toplevel(self)
		top.title(title)
		top.transient(self)
		tkinter.Message(top, text = text, background = "#222", foreground = "white",
			font = _font).pack()
		top.resizable(False, False)
		top.grab_set()
		centrer(top)

	def _afficheRegles(self, event = None):
		text = 	("Au début de la partie, le plateau de jeu est\n"
			"vide. Vous avez le choix de placer n'importe\n"
			"quel domino pour commencer.\n"
			"Dès lors qu'il y a un domino sur le plateau\n"
			"les dominos à placer sur le plateau doivent\n"
			"avoir au moins une extrêmité commune avec\n"
			"l'une des deux extrêmités du plateau.\n"
			"Sachant que l'extrêmité droite du plateau\n"
			"correspond à l'extrêmité du domino le plus\n"
			"à droite ; pareil pour la gauche.\n"
			"Ne vous inquiétez pas! Dans une partie simple\n"
			"les extrêmités d'un domino sont interchangeables.\n"
			"Votre score est calculé en fonction des\n"
			"valeursdes dominos que vous arrivez à placer.\n"
			"La partie s'arrête quand il n'y a plus aucun\n"
			"domino à piocher et que tous les deux joueurs\n"
			"ne peuvent plus jouer.\n"
			"\n"
			"Quand c'est votre tour:\n"
			" - Pour pouvoir jouer un domino, tapez son\n"
			"  numéro correspondant. S'il est jouable,\n"
			"  vous gagnez des points. S'il ne l'est pas,\n"
			"  dans une partie simple, vous pourrez\n"
			"  retenter votre chance.\n"
			" - Si vous êtes dans l'incapacité de jouer,\n"
			"  cliquez sur 'Piocher' pour piocher un domino,\n"
			"  qui sera rajouté à votre main.\n"
			"\n"
			"Cordialement, Ben Kabongo.\n")
		self._affiche("Règles de jeu", text)

	def _afficheCommandes(self, event = None):
		text = 	(
			"control+j : jouer\n"
			"control+p : piocher\n"
			"<- et ->  : faire défiler les dominos\n"
			"control+n : nouvelle partie facile\n"
			"control+d : nouvelle partie difficile\n"
			"alt+r     : affiche les règles de jeu\n"
			"alt+c     : affiche les commandes de jeu\n"
			"alt+i     : affiche mes infos persos\n"
			"control+q : quitter\n"
			)
		self._affiche("Commandes de jeu", text)

	def _afficheInfos(self, event = None):
		text =	("Jeu codé par Ben Kabongo Buzangu\n"
			"Etudiant en L1 Informatique de l'Unicaen\n")
		self._affiche("A propos de moi", text)

def main():
	app = Application()
	app.mainloop()

if __name__ == "__main__":
	main()
