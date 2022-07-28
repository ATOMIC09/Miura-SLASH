import asyncio
from datetime import datetime
from multiprocessing.spawn import import_main_path
from typing import Optional
import os
from cv2 import VideoWriter
import discord
from discord import app_commands
from discord.utils import get
import requests
import shutil
import gtts
import pdf2image
from youtube_dl import YoutubeDL
import json
import cv2

from utils import countdown_fn, imageprocess_fn, videoprocess_fn, youtubedl_fn, shorten_url, sectobigger, audio2video
from asset.lasereye import lasereye_fn

MY_GUILD = discord.Object(id=720687175611580426)  # replace with your guild id

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await client.change_presence(activity=discord.Game(name=f"💤 Standby..."))
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('----------------------------------------------------------')

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.all()
intents.members = True
client = MyClient(intents=intents)

client.name_only = ""
client.last_image = ""
client.last_video = ""
client.last_audio = ""
client.last_pdf = ""

client.last_image_url = ""
client.last_video_url = ""
client.last_audio_url = ""
client.last_pdf_url = ""

################################################# Help #################################################
@client.tree.command(description="❔ ความช่วยเหลือ")
async def help(interaction: discord.Interaction):
    # หน้าเมนู Embed
    util = discord.Embed(title="**❔ ช่วยเหลือ**",description="╰ *🔧 เครื่องมืออรรถประโยชน์*", color=0x40eefd)
    util.add_field(name="**⏰ นับเวลาถอยหลัง**", value="`/countdown`", inline=False)
    util.add_field(name="**🔌 นับถอยหลังและตัดการเชื่อมต่อ**", value="`/countdis`", inline=False)
    util.add_field(name="**🛡 ยกเว้นการตัดการเชื่อมต่อ**", value="`/except`", inline=False) 
    util.add_field(name="**👄 สังเคราะห์เสียง**", value="`/tts`", inline=False)
    util.add_field(name="**📄 แปลงเอกสารเป็นรูปภาพ**", value="`/pdftopng`", inline=False)
    util.add_field(name="**❌ ยกเลิกคำสั่ง**", value="`/cancel`", inline=False)

    music = discord.Embed(title="**❔ ช่วยเหลือ**",description="╰ *🎵 มีเดียและเพลง*", color=0xff3859)
    music.add_field(name="**📶 เรียกบอท**", value="`/music summon`", inline=False)
    music.add_field(name="**⏏️ เตะบอท**", value="`/music disconnect`", inline=False)
    music.add_field(name="**▶️ เล่นเสียง**", value="`/music play`", inline=False)
    music.add_field(name="**💾 เล่นเสียงผ่านไฟล์มีเดีย**", value="`/music plocal`", inline=False)
    music.add_field(name="**⏭ ข้าม**", value="`/music skip`", inline=False)
    music.add_field(name="**⏯ พักหรือเล่นต่อ**", value="`/music resume`", inline=False)
    music.add_field(name="**⏹ หยุด**", value="`/music stop`", inline=False)
    music.add_field(name="**🔢 คิวการเล่น**", value="`/music queue`", inline=False)
    music.add_field(name="**🆑 ล้างคิวทั้งหมด**", value="`/music clear`", inline=False)

    image = discord.Embed(title="**❔ ช่วยเหลือ**",description="╰ *🖼️ รูปภาพและการประมวลผลภาพ*", color=0x5be259)
    image.add_field(name="**🔦 ตรวจสอบคุณสมบัติ**", value="`/image info`", inline=False)
    image.add_field(name="**🔍 ค้นหาภาพคล้าย**", value="`/image reverse`", inline=False)
    image.add_field(name="**⬜ แปลงภาพสีเป็นภาพขาวดำ**", value="`/image grayscale`", inline=False)
    image.add_field(name="**🎨 แปลงภาพขาวดำเป็นภาพสี**", value="`/image colorize`", inline=False)
    image.add_field(name="**🧹 ลบพื้นหลังขาว**", value="`/image removebg`", inline=False)
    image.add_field(name="**📷 สร้าง QR Code**", value="`/image qr`", inline=False)
    image.add_field(name="**↔ ยืดภาพ**", value="`/image wide`", inline=False)
    image.add_field(name="**↔ ยืดดดดดภาพ**", value="`/image ultrawide`", inline=False)
    image.add_field(name="**👁 Laser Eye**", value="`/image laser`", inline=False)
    image.add_field(name="**🍳 Deep Fryer**", value="`/image deepfry`", inline=False)
    image.add_field(name="**🐶 Petpet Generator**", value="`/image pet`", inline=False)
    image.add_field(name="**📐 ปรับสเกลภาพ**", value="`/imagemaker scale`", inline=False)
    image.add_field(name="**📏 ปรับขนาดภาพ**", value="`/imagemaker resize`", inline=False)
    image.add_field(name="**✏ เขียนข้อความบนภาพ**", value="`/text`", inline=False)

    video = discord.Embed(title="**❔ ช่วยเหลือ**",description="╰ *🎥 การประมวลผลวิดีโอ*", color=0x4f4eca)
    video.add_field(name="**📹 ใส่เสียงในภาพ**", value="`/video imgaudio`", inline=False)
    video.add_field(name="**📺 ใส่เสียงจาก Youtube ในภาพ**", value="`/video imgyt`", inline=False)
    video.add_field(name="**🧲 ต่อคลิปวิดีโอ**", value="`/video videomix`", inline=False)

    download = discord.Embed(title="**❔ ช่วยเหลือ**",description="╰ *📦 ดาวน์โหลดไฟล์*", color=0xff80c9)
    download.add_field(name="**📺 Youtube Downloader**", value="`/download youtube`", inline=False)
    download.add_field(name="**🔊 Audio Downloader**", value="`/download audio`", inline=False)
    download.add_field(name="**🎞 Video Downloader**", value="`/download video`", inline=False)

    update = discord.Embed(title="**❔ ช่วยเหลือ**",description="╰ *📌 ประวัติการอัพเดท*", color=0xdcfa80)
    update.add_field(name="1️⃣ V 2.0 | 07/11/2021", value="• Add: Countdown\n• Add: PrivateKey\n• Add: Mute\n• Add: YT Downloader\n• Add: Music Player\n• Add: Image Processing")
    update.add_field(name="2️⃣ V 2.1 | 12/11/2021", value="• Add: Audio and Video Downloader")
    update.add_field(name="3️⃣ V 2.2 | 29/11/2021", value="• Add: Image Processing\n• Add: Countdown and Disconnect\n• Add: PDF To PNG Converter\n• Add: Play Audio (Local)\n• Fix: Prefix")
    update.add_field(name="4️⃣ V 2.3 | 17/12/2021", value="• Add: Remove Background\n• Add: AutoSave Attachment\n• Add: Resize (width x height)\n• Add: Read Last Attachment\n• Fix: Alpha Channel for Image Processing")
    update.add_field(name="5️⃣ V 2.4 | 20/12/2021", value="• Add: Text on Image\n• Add: Grayscale to Color\n• Add: Deep Fryer\n• Fix: Countdown Style\n• Fix: Cancel Command\n• Delete: PrivateKey")
    update.add_field(name="6️⃣ V 2.5 | 12/01/2022", value="• Add: Scamming Protection V1\n• Add: Role Selector\n• Fix: มี Model ของ %color แล้ว")
    update.add_field(name="7️⃣ V 2.6 | 21/01/2022", value="• Add: Earrape Warning\n• Add: Video Processing")
    update.add_field(name="8️⃣ V 2.7 | 09/02/2022", value="• Add: Laser Eye Meme\n• Add: Text to Speech\n• Add: Image Properties\n• Add: Image Processing\n• Add: Video Processing")
    update.add_field(name="9️⃣ V 2.8 | 26/03/2022", value="• Add: Hosting Server Status\n• Add: Countdis Exception\n• Add: QR Code Generator\n• Add: เปลี่ยนระบบเลือกบทบาท\n• Add: ระบบแปลคำเพี้ยน")
    update.add_field(name="9️⃣ V 3.0 | 26/03/2022", value="**รอการอัพเดท**")

    select = discord.ui.Select(placeholder="ตัวเลือกเมนู",options=[
    discord.SelectOption(label="เครื่องมืออรรถประโยชน์",emoji="🔧",description="คำสั่งการใช้งานทั่วไป",value="util",default=False),
    discord.SelectOption(label="มีเดียและเพลง",emoji="🎵",description="คำสั่งการใช้งานเสียงและเพลง",value="music",default=False),
    discord.SelectOption(label="รูปภาพและการประมวลผลภาพ",emoji="🖼️",description="คำสั่งการใช้งานรูปภาพ",value="image",default=False),
    discord.SelectOption(label="การประมวลผลวิดีโอ",emoji="🎥",description="คำสั่งการใช้งานการประมวลผลวิดีโอ",value="video",default=False),
    discord.SelectOption(label="ดาวน์โหลดไฟล์",emoji="📦",description="คำสั่งการใช้งานดาวน์โหลดไฟล์",value="download",default=False),
    discord.SelectOption(label="ประวัติการอัพเดท",emoji="📌",description="คำสั่งตรวจสอบเวอร์ชันของบอท",value="update",default=False)
    ])

    async def my_callback(interaction):
        if select.values[0] == "util":
            await interaction.response.edit_message(embed=util)

        elif select.values[0] == "music":
            await interaction.response.edit_message(embed=music)
        
        elif select.values[0] == "image":
            await interaction.response.edit_message(embed=image)

        elif select.values[0] == "video":
            await interaction.response.edit_message(embed=video)

        elif select.values[0] == "download":
            await interaction.response.edit_message(embed=download)

        elif select.values[0] == "update":
            await interaction.response.edit_message(embed=update)
            
    select.callback = my_callback
    view = discord.ui.View()
    view.add_item(select)

    await interaction.response.send_message(embed=util, view=view)


