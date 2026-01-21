import unicodedata
from tablelancerdedes import afficher_5_derniers_lancers

class DiceRoller:
    def __init__(self):
        self.historique = []

    def roll(self, command: str, joueur: str):
        # Supprimer tous les accents de la commande
        command = ''.join(
            c for c in unicodedata.normalize('NFD', command)
            if unicodedata.category(c) != 'Mn'
        )
        match = re.match(r"/(\d+)des(\d+)", command)
        if not match:
            return None, None
        nb, faces = int(match.group(1)), int(match.group(2))
        if nb < 1 or faces < 2:
            return None, None
        rolls = [random.randint(1, faces) for _ in range(nb)]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = f"Lancer {nb}d{faces} : {rolls} (total: {sum(rolls)})"
        histo_entry = f"{now} | {joueur} a lancé {nb}d{faces} : {rolls} (total: {sum(rolls)})"
        self.historique.append(histo_entry)
        return result, histo_entry

    def get_history(self):
        return self.historique


def main():
    print("Bienvenue dans le lanceur de dés JDR !")
    roller = DiceRoller()
    joueur = input("Entrez votre pseudo : ")
    while True:
        cmd = input("Entrez une commande de lancer de dés (ex: /1dés100, /2dés6), 'h' pour historique, ou 'q' pour quitter : ")
        if cmd.lower() == 'q':
            break
        if cmd.lower() == 'h':
            print("\n--- 5 derniers lancers par utilisateur ---")
            afficher_5_derniers_lancers(roller.get_history())
            print("------------------------------------------\n")
            continue
        result, _ = roller.roll(cmd, joueur)
        if result is not None:
            print(result)
        else:
            print("Commande invalide. Essayez : /1dés100 ou /2dés6 ...")


import random
import re
from datetime import datetime


if __name__ == "__main__":
    main()
