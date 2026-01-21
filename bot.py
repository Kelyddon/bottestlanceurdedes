import discord
from discord.ext import commands
from main import DiceRoller
import os

intents = discord.Intents.default()
intents.message_content = True  # Nécessaire pour lire le contenu des messages

bot = commands.Bot(command_prefix="/", intents=intents)
roller = DiceRoller()

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

@bot.command()
async def des(ctx, *, arg):
    # Limites : max 20 dés, max 1000 faces
    try:
        nb, faces = map(int, arg.lower().replace('é','e').replace('dés','des').split('des'))
    except Exception:
        await ctx.send("Commande invalide. Exemple : /des 1des100 ou /des 2des6")
        return
    if nb < 1 or nb > 20 or faces < 2 or faces > 1000:
        await ctx.send("Limite : 1 à 20 dés, 2 à 1000 faces par dé.")
        return
    # Envoie un GIF d'attente
    gif_url = "https://cdn.discordapp.com/attachments/1463498955026468874/1463499986288382128/teamwahoo-don-quixote.gif"
    embed = discord.Embed(title="Lancement des dés...")
    embed.set_image(url=gif_url)
    wait_msg = await ctx.send(embed=embed)
    import asyncio
    await asyncio.sleep(6)
    result, _ = roller.roll(f"/{arg}", str(ctx.author.display_name))
    await wait_msg.delete()
    if result:
        await ctx.send(result)
    else:
        await ctx.send("Commande invalide. Exemple : /des 1des100 ou /des 2des6")

@bot.command(name="aide")
async def aide(ctx, *, arg: str = None):
    if not arg or arg.lower() != "lanceurdedes":
        await ctx.send("Utilise `/aide LanceurDeDes` pour voir les commandes de ce bot.")
        return
    msg = (
        "**Commandes disponibles pour LanceurDeDes :**\n"
        "/des XdesY — Lance X dés de Y faces. Exemple : `/des 2des6`\n"
        "/historique me — Affiche tes 5 derniers lancers.\n"
        "/historique pseudo — Affiche les 5 derniers lancers du pseudo donné.\n"
        "/aide LanceurDeDes — Affiche cette aide.\n"
        "\nLimites : 1 à 20 dés, 2 à 1000 faces par dé."
    )
    await ctx.send(msg)

@bot.command()
async def historique(ctx, qui: str = None):
    if not qui or qui.strip() == "":
        await ctx.send("Mauvaise commande. Utilise `/historique me` ou `/historique pseudo`.")
        return
    hist = roller.get_history()
    if not hist:
        await ctx.send("Aucun lancer de dés enregistré pour le moment.")
        return
    from tablelancerdedes import format_5_derniers_lancers
    pseudo = str(ctx.author.display_name) if qui.lower() == "me" else qui
    msg = format_5_derniers_lancers(hist, pseudo)
    # Discord limite à 2000 caractères par message
    if len(msg) <= 1990:
        await ctx.send(f"```{msg}```")
    else:
        # Découpe le message en morceaux de 1990 caractères
        for i in range(0, len(msg), 1990):
            chunk = msg[i:i+1990]
            await ctx.send(f"```{chunk}```")

bot.run(os.getenv("DISCORD_TOKEN"))