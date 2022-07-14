import asyncio
from ctypes import util
from distutils import extension
from email import message
from lzma import FILTER_LZMA1
from typing import Optional
import os
from xmlrpc.client import Fault
import discord
from discord import app_commands
import requests
import shutil
import gtts
import pdf2image

from utils import countdown_fn

MY_GUILD = discord.Object(id=720687175611580426)  # replace with your guild id

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('----------------------------------------------------------')

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.all()
intents.members = True
client = MyClient(intents=intents)

client.last_image = ""
client.last_video = ""
client.last_audio = ""
client.last_pdf = ""

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
    music.add_field(name="**⏏️ เตะบอท**", value="`/music dis`", inline=False)
    music.add_field(name="**▶️ เล่นเสียง**", value="`/music play`", inline=False)
    music.add_field(name="**💾 เล่นเสียงผ่านไฟล์มีเดีย**", value="`/music plocal`", inline=False)
    music.add_field(name="**⏭ ข้าม**", value="`/music skip`", inline=False)
    music.add_field(name="**⏸ พัก**", value="`/music pause`", inline=False)
    music.add_field(name="**⏯ เล่นต่อ**", value="`/music resume`", inline=False)
    music.add_field(name="**⏹ หยุด**", value="`/music stop`", inline=False)
    music.add_field(name="**🔢 คิวการเล่น**", value="`/music queue`", inline=False)
    music.add_field(name="**🆑 ล้างคิวทั้งหมด**", value="`/music clear`", inline=False)

    image = discord.Embed(title="**❔ ช่วยเหลือ**",description="╰ *🖼 รูปภาพและการประมวลผลภาพ*", color=0x5be259)
    image.add_field(name="**🔦 ตรวจสอบคุณสมบัติ**", value="`/image info`", inline=False)
    image.add_field(name="**🔍 ค้นหาภาพคล้าย**", value="`/image reverse`", inline=False)
    image.add_field(name="**⬜ แปลงภาพสีเป็นภาพขาวดำ**", value="`/image grayscale`", inline=False)
    image.add_field(name="**🎨 แปลงภาพขาวดำเป็นภาพสี**", value="`/image colorize`", inline=False)
    image.add_field(name="**🧹 ลบพื้นหลังขาว**", value="`/image removebg`", inline=False)
    image.add_field(name="**📷 ตัวสร้าง QR Code**", value="`/image qr`", inline=False)
    image.add_field(name="**↔ ยืดภาพ**", value="`/image wide`", inline=False)
    image.add_field(name="**↔↔ ยืดดดดดภาพ**", value="`/image ultrawide`", inline=False)
    image.add_field(name="**↙↗ ปรับสเกลภาพ**", value="`/image scale`", inline=False)
    image.add_field(name="**↕↔ ปรับขนาดภาพ**", value="`/image resize`", inline=False)
    image.add_field(name="**✏ เขียนข้อความบนภาพ**", value="`/image text`", inline=False)
    image.add_field(name="**👁 Laser Eye**", value="`/image laser`", inline=False)
    image.add_field(name="**🍳 Deep Fryer**", value="`/image deepfry`", inline=False)
    image.add_field(name="**🐶 Petpet Generator**", value="`/image pet`", inline=False)

    video = discord.Embed(title="**❔ ช่วยเหลือ**",description="╰ *🎥 การประมวลผลวิดีโอ*", color=0x4f4eca)
    video.add_field(name="**📹 ใส่เสียงในภาพ**", value="`/video imgaudio`", inline=False)
    video.add_field(name="**📺 ใส่เสียงจาก Youtube ในภาพ**", value="`/video imgyt`", inline=False)
    video.add_field(name="**🧲 ต่อคลิปวิดีโอ**", value="`/video videomix`", inline=False)

    download = discord.Embed(title="**❔ ช่วยเหลือ**",description="╰ *📦 ดาวน์โหลดไฟล์*", color=0xff80c9)
    download.add_field(name="**📺 Youtube Downloader**", value="`/download youtube`", inline=False)
    download.add_field(name="**💿 Audio Downloader**", value="`/download audio`", inline=False)
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
    discord.SelectOption(label="รูปภาพและการประมวลผลภาพ",emoji="🖼",description="คำสั่งการใช้งานรูปภาพ",value="image",default=False),
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
async def pdftoimage(interaction: discord.Interaction,zipped: discord.app_commands.Choice[str], extension: discord.app_commands.Choice[str], filename: Optional[str] = None):
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














################################################# Cancel #################################################
@client.tree.command(description="❌ ยกเลิกคำสั่ง")
@app_commands.choices(command=[
    app_commands.Choice(name="Countdown",value="cancel_countdown"),
    app_commands.Choice(name="Countdis",value="cancel_countdis"),
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
            r = requests.get(url, stream=True)
            with open(FileName, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            shutil.move(FileName, f"temp/autosave/{FileName}")
            print('Saving : ' + FileName)

            if extension == "png" or extension == "jpg" or extension == "jpeg" or extension == "webp":
                client.last_image = FileName
                print(f"Saved {FileName} to Last Image")
            elif extension == "mp4" or extension == "webm" or extension == "mkv" or extension == "avi":
                client.last_video = FileName
                print(f"Saved {FileName} to Last Video")
            elif extension == "mp3" or extension == "wav" or extension == "m4a":
                client.last_audio = FileName
                print(f"Saved {FileName} to Last Audio")
            elif extension == "pdf":
                client.last_pdf = FileName
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