################################################# Countdown #################################################
client.timestop1 = 0
@client.tree.command(description="⏰ นับถอยหลัง")
@app_commands.describe(time="ใส่เวลาเป็นหน่วยวินาที")
async def countdown(interaction: discord.Interaction, time: str):
    time_int = int(time)
    client.timestop1 = time_int

    if time_int < 0:
        await interaction.response.send_message("**เวลาไม่ถูกต้อง ❌**")
    else:
        output = countdown_fn.countdown_fn(time_int)
        await interaction.response.send_message(output)
        for i in range(time_int):
            output = countdown_fn.countdown_fn(time_int)
            await interaction.edit_original_message(content=output)
            await asyncio.sleep(1)
            time_int -= 1

            if client.timestop1 == -22052603:
                await interaction.edit_original_message(content="**การนับถอยหลังถูกยกเลิก 🛑**")
                break
        if client.timestop1 != -22052603:
            await interaction.edit_original_message(content="**หมดเวลา 🔔**")


################################################# Countdis #################################################
client.timestop2 = 0
client.member_except = []
@client.tree.command(description="⏱️ นับถอยหลังและตัดการเชื่อมต่อ")
@app_commands.describe(time="ใส่เวลาเป็นหน่วยวินาที")
async def countdis(interaction: discord.Interaction, time: str):
    people_counter = 0

    time_int = int(time)
    client.timestop2 = time_int

    if time_int < 0:
        await interaction.response.send_message("**เวลาไม่ถูกต้อง ❌**")
    else:
        output = countdown_fn.countdown_fn(time_int)
        await interaction.response.send_message(output)
        for i in range(time_int):
            output = countdown_fn.countdown_fn(time_int)
            await interaction.edit_original_message(content=output)
            await asyncio.sleep(1)
            time_int -= 1

            if client.timestop2 == -22052603:
                await interaction.edit_original_message(content="**การนับถอยหลังถูกยกเลิก 🛑**")
                break
        if client.timestop2 != -22052603:
            try:
                members = interaction.user.voice.channel.members
                channel = interaction.user.voice.channel
            
                await interaction.edit_original_message(content="**หมดเวลา 🔔**")
                
                if client.member_except == []: # ไม่มีใครยกเว้น
                    members = interaction.user.voice.channel.members
                    for member in members:
                        await member.move_to(None)
                        people_counter += 1

                    client.member_except = []
                    await interaction.followup.send(f"⏏️  **ตัดการเชื่อมต่อจำนวน {people_counter} คน จาก `{channel}` สำเร็จแล้ว**")

                else:
                    members = interaction.user.voice.channel.members
                    for member in members:
                        if member not in client.member_except: # เช็คว่าใครไม่ออก
                            await member.move_to(None)
                            people_counter += 1

                    await interaction.followup.send(f"⏏️  **ตัดการเชื่อมต่อจำนวน {people_counter} คน จาก `{channel}` สำเร็จแล้ว**")
                    
            except:
                await interaction.edit_original_message(content="**ℹ ต้องอยู่ในช่องเสียงก่อน จึงจะสามารถใช้ได้**")


################################################# Except #################################################
client.last_use = [0]

@client.tree.command(name="except",description="⛔ ยกเว้นคำสั่ง Countdis")
async def except_def(interaction: discord.Interaction):
    user = interaction.user
    if user.id not in client.last_use:
        client.member_except.append(user) # คนที่จะไม่ออก
        client.last_use.pop(0)
        client.last_use.append(user.id)
        await interaction.response.send_message(content=f"**<@{user.id}> ได้รับการยกเว้น <:Approve:921703512382009354>**")
    else:
        client.member_except.remove(user) # คนที่จะไม่ออก
        client.last_use.pop(0)
        client.last_use.append(0)
        await interaction.response.send_message(content=f"**<@{user.id}> ถูกลบออกจากรายการที่ยกเว้น <:Deny:921703523111022642>**")


################################################# Send Message #################################################
@client.tree.command(description="📨 ส่งข้อความ (เฉพาะเจ้าของ)")
@app_commands.describe(channel="ช่องข้อความที่จะส่ง",message="ข้อความ")
async def send(interaction: discord.Interaction, channel: discord.TextChannel, *, message: str):
    if interaction.user.id == 269000561255383040:
        await interaction.response.send_message(content=f'"{message}" ถูกส่งไปยัง {channel.mention}')
        await channel.send(message)
    else:
        await interaction.response.send_message(content="**แกไม่มีสิทธิ์!**")


