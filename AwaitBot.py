try:
    import os
    import discord
    from googleapiclient.discovery import build
    import requests
    from moment import utc
    from imdb import IMDb
    import asyncio
    import time
    import re
    from discord.ext import commands
    from discord.utils import get
    from discord.ext.commands import has_permissions, guild_only
    import discord.role
    from discord.ext.commands import check
except:
    os.system("pip install discord.py")
    os.system("pip install google-api-python-client")
    os.system("pip install requests")
    os.system("pip install moment")
    os.system("pip install imdbpy")
    os.system("slc")
intents = discord.Intents.default()
intents.members = True
ARTBot = commands.Bot(command_prefix="$", intents=intents)
ARTBot.remove_command("help")
token = 'NzUzOTQ2MDQyNTkyMDAyMDU4.X1tk-A.xXis4JheNzBVpNx5dGUTGEf7aFw'


@ARTBot.event
async def on_ready():
    print("[+] Successfully Login", ARTBot.user)
    print("[+] Bot Ready")
    print("=====================================")


@ARTBot.event
async def on_message(message):
    for x in message.mentions:
        if x == ARTBot.user:
            await message.channel.send(message.author.mention + ", My prefix is ``$``\n Iam Coded By <@602929951519408133>")
    await ARTBot.process_commands(message)
    urls = re.findall('discord.gg', message.content.lower())
    if urls:
        await message.channel.purge(limit=1)
        mutedRole = discord.utils.get(message.guild.roles, name="muted")
        await message.author.add_roles(mutedRole)
        embed = discord.Embed(title="muted", description=f"{message.author.mention} was Muted ",
                              colour=discord.Colour.random())
        embed2 = discord.Embed(title="ART2", colour=discord.Colour.random(),
                               description=" لا تنشر ريلاكس " + message.author.mention)
        embed2.set_footer(text="By await @_824", icon_url="https://www.upload.ee/image/13011911/72e9a040a03664e1749e39bd2a3ed554.png")
        embed2.set_thumbnail(url="https://www.upload.ee/image/13009848/117fc6beb243337783db3c63e2a8cbee.png")
        await message.channel.send(embed=embed2)
        await message.channel.send(embed=embed)


def in_voice_channel():  # check to make sure ctx.author.voice.channel exists
    def predicate(ctx):
        return ctx.author.voice and ctx.author.voice.channel
    return check(predicate)


@in_voice_channel()
@ARTBot.command()
@has_permissions(manage_messages=True)
async def move(ctx, Member: discord.Member, Member2: discord.Member = None):
    if Member2 is None:
        await Member.move_to(ctx.author.voice.channel)
    else:
        await Member.move_to(Member2.voice.channel)


@ARTBot.command()
async def server(ctx):
    role_count = len(ctx.guild.roles)
    member = ctx.guild.members
    onlineMember = list(filter(filterOnlyOnlineMembers, member))
    onlineMembersCount = len(onlineMember)
    embed = discord.Embed(timestamp=ctx.message.created_at, color=discord.Colour.random())
    embed.add_field(name='Name', value=f"{ctx.guild.name}", inline=True)
    embed.add_field(name='Owner', value=ctx.guild.owner.mention, inline=True)
    embed.add_field(name='Level Boost', value=str(ctx.guild.premium_tier), inline=True)
    embed.add_field(name='Server Boost', value=str(ctx.guild.premium_subscription_count), inline=True)
    embed.add_field(name='Highest role', value=ctx.guild.roles[-1], inline=True)
    embed.add_field(name='Number of roles', value=str(role_count), inline=True)
    embed.add_field(name=f'Numbers [{ctx.guild.member_count}]', value=f'[{onlineMembersCount}] Online', inline=True)
    embed.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=True)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    await ctx.send(embed=embed)


def filterOnlyOnlineMembers(member):
    return member.status != 'offline' and not member.bot


