import discord, requests, aiohttp, io, random, asyncio, json, os
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from dotenv import load_dotenv, dotenv_values 

#hi jorge!

"""--- SETTING UP ---"""
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="@", intents=intents)
sleepTimer = 3
load_dotenv()


def log(s: str):
    """prints a message to the terminal to 'log' it with a timestamp"""
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    print(time + s)


@bot.event
async def on_ready():
    """what does the bot do when i click run"""
    print(f"Logged in as {bot.user}")
    try:
        game = discord.Game("globally")
        await bot.change_presence(status=discord.Status.idle, activity=game)
        synced = await bot.tree.sync()  # Sync commands globally
        print(f"Synced {len(synced)} commands globally.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return


@bot.tree.command(
    name="brailynmom",
    description="add a tally to the number of times brailyn's mother has been fucked",
)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def brailynmom(interaction: discord.Integration):
    """Adds one to the number of times we've fucked brailyns mom"""

    userid = interaction.user.id

    log(f"{userid} ran brailynmomcounter")

    with open("brailynmom.json", "r+") as file:
        j = json.load(file)

        # adds one more to tally
        counter = j["counter"] + 1
        j["counter"] = counter

        # increment leaderboard for the user
        if str(userid) in j["leaderboard"]:
            j["leaderboard"][str(userid)] += 1
        else:
            j["leaderboard"][str(userid)] = 1

        # write back to the file
        file.seek(0)
        json.dump(j, file, indent=4)
        file.truncate()

    await interaction.response.send_message(
        f"You did brailyn's mother!\nTotal = **{counter}**\nYou = **{j['leaderboard'][str(userid)]}**"
    )


# Define the slash command, localized to the specific server
@bot.tree.command(
    name="fire", 
    description="Send a FIRE GIF with your custom message")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def fire(interaction: discord.Interaction, message: str):
    """Slash command to send a FIRE gif with a custom message."""

    # 1) CREATE GIF
    payload = {
        "LogoID": "4",
        "Text": message,
        "FontSize": "70",
        "Color1_color": "#FF0000",
        "Integer1": "15",
        "Boolean1": "on",
        "Integer9": "0",
        "Integer13": "on",
        "Integer12": "on",
        "BackgroundColor_color": "#FFFFFF",
    }

    gifurl = requests.post("https://cooltext.com/PostChange", data=payload).json()[
        "renderLocation"
    ]

    # 2) SAVE GIF (not to storage hopefully)
    output = "fire.gif"
    r = requests.get(gifurl, verify=False)
    if r.status_code == 200:
        with open(output, "wb") as file:
            file.write(r.content)
        log("Saved fire.gif")
    else:
        log(f"Failed to download the GIF. Status code: {r.status_code}")

    # 3) SEND GIF
    try:
        # Send the response with the GIF and the message
        with open("fire.gif", "rb") as gif_file:
            file = discord.File(gif_file, filename="fire.gif")
            await interaction.response.defer()
            await asyncio.sleep(sleepTimer)
            await interaction.followup.send(file=file)
            log("fire.gif sent sucessfully")
    except Exception as e:
        await interaction.response.send_message("Something went wrong!", ephemeral=True)
        log(f"Error sending fire gif: {e}")


@bot.tree.command(
    name="dice", 
    description="roll a dice with 'n' sides")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def dice(interaction: discord.Interaction, n: str):
    x = random.randint(1, int(n))
    y = ""
    if int(n) <= 1:
        await interaction.response.send_message(
            ":person_standing: you should prob give a number greater than one..."
        )
    elif x == n:
        y = "!!!"
    elif x == 1:
        y = "..."

    await interaction.response.send_message(f"Rolling a d{n}\nResult is: {x}{y}")


@bot.tree.command(
    name="send_car", 
    description="Get an image of a cute random car")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def send_car(interaction: discord.Interaction):
    """Sends a random cat picture from https://genrandom.com/cats/"""
    url = "https://genrandom.com/api/cat"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                # Read the image bytes
                image_data = await response.read()
                # Get the file extension from the Content-Type header
                content_type = response.headers.get("Content-Type", "image/jpeg")
                extension = (
                    content_type.split("/")[-1] if "/" in content_type else "jpg"
                )
                # Create a file object in memory
                file = discord.File(io.BytesIO(image_data), filename=f"cat.{extension}")
                await interaction.response.defer()
                await asyncio.sleep(sleepTimer)
                await interaction.followup.send(file=file)
                log("Sent a random cat picture!")
            else:
                await interaction.response.send_message(
                    "Couldn't fetch a cat image right now, sorry!"
                )
                log("Couldn't send a random cat picture")


@bot.tree.command(
    name="ping", 
    description="returns the ping between you and the server (chromebook lol)"
)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"pong! 🏓, ping is: {bot.latency*1000:.2f} milliseconds!"
    )