################################################# TTS #################################################
@client.tree.command(description="🗣️ แปลงข้อความเป็นเสียง")
@app_commands.choices(language=[
    app_commands.Choice(name="🇿🇦 Afrikaans (South Africa)",value="af"),
    app_commands.Choice(name="🇩🇰 Danish (Denmark)",value="da"),
    app_commands.Choice(name="🇧🇪 Dutch (Belgium)",value="nl"),
    app_commands.Choice(name="🇺🇸 English (US)",value="en"),
    app_commands.Choice(name="🇫🇮 Finnish (Finland)",value="fi"),
    app_commands.Choice(name="🇫🇷 French (France)",value="fr"),
    app_commands.Choice(name="🇩🇪 German (Germany)",value="de"),
    app_commands.Choice(name="🇮🇳 Gujarati (India)",value="gu"),
    app_commands.Choice(name="🇮🇳 Hindi (India)",value="hi"),
    app_commands.Choice(name="🇮🇩 Indonesian (Indonesia)",value="id"),
    app_commands.Choice(name="🇮🇹 Italian (Italy)",value="it"),
    app_commands.Choice(name="🇯🇵 Japanese (Japan)",value="ja"),
    app_commands.Choice(name="🇰🇷 Korean (South Korea)",value="ko"),
    app_commands.Choice(name="🇲🇾 Malay (Malaysia)	",value="ms"),
    app_commands.Choice(name="🇧🇷 Portuguese (Brazil)",value="pt"),
    app_commands.Choice(name="🇷🇴 Romanian (Romania)",value="ro"),
    app_commands.Choice(name="🇷🇺 Russian (Russia)",value="ru"),
    app_commands.Choice(name="🇷🇸 Serbian (Serbia)",value="sr"),
    app_commands.Choice(name="🇸🇰 Slovak (Slovakia)",value="sk"),
    app_commands.Choice(name="🇪🇸 Spanish (Spain)",value="es"),
    app_commands.Choice(name="🇸🇪 Swedish (Sweden)",value="sv"),
    app_commands.Choice(name="🇹🇭 Thai (Thailand)",value="th"),
    app_commands.Choice(name="🇺🇦 Ukrainian (Ukraine)",value="uk"),
    app_commands.Choice(name="🇻🇳 Vietnamese (Vietnam)",value="vi"),
    ])

@app_commands.describe(language="ภาษาของเสียงพูด",text="ข้อความ")
async def tts(interaction: discord.Interaction,language: discord.app_commands.Choice[str] ,* , text: str):
    tts = gtts.gTTS(text=text,lang=language.value)
    tts.save(f'temp/audio/tts_{language.value}.mp3')

    file = discord.File(f'temp/audio/tts_{language.value}.mp3')
    await interaction.response.send_message(file=file)


################################################# PDF to PNG #################################################
@client.tree.command(description="📄 แปลงเอกสาร PDF เป็นรูปภาพ")
@app_commands.choices(
    zipped=[
    app_commands.Choice(name="✅ Yes | เหมาะกับเอกสาร 4 หน้าขึ้นไป",value="1"),
    app_commands.Choice(name="❌ No | เหมาะกับเอกสารไม่เกิน 3 หน้า (จากนั้นจะส่งกลับช้า)",value="0")])
@app_commands.choices(
    extension=[
    app_commands.Choice(name="PNG | คุณภาพสูง ขนาดไฟล์ใหญ่กว่า",value="png"),
    app_commands.Choice(name="JPG | คุณภาพปานกลาง ขนาดไฟล์เล็กกว่า",value="jpg")])

@app_commands.describe(zipped="ต้องการบีบอัดเป็นไฟล์เดียวหรือไม่",extension="นามสกุลของรูปภาพที่ต้องการ",filename="ตั้งชื่อไฟล์ (ไม่ต้องตั้งก็ได้)")
async def pdftoimage(interaction: discord.Interaction,zipped: discord.app_commands.Choice[str], extension: discord.app_commands.Choice[str], filename: Optional[str]):
    outfilename = filename or client.last_pdf.split(".")[0]

    try:
        await interaction.response.send_message("**🔁  กำลังแปลงเป็นรูปภาพ...**")
        pages = pdf2image.convert_from_path(f"temp/autosave/{client.last_pdf}", 200)
    except:
        await interaction.response.send_message("**⚠️ ไม่พบไฟล์เอกสาร**")
        return

    if extension.value == "png":
        extensionUPPER = "PNG"
    elif extension.value == "jpg":
        extensionUPPER = "JPEG"

    if zipped.value == "0":
        for i in range(len(pages)):
            pages[i].save(f'temp/document/{outfilename}_page{i+1}.{extension.value}', extensionUPPER)
            file = discord.File(f"temp/document/{outfilename}_page{i+1}.{extension.value}")
            await interaction.followup.send(file=file)

    elif zipped.value == "1":
        for i in range(len(pages)):
            pages[i].save(f'temp/document/{outfilename}_page{i+1}.{extension.value}', extensionUPPER)
        
        await interaction.followup.send(f"**🗜️ กำลังบีบไฟล์...**")
        shutil.make_archive(f"{outfilename}", 'zip', 'temp/document')
        shutil.move(f"{outfilename}.zip", f"temp/compressed/{outfilename}.zip")

        try:
            file = discord.File(f"temp/compressed/{outfilename}.zip")
            await interaction.followup.send(file=file)
        except:
            size = os.path.getsize(f"temp/compressed/{outfilename}.zip")/1000000
            await interaction.followup.send("**📦 ไฟล์ใหญ่เกินไป** ({:.2f}MB)".format(size))

        await asyncio.sleep(10)
        for i in range(len(pages)):
            os.remove(f"temp/document/{outfilename}_page{i+1}.{extension.value}")


################################################# Music #################################################
client.queue = []
client.queue_name = []
client.queue_notdel = []

@client.tree.command(name="music",description="🎵 มีเดียและเพลง")
@app_commands.choices(command=[
    app_commands.Choice(name="📶 เรียกบอท",value="summon"),
    app_commands.Choice(name="⏏️ เตะบอท",value="disconnect"),
    app_commands.Choice(name="▶️ เล่นเสียง (Youtube)",value="play"),
    app_commands.Choice(name="💾 เล่นเสียงผ่านไฟล์มีเดีย",value="plocal"),
    app_commands.Choice(name="⏭ ข้าม",value="skip"),
    app_commands.Choice(name="⏯ พักหรือเล่นต่อ",value="resume"),
    app_commands.Choice(name="⏹ หยุด",value="stop"),
    app_commands.Choice(name="🔢 คิวการเล่น",value="queue"),
    app_commands.Choice(name="🆑 ล้างคิวทั้งหมด",value="clear"),
    ])