@ARTBot.command()
async def help(ctx):
    user_id = 602929951519408133
    user = discord.utils.get(ctx.guild.members, id=int(user_id))
    embed = discord.Embed(colour=discord.Colour.blue())
    embed.add_field(name='<:pencil:835493525457600554> Normal', value='```youtube: Display youtube channel information.\n'
                                                                      'avatar: Get user avatar.\n'
                                                                      'server: Get server detail\n'
                                                                      'users: Get info about member in discord.\n'
                                                                      'git: show github information.\n'
                                                                      'anime: Get info about anime in myanimelist.```', inline=False)
    embed.add_field(name='<:gear:835520233371336724> Moderation',
                    value='```roles: Add roles ot Member.\n'
                          'move: Move a member to another voice Channels.\n'
                          'ban: Ban a member from the server.\n'
                          'Clear: Delete a number of messages (max 100).\n'
                          'uBan: uBan a member from the server.\n'
                          'kick: kick a member from the server.\n'
                          'mute: Mute a member from the server.\n'
                          'unmute: unMute a member from the server.```', inline=False)
    embed.set_author(name="HELP Menu", icon_url=ctx.guild.icon_url)
    embed.set_footer(text="By await @_824",
                     icon_url=user.avatar_url)
    await ctx.channel.send(embed=embed)


