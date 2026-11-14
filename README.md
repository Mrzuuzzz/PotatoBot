# PotatoBot 🥔

Hi, this is potatobot, a bot I'm currently working on lol

This bad boy can do:
- brailynsmom (tally + leaderboard)
- send fire messages
- roll dice
- send cute cars
- and more!!!

## Setup

Requires Python 3.9+ and a Discord bot token from the
[Discord Developer Portal](https://discord.com/developers/applications).

```bash
# 1. create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. install dependencies
pip install -r requirements.txt

# 3. add your bot token
echo 'THE_KEY=your-token-here' > .env

# 4. create the tally file used by /brailynmom and /leaderboard
echo '{"counter": 0, "leaderboard": {}}' > brailynmom.json
```

## Run

```bash
python main.py
```

Slash commands are synced globally on startup, so they can take a little while
to show up in Discord the first time.

Run it from the repo folder: the `/stats` command loads `COMIC.TTF` and
`/brailynmom` reads `brailynmom.json` from the current directory.