@bot.tree.command(
    name="potato_pic", 
    description="get a random potato picture :o")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def potato_pic(interaction: discord.Interaction):

    listPotato = [  # a buttload of potato pictures
        "https://images.seattletimes.com/wp-content/uploads/2024/04/04082024_OpEd-Potatoes_124536.jpg?d=2040x1488",
        "https://m.media-amazon.com/images/I/51gMSeWnmgL._AC_UF894,1000_QL80_.jpg",
        "https://media.istockphoto.com/id/146731001/photo/potato.jpg?s=612x612&w=0&k=20&c=S20OtjWX02j5o4EB3oC89fjgGw0SnxGbJ3AT6mLvuhs=",
        "https://www.shutterstock.com/image-photo/washed-potatoes-organic-potato-isolated-260nw-2452909787.jpg",
        "https://i5.walmartimages.com/asr/900b3713-5ba3-4f40-bd73-f95a04b0ae13.76d4af6527a3e0f5f463c7e0877f7cfd.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF",
        "https://www.heddensofwoodtown.co.uk/wp-content/uploads/2020/02/wilja_potatoes_opt.jpg",
        "https://plus.unsplash.com/premium_photo-1724256031338-b5bfba816cfd?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8cG90YXRvfGVufDB8fDB8fHww"
        "https://www.keystonepotato.com/wp-content/uploads/2022/04/banner-potato-image.png",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTu3hixOCV2Ev7g5oonOdjEdC3h_YsNUuEAWaRrGOHOPtrqjRcCwiJEiY0sV26kfVaKblE&usqp=CAU",
        "https://meridianfarmmarket.ca/cdn/shop/products/little-potato-company-potatoes-baby-boomer_1.jpg?v=1655861933",
        "https://i5.walmartimages.com/seo/Russet-Baking-Potatoes-Whole-Fresh-Each_c638c006-a982-48f7-aa33-6d3a8dc2983c.8fd015937ebfdd46c8fcb6177d0d1b1d.jpeg?odnHeight=2000&odnWidth=2000&odnBg=FFFFFF",
        "https://images.themodernproper.com/billowy-turkey/production/posts/PerfectBakedPotatoRecipe_1.jpg?w=1200&q=82&auto=format&fit=crop&dm=1720704447&s=75603b740f4f3d5adcaa66fa28cb1eae",
        "https://www.crimsoncoward.com/wp-content/uploads/2023/05/potatoes-scaled.jpg",
        "https://www.recipetineats.com/tachyon/2023/11/Fondant-potatoes_4-close-up.jpg",
        "https://cdn.mos.cms.futurecdn.net/iC7HBvohbJqExqvbKcV3pP-1200-80.jpg",
        "https://images.seattletimes.com/wp-content/uploads/2024/04/04082024_OpEd-Potatoes_124536.jpg?d=2040x1488",
        "https://cdn.britannica.com/08/194708-050-56FF816A/potatoes.jpg",
        "https://www.completelydelicious.com/wp-content/uploads/2020/10/buttery-boiled-potatoes-6.jpg",
        "https://www.simplotfoods.com/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2F0dkgxhks0leg%2FRKiZ605RAV8kjDQnxFCWP%2Fb03b8729817c90b29b88d536bfd37ac5%2F9-Unusual-Uses-For-Potatoes.jpg%3Ffm%3Dwebp&w=1920&q=75",
        "https://nutritionsource.hsph.harvard.edu/wp-content/uploads/2014/01/potatoes-411975_1280-1024x682.jpg",
        "https://www.lovefoodhatewaste.com/sites/default/files/styles/twitter_card_image/public/2022-08/Potatoes-shutterstock-1721688538.jpg.webp?itok=4hLqSjDi",
        "https://cdn.britannica.com/20/191620-050-161F6867/fingerling-potatoes.jpg",
        "https://www.netafimindia.com/cdn-cgi/image/format=auto,fit=crop,quality=80,width=750,/contentassets/98512e81691249368e1ca89dcaa7abcd/potatoes_challenge-1-1.png",
        "https://scitechdaily.com/images/Potato-Sunlight-777x518.jpg",
    ]

    url = random.choice(listPotato)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                # Read the image bytes
                image_data = await response.read()
                # Get the file extension from the Content-Type header
                content_type = response.headers.get("Content-Type", "image/jpeg")
                extension = (
                    content_type.split("/")[-1] if "/" in content_type else "jpg"
                )
                # Create a file object in memory
                file = discord.File(
                    io.BytesIO(image_data), filename=f"potato.{extension}"
                )
                await interaction.response.send_message(file=file)
                log("Sent a random potato picture!")
            else:
                await interaction.response.send_message(
                    "Couldn't fetch a potato image right now, sorry!"
                )
                log("Couldn't send a random potato picture")


@bot.tree.command(
    name="leaderboard", 
    description="view the leaderboard for that one command"
)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def embed_message(interaction: discord.Interaction):
    """Sends an embedded message with a title and description."""
    me = interaction.user.id
    with open("brailynmom.json", "r") as file:
        data = json.load(file)

    leaderboard = data["leaderboard"]
    leaderboard_tuples = [(int(key), value) for key, value in leaderboard.items()]
    sorted_leaderboard = sorted(leaderboard_tuples, key=lambda x: x[1], reverse=True)
    positioned_leaderboard = [
        (
            f"{i+1}{'st' if i == 0 else 'nd' if i == 1 else 'rd' if i == 2 else 'th'}",
            score,
            user_id,
        )
        for i, (user_id, score) in enumerate(sorted_leaderboard)
    ]

    output = "**Total: " + str(data["counter"]) + "**\n"
    for i in positioned_leaderboard:
        x = ""
        if i[2] == me:
            x = " < YOU"
        output += f"\n{i[0]}, {i[1]}{x}"

    embed = discord.Embed(title="Leaderboard", description=output, colour=0xD6B67E)
    await interaction.response.send_message(embed=embed)

    log(f"{me} sent leaderboard of brailynmom")


@bot.tree.command(
    name="peter", 
    description="tee hee")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def peter(interaction: discord.Interaction):
    x = random.randint(0,10)  # Hash userID and limit it to the range 0-10
    y = ""
    if x <= 1:  y = "tiny peter"
    if x >= 9: y = "beeg peter"
    await interaction.response.send_message(f"8{'='*x}D {y}")
    
@bot.tree.command(
    name="server", 
    description="free advertisment i guess")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install()
async def peter(interaction: discord.Interaction):
    await interaction.response.send_message("https://discord.gg/Zp7GqWxZXW")


# run that mofo
bot.run(os.getenv("THE_KEY"))