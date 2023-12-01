import os
import urllib.request
import json
from datetime import datetime
import pytz
import discord
from dotenv import load_dotenv

load_dotenv()

_NUMS = ['first_place', 'second_place', 'third_place', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
_SESSION_COOKIE = os.getenv('SESSION_COOKIE')


def get_leaderboard_json(guild_id: str) -> dict:
    '''Returns the leaderboard JSON as a dict.'''
    leaderboard_id = get_mapping_json(guild_id)['leaderboard_id']
    request = urllib.request.Request(f'https://adventofcode.com/2023/leaderboard/private/view/{leaderboard_id}.json')
    request.add_header('Cookie', f'session={_SESSION_COOKIE}')
    response = urllib.request.urlopen(request)
    return dict(json.loads(response.read().decode('utf-8')))


def get_test_json() -> dict:
    '''Returns the test JSON as a dict'''
    f = open('json/test.json', 'r')
    return dict(json.loads(f.read()))


def get_mapping_json(guild_id: str) -> dict:
    '''Returns the mapping JSON as a dict.'''
    f = open('json/mapping.json', 'r')
    return dict(json.loads(f.read()))[guild_id]


def _get_day() -> int:
    '''Returns the current day in EST.'''
    now_utc = datetime.utcnow()
    est_timezone = pytz.timezone('America/New_York')
    now_est = now_utc.astimezone(est_timezone)
    return now_est.day


def _get_user_completed_today(leaderboard: dict, user_id: str) -> bool:
    '''Returns whether or not the user has completed today's challenge.'''
    if str(_get_day()) in leaderboard['members'][user_id]['completion_day_level']:
        if "2" in leaderboard['members'][user_id]['completion_day_level'][str(_get_day())]:
            return True
    return False


def get_stats_string(leaderboard: dict) -> str:
    '''Returns the stats string on who has completed today's challenge.'''
    string = ''
    for id in leaderboard['members']:
        if _get_user_completed_today(leaderboard, id):
            string += f'{leaderboard["members"][id]["name"]} has completed today\'s challenge.\n'
        else:
            string += f'{leaderboard["members"][id]["name"]} has not completed today\'s challenge\n'
    return string


def get_stats_embed(leaderboard: dict, guild: discord.Guild) -> discord.Embed:
    '''Returns the stats embed on who has completed today's challenge.'''
    embed = discord.Embed(title='Today\'s Challenge', description='Who has completed today\'s challenge?', color=0xffff69)

    completed_str = ''
    i = 0
    for id in get_discord_ids_completed_challenge_sorted(leaderboard, get_mapping_json(str(guild.id))):
        try:
            member = guild.get_member(id).mention
        except AttributeError:
            member = id
        completed_str += f':{_NUMS[i]}: {member}\n'
        if i == 2:
            completed_str += '----------------\n'
        if i == 9:
            break
        i += 1
    embed.add_field(name='Completed', value=completed_str, inline=False)

    not_completed_str = ''
    for id in get_discord_ids_not_completed_challenge(leaderboard, get_mapping_json(str(guild.id))):
        try:
            member = guild.get_member(id).mention
        except AttributeError:
            member = id
        not_completed_str += f'{member}\n'
    embed.add_field(name='Not Completed', value=not_completed_str, inline=False)

    return embed


def get_discord_ids_completed_challenge(leaderboard: dict, mapping: dict) -> list:
    '''Returns a list of discord ids of people who have completed today's challenge.'''
    discord_ids = []
    for advent_id in leaderboard['members']:
        if _get_user_completed_today(leaderboard, advent_id):
            if mapping[advent_id] is not None:
                discord_ids.append(mapping[advent_id])
    return discord_ids


def get_discord_ids_not_completed_challenge(leaderboard: dict, mapping: dict) -> list:
    '''Returns a list of discord ids of people who have not completed today's challenge.'''
    discord_ids = []
    for advent_id in leaderboard['members']:
        if not _get_user_completed_today(leaderboard, advent_id):
            if mapping[advent_id] is not None:
                discord_ids.append(mapping[advent_id])
    return discord_ids


def get_discord_ids_completed_challenge_sorted(leaderboard: dict, mapping: dict) -> list:
    '''Returns a list of discord ids sorted by the time they got their last star.'''
    last_star_ts = []
    for advent_id in leaderboard['members']:
        if _get_user_completed_today(leaderboard, advent_id):
            if mapping[advent_id] is not None:
                last_star_ts.append((mapping[advent_id], leaderboard['members'][advent_id]['last_star_ts']))
    last_star_ts.sort(key=lambda x: x[1])
    return [x[0] for x in last_star_ts]