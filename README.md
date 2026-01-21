# LanceurDeDes — Bot Discord de lancer de dés

Ce projet est un bot Discord permettant de lancer des dés pour le jeu de rôle, avec historique par utilisateur.

## Lancer le bot

```powershell
$env:DISCORD_TOKEN="votre_token_ici"
python demo/test/bot.py
```

## Animation de chargement (GIF)

Lors d'un lancer de dés, le bot affiche une animation GIF pendant 6 secondes avant de donner le résultat.

**Personnaliser le GIF :**
- Uploade ton GIF dans un salon Discord (même privé).
- Clique droit sur le GIF envoyé > "Copier le lien".
- Remplace l'URL dans le code bot.py (`gif_url = ...`) par ce lien Discord (commence par `https://cdn.discordapp.com/attachments/...`).
- Ce lien Discord CDN garantit un affichage rapide et fiable pour tous les membres du serveur.

## Commandes disponibles

- `/aide LanceurDeDes`  
  Affiche la liste des commandes et les limites du bot.

- `/des <nombre_de_dés>des<nombre_de_faces>`  
  Lance le nombre de dés souhaité.  
  **Exemple :** `/des 2des6` (lance 2 dés à 6 faces)

- `/historique me`  
  Affiche vos 5 derniers lancers.

- `/historique <Nom d'utilisateur>`  
  Affiche les 5 derniers lancers d'un utilisateur donné.

## Limites
- **Nombre de dés :** 1 à 20
- **Nombre de faces :** 2 à 1000

## Exemple d'utilisation

```text
/des 1des100
/historique me
/historique Alice
```

---

**N'oubliez pas de ne jamais publier votre token Discord !**