import random
import json

from discord.ext.menus import *
import discord

def randcolor():
    return random.randint(int('000000', 16), int('FFFFFF', 16))

def expert_buttons(menu, ctx, l : dict):
    buttons = list()
    for emoji in l.keys():
        role = discord.utils.get(ctx.channel.guild.roles, name=l[emoji])
        button = Button(emoji, get_expert_action(role, menu, ctx))
        buttons.append(button)
    return buttons

def get_expert_action(role, menu, ctx):
    async def b(self, payload):
        await ctx.send(f'{ctx.message.author.mention} needs {role.mention}!')
        await menu.message.delete()
    return b

def role_buttons(menu, ctx, l : dict):
    buttons = list()
    for emoji in l.keys():
        role = discord.utils.get(ctx.channel.guild.roles, name=l[emoji])
        button = Button(emoji, get_role_actions(role, menu, ctx))
        buttons.append(button)
    return buttons

def get_role_actions(role, menu, ctx):
    with open('data/specialroles.json', encoding='utf-8') as f:
        special_roles = json.loads(f.read())
    async def b(self, payload):
        if role.name in special_roles['special_roles']:
            em = discord.Embed(title = f'{ctx.message.author.name} applied for {role.name}', description = f'[View user profile!](https://discord.com/users/{ctx.message.author.id})', color = randcolor())
            em.set_thumbnail(url=ctx.message.author.avatar_url)
            await discord.utils.get(ctx.guild.channels, name='staff-log').send(content = menu.bot.staff_role.mention, embed = em)

            msg = await ctx.send('Applied for the role!')
        elif role not in ctx.message.author.roles:
            await ctx.message.author.add_roles(role)
            msg = await ctx.send('Gave you the role!')
        elif role in ctx.message.author.roles:
            await ctx.message.author.remove_roles(role)
            msg = await ctx.send('Removed the role!')
        await menu.message.delete()
        await asyncio.sleep(20)
        try: 
            await msg.delete()
        except: 
            pass
    return b