@ARTBot.command()
async def users(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    embed = discord.Embed(colour=discord.Colour.random())
    embed.add_field(name='Nickname', value=member.name, inline=False)
    joined_at = re.compile('(.*?) (.*?)').search(str(member.joined_at))[1]
    created_at = re.compile('(.*?) (.*?)').search(str(member.created_at))[1]
    embed.add_field(name='Joined this Server At', value=utc(joined_at).format("dddd, MMMM, D YYYY"), inline=False)
    embed.add_field(name='Account Created At', value=utc(created_at).format("dddd, MMMM, D YYYY"), inline=False)
    embed.set_footer(text=member.status, icon_url="https://images-ext-2.discordapp.net/external/Pktl1WuJNhGlFWPydBCFUdWxfCTrc_o0BdX4Pqx0Lzw/https/emoji.gg/assets/emoji/7445_status_offline.png")
    embed.set_author(name=member.name + '#' + member.discriminator, icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    mention = []
    for role in member.roles:
        if role.name != "@everyone":
            mention.append(role.mention)
    b = ", ".join(mention)
    embed.add_field(name='roles', value=b, inline=False)
    await ctx.send(embed=embed)


@ARTBot.command()
@has_permissions(manage_messages=True)
async def roles(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    embed = discord.Embed(colour=discord.Colour.random(), description=f"<:white_check_mark:835493038595637298> Added {role} to {member.mention}")
    userAvatar = member.avatar_url
    embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    embed.set_thumbnail(url=userAvatar)
    await ctx.channel.send(embed=embed)


@ARTBot.command()
async def avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    embed = discord.Embed(colour=discord.Colour.random(), description=f"[Download]({member.avatar_url})")
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)


@ARTBot.command()
@has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.reply("You can't give yourself")
    else:
        mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
        await member.add_roles(mutedRole)
        embed = discord.Embed(title="muted", colour=discord.Colour.random(), description=f"<:white_check_mark:835493038595637298>  {ctx.author.name} you muted {member.mention}")
        embed.set_footer(text="By await @_824",
                         icon_url="https://www.upload.ee/image/13011911/72e9a040a03664e1749e39bd2a3ed554.png")
        await ctx.send(embed=embed)
        await member.send(f" you have been muted from: {ctx.guild.name} server")


@ARTBot.command()
@has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
    await member.remove_roles(mutedRole)
    embed = discord.Embed(title="UnMuted", colour=discord.Colour.random(),
                          description=f"<:white_check_mark:835493038595637298>  {member.mention} is now unmuted ")
    embed.set_footer(text="By await @_824",
                     icon_url="https://www.upload.ee/image/13011911/72e9a040a03664e1749e39bd2a3ed554.png")
    await ctx.send(embed=embed)
    await member.send(f" you have been UnMuted from: {ctx.guild.name} server")


@ARTBot.command()
@has_permissions(manage_messages=True)
async def clear(ctx, amount):
    amount = int(amount)
    await ctx.channel.purge(limit=amount)


@ARTBot.command()
@has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
    await user.kick(reason=reason)
    embed = discord.Embed(title=f":boot: Kicked {user.name}!", colour=discord.Colour.random(), description=f"Reason: {reason}\nBy: {ctx.author.mention}")
    await ctx.channel.send(embed=embed)
    await user.send(embed=embed)


@ARTBot.command()
@has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason):
    if reason is None:
        await ctx.reply("You did not write a reason")
    else:
        await user.ban(reason=reason)
        send = discord.Embed(title=f"banned {user.name}!", colour=discord.Colour.random(),
                             description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.channel.send(embed=send)
        await user.send(embed=send)


@ARTBot.command(name='unban')
@guild_only()
async def unban(ctx, id: int):
    user = await ARTBot.fetch_user(id)
    await ctx.guild.unban(user)
    send = discord.Embed(title=f"unBan {user.name}!", colour=discord.Colour.random())
    await ctx.channel.send(embed=send)


@ARTBot.command(pass_context=True)
async def youtube(ctx, name):
    request = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={name}&key=AIzaSyDYz8Y2r7IbZT8VChEUSOanOMnGu44jzGs&maxResults=1&type=channels").text
    title = re.compile('"title": "(.*?)"').search(request)[1]
    channelId = re.compile('"channelId": "(.*?)"').search(request)[1]
    pic = re.compile('"url": "(.*?)"').search(request)[1]
    publishTime = re.compile('"publishTime": "(.*?)"').search(request)[1]
    description = re.compile('"description": "(.*?)"').search(request)[1]
    youtube2 = build('youtube', 'v3', developerKey='AIzaSyDYz8Y2r7IbZT8VChEUSOanOMnGu44jzGs')
    ch_request = youtube2.channels().list(part='statistics', id=channelId)
    ch_response = ch_request.execute()
    sub = ch_response['items'][0]['statistics']['subscriberCount']
    vid = ch_response['items'][0]['statistics']['videoCount']
    views = ch_response['items'][0]['statistics']['viewCount']
    embed = discord.Embed(title="", colour=discord.Colour.random(),
                          description=title)
    embed.add_field(name='subscriberCount', value=sub, inline=False)
    embed.add_field(name='videoCount', value=vid, inline=True)
    embed.add_field(name='viewCount', value=views, inline=True)
    publishTime = re.compile('(.*?)T(.*?)').search(publishTime)[1]
    embed.add_field(name='join youtube', value=utc(publishTime).format("dddd, MMMM, D YYYY"), inline=False)
    embed.set_thumbnail(url=pic)
    embed.set_footer(text="By await @_824",
                     icon_url="https://www.upload.ee/image/13011911/72e9a040a03664e1749e39bd2a3ed554.png")
    await ctx.send(embed=embed)


@ARTBot.command(pass_context=True)
async def git(ctx, user):
    req = requests.get(f'https://api.github.com/users/{user}').text
    avatar_url = re.compile('"avatar_url":"(.*?)",').search(req)[1]
    Name = re.compile('"name":"(.*?)",').search(req)[1]
    twitter_username = re.compile('"twitter_username":(.*?),').search(req)[1]
    followers = re.compile('"followers":(.*?),').search(req)[1]
    following = re.compile('"following":(.*?),').search(req)[1]
    created_at = re.compile('"created_at":"(.*?)",').search(req)[1]
    blog = re.compile('"blog":"(.*?)",').search(req)[1]
    bio = re.compile('"bio":(.*?),').search(req)[1]
    public_repos = re.compile('"public_repos":(.*?),').search(req)[1]
    embed = discord.Embed(colour=discord.Colour.random())
    embed.set_author(name=user, icon_url=avatar_url)
    embed.set_footer(text="By await @_824",
                     icon_url="https://www.upload.ee/image/13011911/72e9a040a03664e1749e39bd2a3ed554.png")
    embed.add_field(name='Name', value=Name, inline=True)
    embed.add_field(name='bio', value=bio, inline=True)
    embed.add_field(name='Twitter', value=twitter_username, inline=False)
    embed.add_field(name='Blog', value=blog, inline=False)
    embed.add_field(name='Repositories', value=public_repos, inline=True)
    embed.add_field(name='followers', value=followers, inline=True)
    embed.add_field(name='following', value=following, inline=True)
    created_at = re.compile('(.*?)T(.*?)').search(created_at)[1]
    embed.add_field(name='Account Created', value=utc(created_at).format("dddd, MMMM, D YYYY"), inline=False)
    embed.set_thumbnail(url=avatar_url)
    await ctx.send(embed=embed)


@ARTBot.command()
async def anime(ctx, Name=None):
    if Name == None:
        pass
    req = requests.get(f"https://myanimelist.net/search/prefix.json?type=anime&keyword={Name}&v=1").text
    image_url = re.compile('"image_url":"(.*?)",').search(req)[1]
    avatar_url = image_url.replace('\\', "")
    url = re.compile('"url":"(.*?)",').search(req)[1]
    url = url.replace('\\', "")
    media_type = re.compile('"media_type":"(.*?)",').search(req)[1]
    start_year = re.compile('"start_year":(.*?),').search(req)[1]
    score = re.compile('"score":"(.*?)",').search(req)[1]
    status = re.compile('"status":"(.*?)"}').search(req)[1]
    Name = re.compile('"name":"(.*?)",').search(req)[1]
    req2 = requests.get(url).text
    rank = re.compile('<span class="dark_text">Ranked:</span>\n  (.*?)<sup>2</sup>').search(req2)[1]
    Members = re.compile('<span class="dark_text">Members:</span>\n    (.*?)\n</div>\n<div>').search(req2)[1]
    Episodes = re.compile('<span class="dark_text">Episodes:</span>\n  (.*?)\n  </div>').search(req2)[1]
    embed = discord.Embed(colour=discord.Colour.random())
    embed.set_author(name=Name, icon_url=avatar_url)
    embed.set_footer(text="By await @_824",
                     icon_url="https://www.upload.ee/image/13011911/72e9a040a03664e1749e39bd2a3ed554.png")
    embed.add_field(name='Name', value=Name, inline=True)
    embed.add_field(name='Episodes', value=Episodes, inline=True)
    embed.add_field(name='media_type', value=media_type, inline=False)
    embed.add_field(name='score', value=score, inline=True)
    embed.add_field(name='rank', value=rank, inline=True)
    embed.add_field(name='Members', value=Members, inline=True)
    embed.add_field(name='status', value=status, inline=False)
    embed.add_field(name='start_year', value=start_year, inline=False)
    embed.set_thumbnail(url=avatar_url)
    await ctx.send(embed=embed)


@roles.error
async def roles_error(ctx, error):
    embed = discord.Embed()
    embed.set_image(url="https://l.top4top.io/p_196047t081.jpg")
    await ctx.reply(embed=embed)


@mute.error
async def mute_error(ctx, error):
    embed = discord.Embed()
    embed.set_image(url="https://l.top4top.io/p_196047t081.jpg")
    await ctx.reply(embed=embed)


@unmute.error
async def unmute_error(ctx, error):
    embed = discord.Embed()
    embed.set_image(url="https://l.top4top.io/p_196047t081.jpg")
    await ctx.reply(embed=embed)


@clear.error
async def clear_error(ctx, error):
    embed = discord.Embed()
    embed.set_image(url="https://l.top4top.io/p_196047t081.jpg")
    await ctx.reply(embed=embed)


@kick.error
async def kick_error(ctx, error):
    embed = discord.Embed()
    embed.set_image(url="https://l.top4top.io/p_196047t081.jpg")
    await ctx.reply(embed=embed)


@ban.error
async def ban_error(ctx, error):
    embed = discord.Embed()
    embed.set_image(url="https://l.top4top.io/p_196047t081.jpg")
    await ctx.reply(embed=embed)


@unban.error
async def unban_error(ctx, error):
    embed = discord.Embed()
    embed.set_image(url="https://l.top4top.io/p_196047t081.jpg")
    await ctx.reply(embed=embed)


@move.error
async def move_error(ctx, error):
    embed = discord.Embed()
    embed.set_image(url="https://l.top4top.io/p_196047t081.jpg")
    await ctx.reply(embed=embed)


@git.error
async def git_error(ctx, error):
    await ctx.reply("i can't get any info from this user")


@youtube.error
async def youtube_error(ctx, error):
    await ctx.reply("i can't get any info from this channels")


ARTBot.run(token)
