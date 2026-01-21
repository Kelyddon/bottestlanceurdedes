

# Module pour la gestion et l'affichage de l'historique des lancers de dés
from collections import defaultdict  # Pour regrouper les lancers par joueur

def get_lancers_par_joueur(historique):
	"""
	Transforme la liste d'historique en dictionnaire {pseudo: [lancers]}.
	Chaque pseudo a sa propre liste de lancers (chaîne).
	Args:
		historique (list[str]): Liste des entrées d'historique
	Returns:
		dict: Dictionnaire pseudo -> liste de lancers
	"""
	lancers_par_joueur = defaultdict(list)
	for entry in historique:
		try:
			# Récupère le pseudo à partir de l'entrée formatée
			pseudo = entry.split('|')[1].split(' a lancé')[0].strip()
		except Exception:
			# Ignore les entrées mal formatées
			continue
		lancers_par_joueur[pseudo].append(entry)
	return lancers_par_joueur

def format_5_derniers_lancers(historique, pseudo=None):
	"""
	Retourne une chaîne formatée des 5 derniers lancers pour un pseudo donné.
	Si pseudo=None, retourne pour tous les joueurs.
	Format adapté à Discord (ou console), avec saut de ligne entre chaque lancer.
	Args:
		historique (list[str]): Liste des entrées d'historique
		pseudo (str, optionnel): Pseudo du joueur ciblé
	Returns:
		str: Texte formaté à afficher
	"""
	lancers_par_joueur = get_lancers_par_joueur(historique)
	output = ""
	if pseudo:
		# Affiche pour un joueur spécifique
		if pseudo not in lancers_par_joueur:
			output += f"Aucun lancer trouvé pour {pseudo}.\n"
		else:
			output += f"--- {pseudo} ---\n"
			for lancer in lancers_par_joueur[pseudo][-5:]:
				try:
					# Sépare la date et le reste du texte
					date, reste = lancer.split('|', 1)
					reste = reste.strip()
					output += f"{date.strip()} : {reste}\n"
				except Exception:
					# Si le format est inattendu, affiche brut
					output += lancer + "\n"
			output += "\n"
	else:
		# Affiche pour tous les joueurs
		for joueur, lancers in lancers_par_joueur.items():
			output += f"--- {joueur} ---\n"
			for lancer in lancers[-5:]:
				try:
					date, reste = lancer.split('|', 1)
					reste = reste.strip()
					output += f"{date.strip()} : {reste}\n"
				except Exception:
					output += lancer + "\n"
			output += "\n"
	return output

# =====================
# Utilisation typique :
#   format_5_derniers_lancers(historique, pseudo) -> str
#   format_5_derniers_lancers(historique) -> str (tous joueurs)
# =====================

# Ce module ne doit contenir que la logique liée à l'affichage et la gestion du tableau des lancers de dés.
# Les fonctions sont utilisées par le bot Discord et le lanceur local.
