from random import choices
import discord
from discord import Guild, app_commands
import os
import asyncio
import gtts

from utils import countdown

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.sync = False
        
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.sync:
            await bot.sync(guild=discord.Object(id=720687175611580426))
        print(f'Logged in as {self.user}')

client = aclient()
bot = app_commands.CommandTree(client)

# Help Embed
@bot.command(name="help",description="ความช่วยเหลือ", guild=discord.Object(id=720687175611580426))
async def help(interaction: discord.Integration):
    # หน้าเมนู Embed
    util = discord.Embed(title="**❔ ช่วยเหลือ**",description="╰ *🔧 เครื่องมืออรรถประโยชน์*", color=0x40eefd)
    util.add_field(name="**⌚ นับเวลาถอยหลัง**", value="`/countdown`", inline=False)
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

    select = discord.ui.Select(
        placeholder="เลือกเมนู",
        options=[
            discord.SelectOption(label="เครื่องมืออรรถประโยชน์",emoji="🔧",description="คำสั่งการใช้งานทั่วไป",value="util",default=False),
            discord.SelectOption(label="มีเดียและเพลง",emoji="🎵",description="คำสั่งการใช้งานเสียงและเพลง",value="music",default=False),
            discord.SelectOption(label="รูปภาพและการประมวลผลภาพ",emoji="🖼",description="คำสั่งการใช้งานรูปภาพ",value="image",default=False),
            discord.SelectOption(label="การประมวลผลวิดีโอ",emoji="🎥",description="คำสั่งการใช้งานการประมวลผลวิดีโอ",value="video",default=False),
            discord.SelectOption(label="ดาวน์โหลดไฟล์",emoji="📦",description="คำสั่งการใช้งานดาวน์โหลดไฟล์",value="download",default=False),
            discord.SelectOption(label="ประวัติการอัพเดท",emoji="📌",description="คำสั่งตรวจสอบเวอร์ชันของบอท",value="update",default=False),
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

    await interaction.response.send_message(embed=util,view=view)


# Countdown
bot.timestop1 = 0
@bot.command(name="countdown",description="นับถอยหลัง", guild=discord.Object(id=720687175611580426))
async def countdown_def(interaction: discord.Interaction, time: str):

    time_int = int(time)
    bot.timestop1 = time_int

    if time_int < 0:
        await interaction.response.send_message("**เวลาไม่ถูกต้อง ❌**")
    else:
        output = countdown.countdown_fn(time_int)
        await interaction.response.send_message(output)
        for i in range(time_int):
            output = countdown.countdown_fn(time_int)
            await interaction.edit_original_message(content=output)
            await asyncio.sleep(1)
            time_int -= 1

            if bot.timestop1 == -22052603:
                await interaction.edit_original_message(content="**การนับถอยหลังถูกยกเลิก 🛑**")
                break
        if bot.timestop1 != -22052603:
            await interaction.edit_original_message(content="**หมดเวลา 🔔**")

# Countdis
bot.timestop2 = 0
bot.member_except = []
@bot.command(name="countdis",description="นับถอยหลังและตัดการเชื่อมต่อ", guild=discord.Object(id=720687175611580426))
async def countdown_def(interaction: discord.Interaction, time: str):
    people_counter = 0

    time_int = int(time)
    bot.timestop2 = time_int

    if time_int < 0:
        await interaction.response.send_message("**เวลาไม่ถูกต้อง ❌**")
    else:
        output = countdown.countdown_fn(time_int)
        await interaction.response.send_message(output)
        for i in range(time_int):
            output = countdown.countdown_fn(time_int)
            await interaction.edit_original_message(content=output)
            await asyncio.sleep(1)
            time_int -= 1

            if bot.timestop2 == -22052603:
                await interaction.edit_original_message(content="**การนับถอยหลังถูกยกเลิก 🛑**")
                break
        if bot.timestop2 != -22052603:
            try:
                members = interaction.user.voice.channel.members
                channel = interaction.user.voice.channel
            
                await interaction.edit_original_message(content="**หมดเวลา 🔔**")
                
                if bot.member_except == []: # ไม่มีใครยกเว้น
                    members = interaction.user.voice.channel.members
                    for member in members:
                        await member.move_to(None)
                        people_counter += 1

                    bot.member_except = []
                    await interaction.followup.send(f"⏏  **ตัดการเชื่อมต่อจำนวน {people_counter} คน จาก `{channel}` สำเร็จแล้ว**")

                else:
                    members = interaction.user.voice.channel.members
                    for member in members:
                        if member not in bot.member_except: # เช็คว่าใครไม่ออก
                            await member.move_to(None)
                            people_counter += 1

                    await interaction.followup.send(f"⏏  **ตัดการเชื่อมต่อจำนวน {people_counter} คน จาก `{channel}` สำเร็จแล้ว**")
                    
            except:
                await interaction.edit_original_message(content="**ℹ ต้องอยู่ในช่องเสียงก่อน จึงจะสามารถใช้ได้**")

# Cancel Command
@bot.command(name="cancel",description="ยกเลิกคำสั่ง", guild=discord.Object(id=720687175611580426))
@app_commands.choices(command=[
    app_commands.Choice(name="Countdown",value="cancel_countdown"),
    app_commands.Choice(name="Countdis",value="cancel_countdis"),
    ])

async def cancel_def(interaction: discord.Interaction, command: discord.app_commands.Choice[str]):
    if command.value == "cancel_countdown":
        bot.timestop1 = -22052603
        await interaction.response.send_message(content="**🛑 ยกเลิกคำสั่ง Countdown แล้ว**")
    elif command.value == "cancel_countdis":
        bot.timestop2 = -22052603
        await interaction.response.send_message(content="**🛑 ยกเลิกคำสั่ง Countdis แล้ว**")

# Except Countdis
bot.last_use = [0]

@bot.command(name="except",description="ยกเว้นคำสั่ง Countdis", guild=discord.Object(id=720687175611580426))
async def except_def(interaction: discord.Interaction):
    user = interaction.user
    if user.id not in bot.last_use:
        bot.member_except.append(user) # คนที่จะไม่ออก
        bot.last_use.pop(0)
        bot.last_use.append(user.id)
        await interaction.response.send_message(content=f"**<@{user.id}> ได้รับการยกเว้น <:Approve:921703512382009354>**")
    else:
        bot.member_except.remove(user) # คนที่จะไม่ออก
        bot.last_use.pop(0)
        bot.last_use.append(0)
        await interaction.response.send_message(content=f"**<@{user.id}> ถูกลบออกจากรายการที่ยกเว้น <:Deny:921703523111022642>**")

# Send Message
@bot.command(name="send",description="ส่งข้อความ", guild=discord.Object(id=720687175611580426))
async def send_def(interaction: discord.Interaction, channel: discord.TextChannel, *, message: str):
    if interaction.user.id == 269000561255383040:
        await interaction.response.send_message(content=f'**"**{message}**"** ถูกส่งไปยัง {channel.mention}')
        await channel.send(message)
    else:
        await interaction.response.send_message(content="**แกไม่มีสิทธิ์!**")
    
# TTS
@bot.command(name="tts",description="แปลงข้อความเป็นเสียง", guild=discord.Object(id=720687175611580426))
@app_commands.choices(language=[
    app_commands.Choice(name="Afrikaans (South Africa)",value="af"),
    app_commands.Choice(name="Arabic",value="ar"),
    app_commands.Choice(name="Danish (Denmark)",value="da"),
    app_commands.Choice(name="Dutch (Belgium)",value="nl"),
    app_commands.Choice(name="English (US)",value="en"),
    app_commands.Choice(name="Finnish (Finland)",value="fi"),
    app_commands.Choice(name="French (France)",value="fr"),
    app_commands.Choice(name="German (Germany)",value="de"),
    app_commands.Choice(name="Gujarati (India)",value="gu"),
    app_commands.Choice(name="Hindi (India)",value="hi"),
    app_commands.Choice(name="Indonesian (Indonesia)",value="id"),
    app_commands.Choice(name="Italian (Italy)",value="it"),
    app_commands.Choice(name="Japanese (Japan)",value="ja"),
    app_commands.Choice(name="Korean (South Korea)",value="ko"),
    app_commands.Choice(name="Malay (Malaysia)	",value="ms"),
    app_commands.Choice(name="Portuguese (Brazil)",value="pt"),
    app_commands.Choice(name="Romanian (Romania)",value="ro"),
    app_commands.Choice(name="Russian (Russia)",value="ru"),
    app_commands.Choice(name="Serbian (Serbia)",value="sr"),
    app_commands.Choice(name="Slovak (Slovakia)",value="sk"),
    app_commands.Choice(name="Spanish (Spain)",value="es"),
    app_commands.Choice(name="Swedish (Sweden)",value="sv"),
    app_commands.Choice(name="Thai (Thailand)",value="th"),
    app_commands.Choice(name="Ukrainian (Ukraine)",value="uk"),
    app_commands.Choice(name="Vietnamese (Vietnam)",value="vi"),
    ])
    
async def tts_def(interaction: discord.Interaction,language: discord.app_commands.Choice[str] ,* , text: str):
    tts = gtts.gTTS(text=text,lang=language.value)
    tts.save(f'temp/tts_{language.value}.mp3')

    file = discord.File(f'temp/tts_{language.value}.mp3')
    await interaction.response.send_message(file=file)

Token = os.environ['MiuraTesterToken']
client.run(Token)