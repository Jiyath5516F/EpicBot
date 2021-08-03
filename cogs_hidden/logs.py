"""
Copyright 2021 Nirlep_5252_

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import discord

from discord.ext import commands
from utils.embed import success_embed, error_embed
from utils.bot import EpicBot
from config import (
    COMMANDS_LOG_CHANNEL, ADD_REMOVE_LOG_CHANNEL,
    DM_LOG_CHANNEL, COOLDOWN_BYPASS, EMOJIS,
    PREFIX, MAIN_COLOR, EMPTY_CHARACTER, WEBSITE_LINK,
    SUPPORT_SERVER_LINK
)


class Logs(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client
        self.cmd_log_channel = self.client.get_channel(COMMANDS_LOG_CHANNEL)
        self.add_remove_log_channel = self.client.get_channel(ADD_REMOVE_LOG_CHANNEL)
        self.dm_log_channel = self.client.get_channel(DM_LOG_CHANNEL)

    @commands.Cog.listener(name="on_command_completion")
    async def add_cmd_used_count_user_profile(self, ctx: commands.Context):
        user_profile = await self.client.get_user_profile_(ctx.author.id)
        user_profile.update({"cmds_used": user_profile['cmds_used'] + 1})

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        if ctx.author.id in COOLDOWN_BYPASS:
            ctx.command.reset_cooldown(ctx)

        embed = success_embed(
            "Ah yes",
            "Some kid used me"
        ).add_field(name="Command:", value=f"```{ctx.message.content}```", inline=False
        ).add_field(name="User:", value=f"{ctx.author.mention}```{ctx.author}\n{ctx.author.id}```", inline=False
        ).add_field(name="Server:", value=f"```{ctx.guild}\n{ctx.guild.id}```", inline=False)
        await self.cmd_log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if str(message.channel.type) == 'private':
            files = []
            for e in message.attachments:
                uwu = await e.to_file()
                files.append(uwu)
            embed = success_embed(
                "New DM!",
                message.content
            ).add_field(
                name="Kid:",
                value=f"{message.author.mention}```{message.author}\n{message.author.id}```",
                inline=False
            )
            await self.dm_log_channel.send(embed=embed, files=files)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.client.get_guild_config(guild.id)
        embed = success_embed(
            f"{EMOJIS['add']}  EpicBot Added",
            f"""
**Server:** ```{guild} ({guild.id})```
**Owner:** {guild.owner.mention}```{guild.owner} ({guild.owner_id})```
**Members:** {guild.member_count}
**Humans:** {len(list(filter(lambda m: not m.bot, guild.members)))}
**Bots:** {len(list(filter(lambda m: m.bot, guild.members)))}
            """
        ).set_author(name=guild.owner, icon_url=guild.owner.avatar.url
        ).set_thumbnail(url=guild.icon.url)
        await self.add_remove_log_channel.send(embed=embed)

        send_embed = discord.Embed(
            title=f"{EMOJIS['wave_1']} Hi, UwU!~",
            description=f"""
Thank you very much for inviting me, I love you!~
My prefix is `{PREFIX}`, but you can change it to whatever you want!

Let me tell you more about me!

~ I am a simple, multipurpose bot designed to make your Discord life simpler.
~ I have a lot of amazing modules that you can discover by using the command `{PREFIX}help`
~ I leave the rest for you to discover... <:hehe:866211987716833300>

I hope you have a fun time with me, UwU!~
                        """,
            color=MAIN_COLOR
        ).set_thumbnail(url=self.client.user.avatar.url
        ).set_author(name=self.client.user.name, icon_url=self.client.user.avatar.url
        ).add_field(name=EMPTY_CHARACTER, value=f"[Invite EpicBot]({WEBSITE_LINK}/invite) | [Vote EpicBot]({WEBSITE_LINK}/vote) | [Support Server]({SUPPORT_SERVER_LINK})", inline=False)

        for channel in guild.channels:
            if "general" in channel.name:
                try:
                    return await channel.send(embed=send_embed)
                except Exception:
                    pass

        for channel in guild.channels:
            if "bot" in channel.name or "cmd" in channel.name or "command" in channel.name:
                try:
                    return await channel.send(embed=send_embed)
                except Exception:
                    pass

        for channel in guild.channels:
            try:
                return await channel.send(embed=send_embed)
            except Exception:
                pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        embed = error_embed(
            f"{EMOJIS['remove']}  EpicBot Removed",
            f"""
```yaml
Server: {guild} ({guild.id})
Owner: {guild.owner} ({guild.owner_id})
Members: {guild.member_count}
Humans: {len(list(filter(lambda m: not m.bot, guild.members)))}
Bots: {len(list(filter(lambda m: m.bot, guild.members)))}
```
            """
        )
        await self.add_remove_log_channel.send(embed=embed)
        for e in self.client.serverconfig_cache:
            if e['_id'] == guild.id:
                self.client.serverconfig_cache.remove(e)
                await self.client.serverconfig.delete_one({"_id": guild.id})
                return


def setup(client):
    client.add_cog(Logs(client))