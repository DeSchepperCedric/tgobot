# Making a command

Go to `tgobot.py` and just above the last line : `bot.run(config['token'])` add the following lines:

```py
@bot.command(aliases = ['alias1', 'alias2'])
async def Command1(ctx):
    with open('data/CustomMenus.json', encoding = 'utf-8') as f:
        commands = json.loads(f.read())
    em = discord.Embed.from_dict(commands['Command1'])
    await ctx.send(embed = em)
```

Your `CustomMenus.json` file should look something like this:

```json
{
    "Command1" : {<Here goes the json you would send along with the -sendembed command.>},
    "Command2" : {<More json>},
    "Command3" : {<And so on>}
}
```

Notice how the last entry does not have a trailing `,`.

To add this command to the main menu, go to the `MainMenu.json` file and add an entry for it.
Then, go to `tgomenus.py` under the class `TGOMenu`. Now make the button for it like this:

```py
@menus.button('<BUTTON EMOJI HERE>')
async def button_name_here(self, payload):
    await self.ctx.invoke(self.bot.get_command('Command1'))
    await self.message.delete()
    self.stop()
```

You are all set.

A sample embed can look like this:

```json
{
    "title": "title ~~(did you know you can have markdown here too?)~~",
    "description": "this supports [named links](https://discordapp.com) on top of the previously shown subset of markdown. ```\nyes, even code blocks```",
    "url": "https://discordapp.com",
    "color": 5594390,
    "timestamp": "2020-11-02T20:31:02.141Z",
    "footer": {
      "icon_url": "https://cdn.discordapp.com/embed/avatars/0.png",
      "text": "footer text"
    },
    "thumbnail": {
      "url": "https://cdn.discordapp.com/embed/avatars/0.png"
    },
    "image": {
      "url": "https://cdn.discordapp.com/embed/avatars/0.png"
    },
    "author": {
      "name": "author name",
      "url": "https://discordapp.com",
      "icon_url": "https://cdn.discordapp.com/embed/avatars/0.png"
    },
    "fields": [
      {
        "name": "🤔",
        "value": "some of these properties have certain limits..."
      },
      {
        "name": "😱",
        "value": "try exceeding some of them!"
      }
    ]
  }
```