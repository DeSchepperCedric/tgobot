import json
import datetime
import random
import asyncio

import discord
from discord.ext import commands, tasks, menus

from helpers import *

class TGOMenu(menus.Menu):
    def __init__(self, usermessagectx):
        super().__init__(timeout=180.0, delete_message_after=False, clear_reactions_after=False, check_embeds=False, message=None)
        self.userctx = usermessagectx

    async def send_initial_message(self, ctx, channel):
        with open('data/MainMenu.json', encoding = 'utf-8') as f:
            mainmenu = json.loads(f.read())
        em = discord.Embed(title='Helpdesk', color = randcolor())
        em.set_author(name=f'Hi, {ctx.message.author}!', icon_url=ctx.message.author.avatar_url)
        em.set_thumbnail(url=ctx.guild.icon_url)
        for option in mainmenu.keys():
            em.add_field(name = option, value=mainmenu[option], inline = False)
        await self.userctx.message.delete()
        return await ctx.send(embed = em)
        
    @menus.button('🌲')
    async def expert(self, payload):
        await self.ctx.invoke(self.bot.get_command('expert'))
        await self.message.delete()
        self.stop()

    @menus.button('📢')
    async def help(self, payload):
        await self.message.delete()
        await self.ctx.invoke(self.bot.get_command('staff'))
        self.stop()

    @menus.button('🏅')
    async def roles(self, payload):
        await self.message.delete()
        await self.ctx.invoke(self.bot.get_command('roles'))
        self.stop()

        

class ExpertMenu(menus.Menu):
    def __init__(self, usermessagectx):
        super().__init__(timeout=180.0, delete_message_after=False, clear_reactions_after=False, check_embeds=False, message=None)
        with open('data/ExpertMenu.json', encoding='utf-8') as f:
            self.mainmenu = json.loads(f.read())
        for button in expert_buttons(self, usermessagectx, self.mainmenu):
            self.add_button(button)


    async def send_initial_message(self, ctx, channel):

        em = discord.Embed(title='Experts', color = randcolor())
        em.set_author(name=f'Hi, {ctx.message.author}!', icon_url=ctx.message.author.avatar_url)
        em.set_thumbnail(url=ctx.guild.icon_url)
        for option in self.mainmenu.keys():
            em.add_field(name = f'{option} - {self.mainmenu[option]}', value=f'Call a {self.mainmenu[option].lower()} expert.', inline=False)
        self.ctx = ctx
        return await ctx.send(embed = em)

class RoleMenu(menus.Menu):
    def __init__(self, usermessagectx):
        super().__init__(timeout=180.0, delete_message_after=False, clear_reactions_after=False, check_embeds=False, message=None)
        with open('data/RoleMenu.json', encoding='utf-8') as f:
            self.mainmenu = json.loads(f.read())
        for button in role_buttons(self, usermessagectx, self.mainmenu):
            self.add_button(button)


    async def send_initial_message(self, ctx, channel):

        em = discord.Embed(title='Roles', color = randcolor())
        em.set_author(name=f'Hi, {ctx.message.author}!', icon_url=ctx.message.author.avatar_url)
        em.set_thumbnail(url=ctx.guild.icon_url)
        for option in self.mainmenu.keys():
            em.add_field(name = f'{option} - {self.mainmenu[option]}', value=f'Give yourself the {self.mainmenu[option]} role.', inline=False)
        self.ctx = ctx
        return await ctx.send(embed = em)
