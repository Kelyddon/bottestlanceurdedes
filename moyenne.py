
# =============================
# Module de calcul de moyenne pour les lancers de dés
# =============================

import re

def moyenne_lancers_par_faces(historique, pseudo, faces):
    """
    Calcule la moyenne de tous les résultats de l'utilisateur 'pseudo' pour les dés à 'faces' faces.
    - Recherche insensible à la casse et aux accents sur le pseudo.
    - Prend en compte tous les lancers, même multiples (ex : 20d20).
    Args:
        historique (list[str]): Liste des entrées d'historique (chaînes)
        pseudo (str): Nom du joueur à rechercher
        faces (int): Nombre de faces du dé (ex : 6 pour d6)
    Returns:
        float | None: Moyenne des résultats, ou None si aucun lancer trouvé
    """
    import unicodedata
    def normalize(s):
        # Supprime les accents, met en minuscule et retire les espaces superflus
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().strip()

    total = 0  # Somme de tous les résultats trouvés
    count = 0  # Nombre total de dés pris en compte
    pseudo_norm = normalize(pseudo)
    # Regex pour extraire tous les lancers du bon type de dé, peu importe le pseudo
    pattern = re.compile(r"\| *(.*?) a lancé (\d+)d{} : \[(.*?)\] \(total: (\d+)\)".format(faces))
    for entry in historique:
        m = pattern.search(entry)
        if m:
            pseudo_entry = normalize(m.group(1))  # Normalise le pseudo trouvé dans l'historique
            if pseudo_entry == pseudo_norm:
                # m.group(3) contient la liste des résultats, ex: '7, 1, 17, ...'
                results = [int(x.strip()) for x in m.group(3).split(',') if x.strip().isdigit()]
                total += sum(results)
                count += len(results)
    if count == 0:
        return None  # Aucun lancer trouvé pour ce pseudo et ce type de dé
    return total / count  # Moyenne réelle sur tous les dés


# =============================
# Exemple d'utilisation et test
# =============================
if __name__ == "__main__":
    # Exemple d'historique simulé
    historique = [
        "2026-01-21 10:00:00 | Alice a lancé 1d6 : [4] (total: 4)",
        "2026-01-21 10:01:00 | Alice a lancé 2d6 : [3, 5] (total: 8)",
        "2026-01-21 10:02:00 | Bob a lancé 1d6 : [6] (total: 6)",
        "2026-01-21 10:03:00 | Alice a lancé 1d20 : [15] (total: 15)",
        "2026-01-21 10:04:00 | Alice a lancé 1d6 : [2] (total: 2)",
    ]

    pseudo = "Alice"
    faces = 6
    moyenne = moyenne_lancers_par_faces(historique, pseudo, faces)
    if moyenne is not None:
        print(f"Moyenne des résultats de {pseudo} pour les dés à {faces} faces : {moyenne:.2f}")
    else:
        print(f"Aucun lancer trouvé pour {pseudo} avec des dés à {faces} faces.")
