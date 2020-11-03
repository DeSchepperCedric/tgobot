import json
import datetime
import random
import asyncio

import discord
from discord.ext import commands, tasks
import pytimeparse

from helpers import *
from tgomenus import *


class TGOBot(commands.Bot):
    def __init__(self, config):
        intents = discord.Intents(messages=True, guilds=True, members=True)
        super().__init__(config['command_prefix'], help_command=None, description=config['description'], intents=intents)
        self.config = config
    
    async def on_ready(self):
        print(f"Logged in as: {self.user.name}")
        self.tgo = self.get_guild(self.config['GuildID'])
        self.staff_role = discord.utils.get(self.tgo.roles, name='Staff')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{self.tgo.member_count} members | -tgo"))

    async def on_message(self, message : discord.Message):
        if message.author == self.user:
            return

        if message.author == discord.utils.get(self.get_guild(self.config['GuildID']).members, id = 159985870458322944):
            if "advanced" in message.clean_content:
                c = message.clean_content[message.clean_content.rfind(','):]
                lvl = int(c.replace(', you just advanced to level ','').replace('!','').strip())
                member = message.mentions[0]
                if lvl == 5:
                    await member.add_roles(discord.utils.get(self.tgo.roles, name = 'Member'))
                elif lvl == 10:
                    await member.add_roles(discord.utils.get(self.tgo.roles, name = 'Regular'))
                elif lvl == 15:
                    await member.add_roles(discord.utils.get(self.tgo.roles, name = 'VIP'))
                elif lvl == 30:
                    await member.add_roles(discord.utils.get(self.tgo.roles, name = 'Mega VIP'))
                else:
                    return

        accepted_role = discord.utils.get(self.tgo.roles, name=self.config['accepted_role'])
        
        if 'accept' in message.content.lower() and message.channel.name == 'welcome' and accepted_role not in message.author.roles:
            await message.author.add_roles(accepted_role, reason = 'Accepted.')
            msg = await message.channel.send('Thank you for accepting. Enjoy your stay.')
            await asyncio.sleep(30)
            await message.delete()
            await msg.delete()
            return

        verified_role = discord.utils.get(self.tgo.roles, name=self.config['verified_role'])
        if message.channel.name == 'introductions' and verified_role not in message.author.roles:
            em = discord.Embed(title = f'{message.author.name} messaged in #introductions.', description = f'[Jump to message!](https://discord.com/channels/{self.tgo.id}/{message.channel.id}/{message.id})', color = randcolor())
            em.set_thumbnail(url=message.author.avatar_url)
            await discord.utils.get(self.tgo.channels, name='staff-log').send(content = self.staff_role.mention, embed = em)

            
        await self.process_commands(message)

    

with open('data/config.json') as f:
    config = json.loads(f.read()) 

# Making the TGOBot obj
bot = TGOBot(config)

@bot.command(aliases = ['help'])
@commands.cooldown(1, 600, commands.BucketType.user)
async def staff(ctx):
    await ctx.send(f'{ctx.message.author.mention} needs {bot.staff_role.mention}!')
    try:
        await ctx.message.delete()
    except:
        pass


@bot.command(aliases = [])
@commands.cooldown(1, 600, commands.BucketType.user)   
async def expert(ctx):
    m = ExpertMenu(ctx)
    try:
        await ctx.message.delete()
    except:
        pass
    await m.start(ctx)

@bot.command(aliases = ['tgo'])   
async def menu(ctx):
    m = TGOMenu(ctx)
    await m.start(ctx)

@bot.command()
async def roles(ctx):
    m = RoleMenu(ctx)
    try:
        await ctx.message.delete()
    except:
        pass
    await m.start(ctx)

@bot.command()
@commands.has_role("Staff")
async def mute(ctx, member: discord.Member, time):
    seconds = int(pytimeparse.parse(time))
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role is None:
        perms = discord.Permissions(send_messages=False, speak=False)
        role = await ctx.guild.create_role(name="Muted", permissions=perms)
        
    await member.add_roles(role) 
    msg = await ctx.send(f"{member.mention} was muted.")
    em = discord.Embed(title = f'{member.name} was muted for {seconds} seconds.', description = f'Use `-unmute <mention>` to unmute.', color = randcolor())
    em.set_thumbnail(url=member.avatar_url)
    em.add_field(name='Muted by', value=f'{ctx.message.author.name}')
    em.add_field(name='Target ID', value=f'`{member.id}`')
    await discord.utils.get(bot.tgo.channels, name='staff-log').send(embed = em)
    await asyncio.sleep(2)
    await ctx.message.delete()
    await msg.delete()
    await asyncio.sleep(seconds)
    await _unmute(ctx, member)

async def _unmute(ctx, member: discord.Member):
    em = discord.Embed(title = f'{member.name} was unmuted.', description = f'Use `-mute <mention> <time>` to mute.', color = randcolor())
    em.set_thumbnail(url=member.avatar_url)
    em.add_field(name='Unmuted by', value=f'{ctx.message.author.name}')
    em.add_field(name='Target ID', value=f'`{member.id}`')
    await discord.utils.get(bot.tgo.channels, name='staff-log').send(embed = em)
    muted = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(muted)
    await member.send(f'You have been unmuted in {member.guild.name}.')

@bot.command()
@commands.has_role("Staff")
async def unmute(ctx, member: discord.Member):
    await _unmute(ctx, member)
    try:
        await ctx.message.delete()
    except:
        pass

@bot.command(aliases=['purge','p', 'del'])
async def _purge(ctx, num : int):
    if num > 100:
        msg = await ctx.send("```Can't delete more than 100 messages.```")
        await asyncio.sleep(2)
        await msg.delete()
    else:
        await ctx.message.channel.purge(limit=num)
    
@bot.command()
@commands.has_role("Staff")
async def sendembed(ctx, *, s):
    em = discord.Embed.from_dict(json.loads(s))
    await ctx.send(embed = em)
    try:
        await ctx.message.delete()
    except:
        pass

"""
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        msg = await ctx.send(f'Error: `{error}`')
        await ctx.message.delete()
        await asyncio.sleep(10)
        await msg.delete()
    else:
        print(error)
"""
bot.run(config['token'])
