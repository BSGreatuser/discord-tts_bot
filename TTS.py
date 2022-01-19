import discord, asyncio, random, os
from gtts import gTTS

token = 'token'

client = discord.Client()


@client.event
async def on_connect():
    if not os.path.isdir('text'):
        os.mkdir('text')
    print(client.user)


@client.event
async def on_message(message):
    if message.content == 'a퇴장':
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                await vc.disconnect()
        info = await message.reply('완료')
        await asyncio.sleep(3)
        await info.delete()

    if message.content.startswith('a') and not message.content == 'a퇴장':
        msg = message.content[1:]
        if len(msg) > 35:
            info = await message.reply('35자를 넘길 수 없습니다')
            await asyncio.sleep(3)
            await info.delete()
            return

        try:
            channel = message.author.voice.channel
        except:
            info = await message.reply('재생실패')
            await asyncio.sleep(3)
            await info.delete()
            return

        vc_client = discord.utils.get(client.voice_clients, guild=message.guild)
        if vc_client is None:
            vc = await channel.connect()
        else:
            vc = vc_client

        ttsmsg = gTTS(msg, lang='ko')
        nan = random.randint(0, 100)
        filename = f'text/{message.author.id}_{nan}.mp3'
        ttsmsg.save(filename)

        try:
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source=filename))
        except Exception as e:
            if str(e) == 'Already playing audio.':
                info = await message.reply('재생실패')
                await asyncio.sleep(3)
                await info.delete()

        os.remove(filename)


client.run(token)
