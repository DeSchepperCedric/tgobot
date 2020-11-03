# tgobot

Bot for TGO discord.

# Changing presence

Edit this line:
```py
await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{self.tgo.member_count} members | -tgo"))
```

To set status to "Playing"
```py
await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="<whatever you want here>")
```

To set status to "Streaming"
```py
await self.change_presence(activity=discord.Streaming(name="<whatever>", url="https://google.com"))
```