@app_commands.describe(command="เลือกคำสั่งที่ต้องการ",link="ใช้งานคู่กับคำสั่งเล่นเสียง (Youtube)")
async def music(interaction: discord.Interaction, command: discord.app_commands.Choice[str], link: Optional[str]):
    try:
        voice_channel = interaction.user.voice.channel
        voice = get(client.voice_clients, guild=interaction.guild)
    except:
        await interaction.response.send_message("**⚠️ คุณยังไม่ได้เข้าร่วมช่องเสียง**")
        return


    if command.value == "summon":
        if voice and voice.is_connected():
            await voice.move_to(voice_channel)
        else:
            voice = await voice_channel.connect()


    elif command.value == "disconnect":
        voice_client = interaction.guild.voice_client
        await voice_client.disconnect()
    

    elif command.value == "play":
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'outtmpl': '%(title)s'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        if voice and voice.is_connected():
            await voice.move_to(voice_channel)
        else:
            voice = await voice_channel.connect()

        client.queue.append(link)

        await interaction.response.send_message(f"🔎 **กำลังหา** `{link}`")
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(client.queue[0], download=False)
            filename = ydl.prepare_filename(info)
        
        thumbnail_dict = info['thumbnails']
        thumbnail = thumbnail_dict[len(thumbnail_dict)-1]['url']
        URL = info['url']
        client.queue_notdel.append(filename)
        client.queue_name.append(filename)
        await interaction.edit_original_message(content=f"👀 **พบ** `{filename}`")
        
        if voice.is_playing() == 1:
            await asyncio.sleep(2)
            await interaction.edit_original_message(content=f"✅ **เพิ่ม** `{filename}` **ไปยังคิวเรียบร้อย**")

        while int(voice.is_playing()) == 0:
            player = discord.Embed(title='🎵 Media Player', color=0xff3859)
            player.description = f"**กำลังเล่น** {client.queue_name[0]}"
            player.set_thumbnail(url=thumbnail)
            player.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
            player.timestamp = interaction.created_at

            await interaction.edit_original_message(content="",embed=player)

            voice.play(discord.FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS))

            client.queue.pop(0)
            client.queue_name.pop(0)


    elif command.value == "plocal":
        if voice and voice.is_connected():
            await voice.move_to(voice_channel)
        else:
            voice = await voice_channel.connect()

        timeoflastmodifiedvideo = os.path.getmtime(f"temp/autosave/{client.last_video}")
        timeoflastmodifiedaudio = os.path.getmtime(f"temp/autosave/{client.last_audio}")

        if client.last_video != "" and client.last_audio != "": # มีไฟล์ทั้งคู่
            if timeoflastmodifiedaudio > timeoflastmodifiedvideo:   # เลือกไฟล์ที่ใหม่กว่า
                shutil.copy(f"temp/autosave/{client.last_audio}", f"temp/plocal/{client.last_audio}")
                voice.play(discord.FFmpegPCMAudio(source=f'temp/plocal/{client.last_audio}'))

                await interaction.response.send_message(f"▶️ **กำลังเล่น** `{client.last_audio}`")
            else:
                shutil.copy(f"temp/autosave/{client.last_video}", f"temp/plocal/{client.last_video}")
                voice.play(discord.FFmpegPCMAudio(source=f'temp/plocal/{client.last_video}'))

                await interaction.response.send_message(f"▶️ **กำลังเล่น** `{client.last_video}`")

        elif client.last_audio != "" and client.last_video == "": # มีเฉพาะไฟล์เสียง
            shutil.copy(f"temp/autosave/{client.last_audio}", f"temp/plocal/{client.last_audio}")
            voice.play(discord.FFmpegPCMAudio(source=f'temp/plocal/{client.last_audio}'))

            await interaction.response.send_message(f"▶️ **กำลังเล่น** `{client.last_audio}`")

        elif client.last_video != "" and client.last_audio == "": # มีเฉพาะไฟล์วิดีโอ
            shutil.copy(f"temp/autosave/{client.last_video}", f"temp/plocal/{client.last_video}")
            voice.play(discord.FFmpegPCMAudio(source=f'temp/plocal/{client.last_video}'))

            await interaction.response.send_message(f"▶️ **กำลังเล่น** `{client.last_video}`")


    elif command.value == "skip":
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'outtmpl': '%(title)s'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        try:
            voice.stop()
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(client.queue[0], download=False)
            URL = info['url']
            voice.play(discord.FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            await interaction.response.send_message('⏩ **ข้าม**')
            client.queue.pop(0)
            client.queue_name.pop(0)
            client.queue_notdel.pop(0)
        except:
            await interaction.response.send_message("❌ **ไม่เจอเพลงในคิว**")
            client.queue_name.clear()
            client.queue_notdel.clear()

    
    elif command.value == "resume":
        if voice.is_paused():
            voice.resume()
            await interaction.response.send_message('▶️ **เล่นต่อ**')
        else:
            voice.pause()
            await interaction.response.send_message('⏸ **พัก**')

    
    elif command.value == "stop":
        if voice.is_playing():
            voice.stop()
            await interaction.response.send_message('⏹ **หยุด**')

    
    elif command.value == "queue":
        number_emoji = [":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:",":keycap_ten:"]
        data = ""

        if len(client.queue_notdel) != 0:
            for i in range(len(client.queue_notdel)):
                try:
                    number_title = number_emoji[i]
                except: 
                    client.queue_notdel.clear()
                    number_title = number_emoji[i]
                music_name = client.queue_notdel[i]
                data += f"{number_title} {music_name}\n"
                
            queue = discord.Embed(title = "🔢 **Queue**", color = 0xff3859)
            queue.description = data
            queue.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
            queue.timestamp = interaction.created_at

            await interaction.response.send_message(embed=queue)
        else:
            await interaction.response.send_message("🗑️ **ไม่มีเพลงในคิว**")


    elif command.value == "clear":
        client.queue.clear()
        client.queue_name.clear()
        client.queue_notdel.clear()
        await interaction.response.send_message("🆑 **ล้างคิวแล้ว**")


################################################# Image Process #################################################
@client.tree.command(name="image",description="🖼️ รูปภาพและการประมวลผลภาพ")
@app_commands.choices(command=[
    app_commands.Choice(name="🔦 ตรวจสอบคุณสมบัติ",value="info"),
    app_commands.Choice(name="🔍 ค้นหาภาพคล้าย",value="reverse"),
    app_commands.Choice(name="⬜ แปลงภาพสีเป็นภาพขาวดำ",value="grayscale"),
    app_commands.Choice(name="🎨 แปลงภาพขาวดำเป็นภาพสี",value="colorize"),
    app_commands.Choice(name="🧹 ลบพื้นหลังขาว",value="removebg"),
    app_commands.Choice(name="📷 สร้าง QR Code",value="qr"),
    app_commands.Choice(name="↔ ยืดภาพ",value="wide"), 
    app_commands.Choice(name="↔ ยืดดดดดภาพ",value="ultrawide"),
    app_commands.Choice(name="👁 Laser Eye",value="laser"),
    app_commands.Choice(name="🍳 Deep Fryer",value="deepfry"),
    app_commands.Choice(name="🐶 Petpet Generator",value="pet"),
    ])

@app_commands.describe(command="เลือกคำสั่งที่ต้องการ",text="ใช้งานคู่กับคำสั่ง สร้าง QR Code")
async def image(interaction: discord.Interaction, command: discord.app_commands.Choice[str], text: Optional[str]):
    if command.value == "qr":
        imageprocess_fn.qr(text)
        await interaction.response.send_message(file=discord.File("temp/autosave/miura_qr.png"))
        os.remove("temp/autosave/miura_qr.png")

    if client.last_image == "":
        await interaction.response.send_message("❌ **ไม่เจอรูปภาพ**")
        return
    else:
        if command.value == "info":
            channel = imageprocess_fn.imginfo_channel(f"temp/autosave/{client.last_image}")
            height = imageprocess_fn.imginfo_height(f"temp/autosave/{client.last_image}")
            width = imageprocess_fn.imginfo_width(f"temp/autosave/{client.last_image}")

            size = os.path.getsize(f"temp/autosave/{client.last_image}")/1000000
            if size < 1:
                size = os.path.getsize(f"temp/autosave/{client.last_image}")/1000
                if size < 1:
                    size = os.path.getsize(f"temp/autosave/{client.last_image}")
                    size = f"{size} Bytes"
                else:
                    size = f"{size} KB"
            else:
                size = f"{size} MB"

            info = discord.Embed(title = "**🔦 คุณสมบัติรูปภาพ**", color = 0x5be259)
            info.timestamp = interaction.created_at
            info.add_field(name="🖨️ ชื่อไฟล์", value=f"`{client.last_image}`", inline=False)
            info.add_field(name="📂 ขนาดไฟล์", value=f"`{size}`", inline=False)
            info.add_field(name="🌈 ช่อง", value=f"`{channel}`", inline=False)
            info.add_field(name="📏 ความกว้าง", value=f"`{width} pixels`", inline=False)
            info.add_field(name="📐 ความสูง", value=f"`{height} pixels`", inline=False)
            info.add_field(name="🪄 ความละเอียด", value=f"`{width}x{height}`", inline=False)
            await interaction.response.send_message(embed=info)

        
        elif command.value == "reverse":
            filePath = f"temp/autosave/{client.last_image}"
            searchUrl = 'https://yandex.com/images/search'
            files = {'upfile': ('blob', open(filePath, 'rb'), 'image/jpeg')}
            params = {'rpt': 'imageview', 'format': 'json', 'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
            response = requests.post(searchUrl, params=params, files=files)
            query_string = json.loads(response.content)['blocks'][0]['params']['url']
            img_search_url= searchUrl + '?' + query_string

            search = discord.Embed(title = "**🔦 คุณสมบัติรูปภาพ**", color = 0x5be259)
            search.set_thumbnail(url=client.last_image_url)
            search.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
            search.timestamp = interaction.created_at

            url_view = discord.ui.View()
            url_view.add_item(discord.ui.Button(label='Result',emoji="🔎",style=discord.ButtonStyle.url, url=img_search_url))

            await interaction.response.send_message(embed=search, view=url_view)


        elif command.value == "grayscale":
            imageprocess_fn.grayscale(f"temp/autosave/{client.last_image}")
            await interaction.response.send_message(file=discord.File(f"temp/autosave/{client.last_image}"))

        
        elif command.value == "colorize":
            imageprocess_fn.colorize(f"temp/autosave/{client.last_image}")
            await interaction.response.send_message(file=discord.File(f"temp/autosave/{client.last_image}"))


        elif command.value == "removebg":
            imageprocess_fn.removebg(f"temp/autosave/{client.last_image}")
            await interaction.response.send_message(file=discord.File(f"temp/autosave/{client.last_image}"))


        elif command.value == "wide":
            imageprocess_fn.wide(f"temp/autosave/{client.last_image}",2)
            await interaction.response.send_message(file=discord.File(f"temp/autosave/{client.last_image}"))


        elif command.value == "ultrawide":
            imageprocess_fn.wide(f"temp/autosave/{client.last_image}",4)
            await interaction.response.send_message(file=discord.File(f"temp/autosave/{client.last_image}"))

        
        elif command.value == "laser":
            shutil.copy(f"temp/autosave/{client.last_image}", f"asset/lasereye/input/{client.last_image}")
            lasereye_fn.imagecov(client.last_image,1.5,client.name_only)
            await interaction.response.send_message("**👁 กำลังสร้าง...**")

            if "_laser" in client.name_only:
                file_name = discord.File(f"asset/lasereye/output/{client.name_only}.png")
                await interaction.followup.send(file=file_name)
            else:
                file_name = discord.File(f"asset/lasereye/output/{client.name_only}_laser.png")
                print(f"asset/lasereye/output/{client.name_only}_laser.png")
                await interaction.followup.send(file=file_name)
                

        elif command.value == "deepfry":
            shutil.copy(f"temp/autosave/{client.last_image}", f"asset/deepfry/deepfryer_input/{client.last_image}")
            imageprocess_fn.deepfry(f"asset/deepfry/deepfryer_input/{client.last_image}")

            if "_deepfryer" in client.name_only:
                file_name = discord.File(f"asset/deepfry/deepfryer_output/{client.name_only}.png")
                await interaction.response.send_message(file=file_name)
            else:
                file_name = discord.File(f"asset/deepfry/deepfryer_output/{client.name_only}_deepfryer.png")
                await interaction.response.send_message(file=file_name)
            
        elif command.value == "pet":
            imageprocess_fn.petpet_def(f"temp/autosave/{client.last_image}",client.name_only)

            file_name = discord.File(f"temp/autosave/{client.name_only}_petpet.gif")
            await interaction.response.send_message(file=file_name)
            await asyncio.sleep(2)


################################################# Image Maker #################################################
@client.tree.command(name="imagemaker",description="📸 การสร้างรูปภาพ")
@app_commands.choices(command=[
    app_commands.Choice(name="📐 ปรับสเกลภาพ (ระบุ info เป็นตัวเลข เช่น 500%)",value="scale"), #int %
    app_commands.Choice(name="📏 ปรับขนาดภาพ (ระบุ info เป็นขนาดของภาพ เช่น 1920x1080)",value="resize")]) #width,height
    
@app_commands.describe(command="เลือกคำสั่งที่ต้องการ",info="ใส่ข้อมูลตามคำสั่งที่เลือก")
async def imagemaker(interaction: discord.Interaction, command: discord.app_commands.Choice[str], info: str):
    if command.value == "scale":
        if "%" in info:
            scale = int(info.replace("%",""))
        else:
            scale = int(info)
        
        imageprocess_fn.scale(f"temp/autosave/{client.last_image}",scale)
        file_name = discord.File(f"temp/autosave/{client.last_image}")
        await interaction.response.send_message(file=file_name)

    elif command.value == "resize":
        width, height = info.split("x")
        imageprocess_fn.resize(f"temp/autosave/{client.last_image}",int(width),int(height))
        file_name = discord.File(f"temp/autosave/{client.last_image}")
        await interaction.response.send_message(file=file_name)


################################################# Text #################################################
@client.tree.command(name="text",description="🖊️ เขียนข้อความลงบนภาพ")
@app_commands.choices(font=[
    app_commands.Choice(name="0 FONT_HERSHEY_SIMPLEX",value="FONT_HERSHEY_SIMPLEX"),
    app_commands.Choice(name="1 FONT_HERSHEY_PLAIN",value="FONT_HERSHEY_PLAIN"),
    app_commands.Choice(name="2 FONT_HERSHEY_DUPLEX",value="FONT_HERSHEY_DUPLEX"),
    app_commands.Choice(name="3 FONT_HERSHEY_COMPLEX",value="FONT_HERSHEY_COMPLEX"),
    app_commands.Choice(name="4 FONT_HERSHEY_TRIPLEX",value="FONT_HERSHEY_TRIPLEX"),
    app_commands.Choice(name="5 FONT_HERSHEY_COMPLEX_SMALL",value="FONT_HERSHEY_COMPLEX_SMALL"),
    app_commands.Choice(name="6 FONT_HERSHEY_SCRIPT_SIMPLEX",value="FONT_HERSHEY_SCRIPT_SIMPLEX"),
    app_commands.Choice(name="7 FONT_HERSHEY_SCRIPT_COMPLEX",value="FONT_HERSHEY_SCRIPT_COMPLEX"),
    ])

@app_commands.describe(text="ใส่ข้อความ", font="เลือกฟอนต์ของข้อความ", color='สีของข้อความ เช่น (0, 0, 255) หรือ "แดง" (เรียงสีแบบ BGR)', size="ขนาดของข้อความ เช่น 5", position="ตำแหน่งของข้อความ เช่น floor หรือ 1.2", thickness="ความหนาของข้อความ เช่น 3")
async def text_def(interaction: discord.Interaction, text: str, font: discord.app_commands.Choice[str], color: Optional[str], size: Optional[int], position: Optional[str], thickness: Optional[int]):
    if font is None:
        font = cv2.FONT_HERSHEY_SIMPLEX
    else:
        font = getattr(cv2,font.value)

    if color is None:
        color = (255, 0, 0)
    if size is None:
        size = 5
    if position is None:
        position = "floor"
    if thickness is None:
        thickness = 3
    

    # กำหนดสี
    if "red" in color or "Red" in color or "RED" in color  or "แดง" in color :
        color = (0, 0, 255)

    elif "green" in color or "Green" in color or "GREEN" in color or "เขียว" in color:
        color = (0, 255, 0)

    elif "blue" in color or "Blue" in color or "BLUE" in color or "น้ำเงิน" in color:
        color = (255, 0, 0)

    elif "white" in color or "White" in color or "WHITE" in color or "ขาว" in color:
        color = (255, 255, 255)

    elif "cyan" in color or "Cyan" in color or "CYAN" in color or "เขียวแกมน้ำเงิน" in color or "น้ำเงินแกมเขียว" in color or "เขียวน้ำเงิน" in color or "น้ำเงินเขียว" in color or "ฟ้า" in color:
        color = (255, 255, 0)

    elif "yellow" in color or "Yellow" in color or "YELLOW" in color or "เหลือง" in color :
        color = (255, 0, 255)

    elif "black" in color or "Black" in color or "BLACK" in color or "ดำ" in color :
        color = (0, 0, 0)

    elif "purple" in color or "Purple" in color or "PURPLE" in color or "ม่วง" in color :
        color = (128, 0, 128)

    elif "gray" in color or "Gray" in color or "GRAY" in color or "เทา" in color :
        color = (128, 128, 128)

    elif "orange" in color or "Orange" in color or "ORANGE" in color or "ส้ม" in color :
        color = (0, 128, 255)

    elif "pink" in color or "Pink" in color or "PINK" in color or "ชมพู" in color :
        color = (255, 128, 255)

    elif "brown" in color or "Brown" in color or "BROWN" in color or "น้ำตาล" in color :
        color = (0, 75, 150)

    # กำหนดตำแหน่ง
    if "head" in position or "upper" in position or "up" in position or "top" in position or "บน" in position:
        position = 6

    elif "center" in position or "medium" in position or "middle" in position or "between" in position or "กลาง" in position:
        position = 2

    elif "bottom" in position or "lower" in position or "floor" in position or "under" in position or "ล่าง" in position:
        position = 1.2

    imageprocess_fn.text(f"temp/autosave/{client.last_image}",text,font,color,size,position,thickness)
    file_name = discord.File(f"temp/autosave/{client.last_image}")
    await interaction.response.send_message(file=file_name)


################################################# Downloader #################################################
@client.tree.command(name="downloader", description="ดาวน์โหลดวิดีโอจาก Youtube")
@app_commands.choices(command=[
    app_commands.Choice(name="📺 Youtube (ดูข้อมูลคลิปและดาวน์โหลดได้)",value="youtube"),
    app_commands.Choice(name="🔊 Audio (ดาวน์โหลดและส่งไฟล์ในห้องแชท)",value="audio"),
    app_commands.Choice(name="🎞 Video (ไม่ควรโหลดคลิปที่มีขนาดใหญ่ เพราะมีความเร็วที่ช้ามาก ๆ )",value="video")])

@app_commands.describe(command="เลือกคำสั่งที่ต้องการ",url="ลิ้งของวิดีโอ")
async def downloader(interaction: discord.Interaction, command: discord.app_commands.Choice[str], url: str):
    if command.value == "youtube":
        await interaction.response.send_message(f"🔎 **กำลังหา** `{url}`")

        # เก็บข้อมูลดิบ
        title = youtubedl_fn.yt_title(url)
        ext = youtubedl_fn.yt_ext(url)
        upload_date = youtubedl_fn.yt_upload_date(url)
        channel = youtubedl_fn.yt_channel(url)
        duration = youtubedl_fn.yt_duration(url)
        view_count = youtubedl_fn.yt_view_count(url)
        like_count = youtubedl_fn.yt_like_count(url)
        dislike_count = youtubedl_fn.yt_dislike_count(url)
        comment_count = youtubedl_fn.yt_comment_count(url)
        filesize_approx = youtubedl_fn.yt_filesize_approx(url)

        # ข้อมูลสำคัญ
        videolink = youtubedl_fn.yt_video(url)
        audiolink = youtubedl_fn.yt_audio(url)
        thumbnail = youtubedl_fn.yt_thumbnail(url)

        # ข้อมูลสุก
        videolinknew = shorten_url.shortenmylink(videolink)
        audiolinknew = shorten_url.shortenmylink(audiolink)
        durationnew = sectobigger.sec(duration)
        upload_datenew = sectobigger.datenumbeautiful(upload_date)

        dl = discord.Embed(title = f"**{title}**", color = 0xff80c9)
        dl.timestamp = interaction.created_at
        dl.add_field(name="🔐 นามสกุลไฟล์", value=f"`{ext}`", inline=False)
        dl.add_field(name="🥼 ช่อง", value=f"`{channel}`", inline=False)
        dl.add_field(name="📆 วันที่อัพโหลด", value=f"`{upload_datenew}`", inline=False)
        dl.add_field(name="🕒 ระยะเวลา", value=f"`{durationnew}`", inline=False)
        dl.add_field(name="👀 จำนวนคนดู", value=f"`{view_count} คน`", inline=False)
        dl.add_field(name="👍🏻 จำนวนคน Like", value=f"`{like_count} คน`", inline=False)
        dl.add_field(name="👎🏻 จำนวนคน Dislike", value=f"`{dislike_count} คน`", inline=False)
        dl.add_field(name="💬 จำนวน Comment", value=f"`{comment_count} คน`", inline=False)
        dl.add_field(name="📦 ขนาดไฟล์", value=f"`{filesize_approx}`", inline=False)
        dl.set_image(url=thumbnail)

        url_view = discord.ui.View()
        url_view.add_item(discord.ui.Button(label='Video',emoji="🎬" , style=discord.ButtonStyle.url, url=videolinknew))
        url_view.add_item(discord.ui.Button(label='Audio',emoji="🔊" , style=discord.ButtonStyle.url, url=audiolinknew))

        await interaction.edit_original_message(content="",embed=dl,view=url_view)

    elif command.value == "audio":
        clipname = youtubedl_fn.yt_audio_get_clip_name(url)
        await interaction.response.send_message(f"📥 **กำลังดาวน์โหลด** `{clipname}`")
        youtubedl_fn.yt_audio_dir(url)

        await interaction.edit_original_message(content=f"✅ **ดาวน์โหลดแล้ว** `{clipname}`")
        file=discord.File(f'temp/audio/{clipname}')
        await interaction.followup.send(file=file)

    elif command.value == "video":
        await interaction.response.send_message(f"🔎 **กำลังหา** `{url}`")
        clipname = youtubedl_fn.yt_video_get_clip_name(url)

        await interaction.edit_original_message(content=f"👀 **พบ** `{clipname}`")
        await asyncio.sleep(2)

        hd = discord.ui.Button(label='คุณภาพสูง',emoji="<:FullHD:1001878040424480828>", style=discord.ButtonStyle.green, custom_id="hd")
        sd = discord.ui.Button(label='คุณภาพต่ำ',emoji="<:Not4K:1001877314390462624>", style=discord.ButtonStyle.red, custom_id="sd")
        
        async def hd_callback(interaction):
            await interaction.response.edit_message(content=f"📥 **กำลังดาวน์โหลด** `{clipname}` **ในโหมดคุณภาพสูง**", view=None)
            youtubedl_fn.yt_video_dir_best(url)
            await interaction.edit_original_message(content=f"✅ **ดาวน์โหลดแล้ว** `{clipname}`")
            await startcompress(clipname)
        
        async def sd_callback(interaction):
            await interaction.response.edit_message(content=f"📥 **กำลังดาวน์โหลด** `{clipname}` **ในโหมดคุณภาพต่ำ**", view=None)
            youtubedl_fn.yt_video_dir_worst(url)
            await interaction.edit_original_message(content=f"✅ **ดาวน์โหลดแล้ว** `{clipname}`")
            await startcompress(clipname)

        hd.callback = hd_callback
        sd.callback = sd_callback
        view = discord.ui.View()
        view.add_item(hd)
        view.add_item(sd)
        await interaction.edit_original_message(content="❔ **โปรดเลือกคุณภาพของคลิปวิดีโอ**",view=view)

        async def startcompress(clipname):
            # Send the video
            try: # No compression
                await interaction.followup.send(file=discord.File(f"temp/video/{clipname}"))
                
            except: # If can't send, compress the file
                size = videoprocess_fn.getfilesize(f"temp/video/{clipname}")
                
                # Ask for compression
                compress_button = discord.ui.Button(label='ลองบีบอัดไฟล์',emoji="🗜", style=discord.ButtonStyle.primary, custom_id="compress")

                async def compress(interaction):
                    await interaction.response.edit_message(content=f"**🗜 กำลังบีบอัด...** `({size})`",view=None)

                    # Video Compression (เฉพาะโมดูล compressvideo ที่ไม่ต้องระบุ path)
                    stat = videoprocess_fn.compressvideo(clipname)[0]
                    compressedclipname = videoprocess_fn.compressvideo(clipname)[1]
                    await interaction.edit_original_message(content=stat)

                    try: # Send again
                        await interaction.followup.send(file=discord.File(f'{compressedclipname}.mp4'))
                    
                    except: # Can't send again
                        size_compresesed = videoprocess_fn.getfilesize(f'{compressedclipname}.mp4')
                        await interaction.edit_original_message(content=f"❌ **ไฟล์มีขนาดใหญ่เกินไป** `{size_compresesed}`**, ไม่สามารถบีบอัดได้มากกว่านี้**")

                compress_button.callback = compress

                compressview = discord.ui.View()
                compressview.add_item(compress_button)

                await interaction.edit_original_message(content=f"❌ **ไฟล์มีขนาดใหญ่เกินไป** `{size}`**, ต้องการบีบอัดไฟล์หรือไม่?**", view=compressview)


################# COMPRESSION #################
async def startcompress(interaction,clipname):
    size = videoprocess_fn.getfilesize(f"temp/video/{clipname}")
    
    # Ask for compression
    compress_button = discord.ui.Button(label='ลองบีบอัดไฟล์',emoji="🗜", style=discord.ButtonStyle.primary, custom_id="compress")

    async def compress(interaction):
        await interaction.response.edit_message(content=f"**🗜 กำลังบีบอัด...** `({size})`",view=None)

        # Video Compression (เฉพาะโมดูล compressvideo ที่ไม่ต้องระบุ path)
        stat = videoprocess_fn.compressvideo(clipname)[0]
        compressedclipname = videoprocess_fn.compressvideo(clipname)[1]
        await interaction.edit_original_message(content=stat)

        try: # Send again
            await interaction.followup.send(file=discord.File(f'{compressedclipname}.mp4'))
        
        except: # Can't send again
            size_compresesed = videoprocess_fn.getfilesize(f'{compressedclipname}.mp4')
            await interaction.edit_original_message(content=f"❌ **ไฟล์มีขนาดใหญ่เกินไป** `{size_compresesed}`**, ไม่สามารถบีบอัดได้มากกว่านี้**")

    compress_button.callback = compress

    compressview = discord.ui.View()
    compressview.add_item(compress_button)

    await interaction.edit_original_message(content=f"❌ **ไฟล์มีขนาดใหญ่เกินไป** `{size}`**, ต้องการบีบอัดไฟล์หรือไม่?**", view=compressview)
##############################################


################################################# Video Process #################################################
@client.tree.command(name="video", description="🎥 การประมวลผลวิดีโอ")
@app_commands.choices(command=[
    app_commands.Choice(name="📹 ใส่เสียงในภาพ (ต้องอัพโหลดภาพและเสียงก่อนใช้งานคำสั่ง)",value="imgaudio"),
    app_commands.Choice(name="📺 ใส่เสียง Youtube ในภาพ (ต้องใส่ลิ้ง Youtube)",value="ytaudio"),
    app_commands.Choice(name="🧲 ต่อคลิปวิดีโอ (ต้องอัพโหลดวิดีโอที่ 2 หลังใช้งานคำสั่ง)",value="videomix")])

@app_commands.describe(command="เลือกคำสั่งที่ต้องการ ",url="ลิ้งของวิดีโอ")
async def downloader(interaction: discord.Interaction, command: discord.app_commands.Choice[str], url: Optional[str]):
    if command.value == "imgaudio":
        await interaction.response.send_message("**🎬 กำลังสร้าง...**")
        image_path = f"temp/autosave/{client.last_image}"
        audio_path = f"temp/autosave/{client.last_audio}"

        # Optimize ให้ดีกว่านี้ได้ แต่ขี้เกียจแล้ว (Co-Pilot ช่วย)
        output_last_image_nameonly = client.last_image.split(".")[0]
        output_last_audio_nameonly = client.last_audio.split(".")[0]

        output_path = f"temp/video/{output_last_image_nameonly}_{output_last_audio_nameonly}.mp4"
        audio2video.add_static_image_to_audio(image_path, audio_path, output_path)

        await interaction.edit_original_message(content="**✅ สร้างเสร็จแล้ว**")
        await interaction.followup.send(file=discord.File(output_path))

    elif command.value == "ytaudio":
        name = youtubedl_fn.yt_audio_get_clip_name(url)
        output_name_nameonly = name.split(".")[0]

        await interaction.response.send_message(f"**📥 กำลังดาวน์โหลด `{output_name_nameonly}`**")
        youtubedl_fn.yt_audio_dir(url)

        await interaction.edit_original_message(content="**🎬 กำลังสร้าง...**")
        image_path = f"temp/autosave/{client.last_image}"
        audio_path = f"temp/audio/{name}"
        
        output_last_image_nameonly = client.last_image.split(".")[0]

        output_path = f"temp/video/{output_last_image_nameonly}_{output_name_nameonly}.mp4"
        audio2video.add_static_image_to_audio(image_path, audio_path, output_path)

        await interaction.edit_original_message(content="**✅ สร้างเสร็จแล้ว**")
        await interaction.followup.send(file=discord.File(output_path))

    elif command.value == "videomix":
        time_elaps = 0

        clip1 = client.last_video
        await interaction.response.send_message("**👀 โปรดส่งไฟล์วิดีโอที่จะต่อ**\n**🕐 เวลาที่เหลือ 30 วินาที**")

        while time_elaps < 30:
            if clip1 != client.last_video:
                await interaction.edit_original_message(content="**✅ ได้รับไฟล์แล้ว**")
                break
            time_elaps += 1
            await interaction.edit_original_message(content=f"**👀 โปรดส่งไฟล์วิดีโอที่จะต่อ**\n**🕐 เวลาที่เหลือ {30 - time_elaps} วินาที**")
            await asyncio.sleep(1)
            print("Clip1: ", clip1)
            print("Clip2: ", client.last_video)
        
        if time_elaps >= 30:
            await interaction.edit_original_message(content="**🕐 หมดเวลา**")
            return

        clip2 = client.last_video

        confirm_button = discord.ui.Button(label='ยืนยัน',emoji="<:Approve:921703512382009354>", style=discord.ButtonStyle.green, custom_id="approve")
        deny_button = discord.ui.Button(label='ยกเลิก',emoji="<:Deny:921703523111022642>", style=discord.ButtonStyle.red, custom_id="deny")
        
        async def confirm_callback(interaction):
            await interaction.response.edit_message(content="**🎬 กำลังสร้าง...**", view=None)
            output_path, output_name = videoprocess_fn.videomixer(clip1, clip2)
            await interaction.followup.send(content="**✅ สร้างเสร็จแล้ว**")

            try:
                await interaction.followup.send(file=discord.File(output_path))
            except:
                print("Compresing")
                startcompress(interaction, output_name)
            

        
        async def deny_callback(interaction):
            await interaction.response.edit_message(content="**❌ ยกเลิกแล้ว**")
            pass

        confirm_button.callback = confirm_callback
        deny_button.callback = deny_callback
        view = discord.ui.View()
        view.add_item(confirm_button)
        view.add_item(deny_button)

        await interaction.followup.send(content=f"**ต้องการจะต่อคลิป** `{clip1}` **กับ** `{clip2}` **ใช่หรือไม่?**",view=view)
        
        
        
        
        
        
        
        
        
        
        
        
        



















################################################# Image Message Context #################################################
@client.tree.context_menu(name='🔦 คุณสมบัติรูปภาพ')
async def imginfo(interaction: discord.Interaction, message: discord.Message):
    channel = imageprocess_fn.imginfo_channel(f"temp/autosave/{client.last_image}")
    height = imageprocess_fn.imginfo_height(f"temp/autosave/{client.last_image}")
    width = imageprocess_fn.imginfo_width(f"temp/autosave/{client.last_image}")

    size = os.path.getsize(f"temp/autosave/{client.last_image}")/1000000
    if size < 1:
        size = os.path.getsize(f"temp/autosave/{client.last_image}")/1000
        if size < 1:
            size = os.path.getsize(f"temp/autosave/{client.last_image}")
            size = f"{size} Bytes"
        else:
            size = f"{size} KB"
    else:
        size = f"{size} MB"

    info = discord.Embed(title = "**🔦 คุณสมบัติรูปภาพ**", color = 0xff3859)
    info.timestamp = interaction.created_at
    info.add_field(name="🖨️ ชื่อไฟล์", value=f"`{client.last_image}`", inline=False)
    info.add_field(name="📂 ขนาดไฟล์", value=f"`{size}`", inline=False)
    info.add_field(name="🌈 ช่อง", value=f"`{channel}`", inline=False)
    info.add_field(name="📏 ความกว้าง", value=f"`{width} pixels`", inline=False)
    info.add_field(name="📐 ความสูง", value=f"`{height} pixels`", inline=False)
    info.add_field(name="🪄 ความละเอียด", value=f"`{width}x{height}`", inline=False)
    await interaction.response.send_message(embed=info)






























################################################# Cancel #################################################
@client.tree.command(description="❌ ยกเลิกคำสั่ง")
@app_commands.choices(command=[
    app_commands.Choice(name="⏰ Countdown",value="cancel_countdown"),
    app_commands.Choice(name="🔌 Countdis",value="cancel_countdis"),
    ])

async def cancel(interaction: discord.Interaction, command: discord.app_commands.Choice[str]):
    if command.value == "cancel_countdown":
        client.timestop1 = -22052603
        await interaction.response.send_message(content="**🛑 ยกเลิกคำสั่ง Countdown แล้ว**")
    elif command.value == "cancel_countdis":
        client.timestop2 = -22052603
        await interaction.response.send_message(content="**🛑 ยกเลิกคำสั่ง Countdis แล้ว**")


################################################# Auto Save Attachments with name #################################################
@client.event
async def on_message(message):
    if message.author.id != "907247505346035752":
        extension = ""
        url = ""

        try:
            attachment_url = message.attachments[0]
            url = str(attachment_url.url)
            splitedbydot = url.split(".")
            splitedbyslash = splitedbydot[len(splitedbydot)-2].split("/")
            name = splitedbyslash[len(splitedbyslash)-1]
            extension = splitedbydot[len(splitedbydot)-1]

            FileName = name+"."+extension
            client.name_only = name
            r = requests.get(url, stream=True)
            with open(FileName, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            shutil.move(FileName, f"temp/autosave/{FileName}")
            await client.change_presence(activity=discord.Game(name=f"💾 {FileName}"))
            print('Saving : ' + FileName)

            if extension == "png" or extension == "jpg" or extension == "jpeg" or extension == "webp":
                client.last_image = FileName
                client.last_image_url = url
                print(f"Saved {FileName} to Last Image")
            elif extension == "mp4" or extension == "webm" or extension == "mkv" or extension == "avi":
                client.last_video = FileName
                client.last_video_url = url
                print(f"Saved {FileName} to Last Video")
            elif extension == "mp3" or extension == "wav" or extension == "m4a":
                client.last_audio = FileName
                client.last_audio_url = url
                print(f"Saved {FileName} to Last Audio")
            elif extension == "pdf":
                client.last_pdf = FileName
                client.last_pdf_url = url
                print(f"Saved {FileName} to Last PDF")
        
        except:
            print("No attachment")

        














# To make an argument optional, you can either give it a supported default argument
# or you can mark it as Optional from the typing standard library. This example does both.
@client.tree.command()
@app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
async def joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    """Says when a member joined."""
    # If no member is explicitly provided then we use the command user here
    member = member or interaction.user

    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')


# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.

# This context menu command only works on members
@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')


# This context menu command only works on messages
@client.tree.context_menu(name='Report to Moderators')
async def report_message(interaction: discord.Interaction, message: discord.Message):
    # We're sending this response message with ephemeral=True, so only the command executor can see it
    await interaction.response.send_message(
        f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
    )

    # Handle report by sending it into a log channel
    log_channel = interaction.guild.get_channel(720687176115027970)  # replace with your channel id

    embed = discord.Embed(title='Reported Message')
    if message.content:
        embed.description = message.content

    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.timestamp = message.created_at

    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

    await log_channel.send(embed=embed, view=url_view)

#อย่าลืมทำ Auto Delete ของ Auto Save
Token = os.environ['MiuraTesterToken']
client.run(Token)