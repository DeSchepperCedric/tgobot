# tgobot

Discord bot for The Great Outdoors server.
Join our server: https://discord.gg/ErtS8y4

# Features
-Advanced two-stage user verification system
-Ping staff members with cooldown
-Ping different helper/expert groups with cooldown
-Self-assign roles
-Request or apply for restricted roles
-Main embed menu for users to access commands graphically
-Snippets: create rich embeds and access them quickly with a custom command (examples: -faq, -rule3)
-Sendembed: quickly send custom embeds by pasting the JSON into chat
-Mute command with searchable log message sent to the desired channel
-Automate reward roles for Mee6 levels (without Mee6 Premium!)
-Control the bot's status message

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
