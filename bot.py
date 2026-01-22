


# =============================
# Imports et initialisation du bot Discord
# =============================
import discord  # Librairie principale pour interagir avec Discord
from discord.ext import commands  # Pour créer des commandes personnalisées
from main import DiceRoller  # Classe pour gérer les lancers et l'historique
from moyenne import moyenne_lancers_par_faces  # Fonction de calcul de moyenne
import os  # Pour accéder aux variables d'environnement

# Configuration des permissions/intents du bot
intents = discord.Intents.default()
intents.message_content = True  # Permet au bot de lire le contenu des messages

# Création de l'instance du bot avec le préfixe '/'
bot = commands.Bot(command_prefix="/", intents=intents)
# Instancie le gestionnaire de dés
roller = DiceRoller()

# =============================
# Commandes du bot
# =============================

# Commande de debug pour afficher tous les pseudos trouvés dans l'historique
@bot.command()
async def debug_pseudos(ctx):
    from tablelancerdedes import get_lancers_par_joueur
    hist = roller.get_history()
    pseudos = list(get_lancers_par_joueur(hist).keys())
    if not pseudos:
        await ctx.send("Aucun pseudo trouvé dans l'historique.")
    else:
        await ctx.send("Pseudos trouvés dans l'historique : " + ", ".join(pseudos))

# Commande pour calculer la moyenne des lancers : /moyenne <pseudo>des<faces>
@bot.command()
async def moyenne(ctx, *, arg):
    """
    Calcule la moyenne des résultats pour un utilisateur et un type de dé.
    Utilisation : /moyenne <pseudo>des<faces>
    Exemple : /moyenne Alice des6
    """
    import re
    # Extraction du pseudo et du nombre de faces depuis l'argument utilisateur
    m = re.match(r"(.+) *des(\d+)", arg.strip(), re.IGNORECASE)
    if not m:
        await ctx.send("Commande invalide. Exemple : /moyenne Alice des6")
        return
    pseudo = m.group(1).strip()
    faces = int(m.group(2))
    hist = roller.get_history()
    moyenne = moyenne_lancers_par_faces(hist, pseudo, faces)
    if moyenne is None:
        await ctx.send(f"Aucun lancer trouvé pour {pseudo} avec des dés à {faces} faces.")
    else:
        await ctx.send(f"Moyenne des résultats de {pseudo} pour les dés à {faces} faces : {moyenne:.2f}")

# Commande pour lancer des dés : /des XdesY
@bot.command()
async def des(ctx, *, arg):
    # Limites : max 20 dés, max 1000 faces
    try:
        # Normalise la commande et extrait le nombre de dés et de faces
        nb, faces = map(int, arg.lower().replace('é','e').replace('dés','des').split('des'))
    except Exception:
        # Message d'erreur si la commande est mal formatée
        await ctx.send("Commande invalide. Exemple : /des 1des100 ou /des 2des6")
        return
    # Vérifie les limites autorisées
    if nb < 1 or nb > 20 or faces < 2 or faces > 1000:
        await ctx.send("Limite : 1 à 20 dés, 2 à 1000 faces par dé.")
        return
    # Envoie un GIF d'attente pour l'effet suspense
    gif_url = "https://cdn.discordapp.com/attachments/1463498955026468874/1463499986288382128/teamwahoo-don-quixote.gif"
    embed = discord.Embed(title="Lancement des dés...")
    embed.set_image(url=gif_url)
    wait_msg = await ctx.send(embed=embed)
    import asyncio
    await asyncio.sleep(6)  # Attente pour l'effet
    # Effectue le lancer de dés
    result, _ = roller.roll(f"/{arg}", str(ctx.author.display_name))
    await wait_msg.delete()  # Supprime le GIF
    if result:
        await ctx.send(result)  # Affiche le résultat
    else:
        await ctx.send("Commande invalide. Exemple : /des 1des100 ou /des 2des6")

# Commande d'aide : /aide LanceurDeDes
@bot.command(name="aide")
async def aide(ctx, *, arg: str = None):
    if not arg or arg.lower() != "lanceurdedes":
        # Invite à utiliser la bonne commande d'aide
        await ctx.send("Utilise `/aide LanceurDeDes` pour voir les commandes de ce bot.")
        return
    # Message d'aide détaillé
    msg = (
        "**Commandes disponibles pour LanceurDeDes :**\n"
        "/des XdesY — Lance X dés de Y faces. Exemple : `/des 2des6`\n"
        "/historique me — Affiche tes 5 derniers lancers.\n"
        "/historique pseudo — Affiche les 5 derniers lancers du pseudo donné.\n"
        "/debug_pseudo — Affiche tous les pseudos trouvés dans l'historique.\n"
        "/moyenne <pseudo>des<faces> — Calcule la moyenne de tous les résultats de l'utilisateur donné pour les dés à X faces.\n"
        "   Exemple : `/moyenne Alice des6` retournera la moyenne de tous les lancers de dés à 6 faces faits par Alice depuis le début du bot.\n"
        "/aide LanceurDeDes — Affiche cette aide.\n"
        "\nLimites : 1 à 20 dés, 2 à 1000 faces par dé."
    )
    await ctx.send(msg)

# Commande pour afficher l'historique : /historique me ou /historique pseudo
@bot.command()
async def historique(ctx, qui: str = None):
    if not qui or qui.strip() == "":
        # Message d'erreur si la commande est incomplète
        await ctx.send("Mauvaise commande. Utilise `/historique me` ou `/historique pseudo`.")
        return
    hist = roller.get_history()  # Récupère l'historique des lancers
    if not hist:
        await ctx.send("Aucun lancer de dés enregistré pour le moment.")
        return
    from tablelancerdedes import format_5_derniers_lancers
    # Détermine le pseudo à afficher (soi-même ou un autre)
    pseudo = str(ctx.author.display_name) if qui.lower() == "me" else qui
    msg = format_5_derniers_lancers(hist, pseudo)  # Formate l'historique
    # Discord limite à 2000 caractères par message
    if len(msg) <= 1990:
        await ctx.send(f"```{msg}```")
    else:
        # Découpe le message en morceaux de 1990 caractères
        for i in range(0, len(msg), 1990):
            chunk = msg[i:i+1990]
            await ctx.send(f"```{chunk}```")

# =============================
# Événements du bot
# =============================

# Événement déclenché quand le bot est prêt
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")  # Affiche le nom du bot dans la console


# Démarre le bot avec le token Discord récupéré depuis la variable d'environnement
bot.run(os.getenv("DISCORD_TOKEN"))
