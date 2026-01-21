from collections import defaultdict

def afficher_5_derniers_lancers(historique):
	"""
	Affiche les 5 derniers lancers de dés pour chaque utilisateur à partir d'une liste d'entrées d'historique.
	Format lisible pour Discord, avec saut de ligne entre chaque lancer.
	"""
	lancers_par_joueur = defaultdict(list)
	for entry in historique:
		try:
			pseudo = entry.split('|')[1].split(' a lancé')[0].strip()
		except Exception:
			continue
		lancers_par_joueur[pseudo].append(entry)

	for joueur, lancers in lancers_par_joueur.items():
		print(f"--- {joueur} ---")
		for lancer in lancers[-5:]:
			try:
				date, reste = lancer.split('|', 1)
				reste = reste.strip()
				print(f"{date.strip()} : {reste}\n")
			except Exception:
				print(lancer + "\n")
		print("")

# Exemple d'utilisation :
if __name__ == "__main__":
	# Exemple d'historique simulé
	historique = [
		"2026-01-21 10:00:00 | Alice a lancé 1d20 : [15] (total: 15)",
		"2026-01-21 10:01:00 | Bob a lancé 2d6 : [3, 5] (total: 8)",
		"2026-01-21 10:02:00 | Alice a lancé 1d20 : [7] (total: 7)",
		# ... ajoutez d'autres entrées pour tester ...
	]
	afficher_5_derniers_lancers(historique)
