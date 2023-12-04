# Advent-Bot
This bot is used to allow simple data to be collected from Advent of Code and embedded in discord. Utility functions are located in advent_resources.py, and these are used in advent.py, which is a Cog for the Discord.py bot.
# Features (Discord Slash Commands)
## /stats_embed
This command pulls data from a private advent leaderboard and the mapping.json file to create a leaderboard of who has fully completed a day with a list of discord mentions.

<img width="378" alt="Screenshot 2023-12-02 at 1 10 56 AM" src="https://github.com/YKawesome/Advent-Bot/assets/72176181/13f9e690-a0e7-409f-b9a9-42736b1add98">

The title is scraped from the AOC website through BeatifulSoup (simple, since the title is in the first h2 tag on each day), and the day to use for everything is found through the datetime module using EST time (since puzzles come out 12AM EST).
Different emojis were used to make the leaderboard a bit more visually interesting, and the embed color is the same hex as AOC (in fact, the bot uses AOC's icon).
## /stats_string
This command pulls a very rudimentary string list of which AOC leaders in the current server have finished the challenge.

<img width="478" alt="Screenshot 2023-12-02 at 1 14 17 AM" src="https://github.com/YKawesome/Advent-Bot/assets/72176181/12fd71fa-8b9d-42be-94f9-d999c133bcc4">

It is more generally used as a backup for /stats_embed since it lacks much more of the functionality.

## /get_leaderboard
Gets the top 8 members of the current server on the private advent leaderboard for that server, and sorts by points. This also shows the *total* number of stars earned by each person.

<img width="386" alt="Screenshot 2023-12-03 at 10 31 28 PM" src="https://github.com/YKawesome/Advent-Bot/assets/72176181/e9ad8264-029b-437b-bcde-d1ae5d5e3435">

All data is taken easily from the json provided by AoC for the private leaderboard.

## /add_mapping and /remove_mapping
These commands are used to map or remove a mapping of a discord user to an advent id; you pass in a mention to a user to the command and a nickname, and you must manually find their AOC id (there isn't a better way to do this since it cannot know who is who).

<img width="465" alt="Screenshot 2023-12-02 at 1 16 28 AM" src="https://github.com/YKawesome/Advent-Bot/assets/72176181/0b0128e9-1167-4f8a-8624-5d1f02b29960">

## Owner-Only
### /sync, /syncowner, syn
Sync will sync the command tree with discord so that all guilds have access to the public commands.
Syncowner will sync all owner-only commands and update them so they can only be used in the developer_guild (which is a secret in the .env file).
Syn is not a slash command, and is used when slash commands need to be initialized for the first time or as a backup.

<img width="306" alt="Screenshot 2023-12-02 at 1 18 45 AM" src="https://github.com/YKawesome/Advent-Bot/assets/72176181/df653050-43e4-4a12-b414-010b36c22717">
