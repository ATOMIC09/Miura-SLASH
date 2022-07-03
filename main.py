import discord
from discord.ext import commands
import interactions
import os

Token = os.environ["MiuraTesterToken"]
bot = interactions.Client(token=Token)

@bot.command(name="help",description="เรียกเมนูช่วยเหลือ")
async def help(self, ctx: interactions.CommandContext):
    interactions.Embed(title="❔ ช่วยเหลือ >🎵 เพลง",color=0x40eefd)
    submissions = await get_memes('memes')
    button1 = Button(label='Next Meme', style=discord.ButtonStyle.green)
    button2 = Button(label='End Interaction', style=discord.ButtonStyle.red)

    async def next_meme(interaction):
        if len(submissions) == 0:
            await interaction.response.edit_message(content='No more memes available')
            return
        submissions.pop(0)
        embed.title = submissions[0].title
        embed.url = submissions[0].url
        embed.set_image(url=submissions[0].url)
        await interaction.response.edit_message(embed=embed)

    async def end_interaction(interaction):
        pass
        # I have no idea what to do here

    view = View()
    view.add_item(button1)
    view.add_item(button2)
    embed = discord.Embed(title=submissions[0].title, url=submissions[0].url, colour=discord.Colour.random())
    embed.set_image(url=submissions[0].url)
    await ctx.send(embed=embed, view=view)
    button1.callback = next_meme
    button2.callback = end_interaction

@bot.command(
    name="test 1",
    description="This is **TEST** command",
    options = [
        interactions.Option(
            name="text",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def my_first_command(ctx: interactions.CommandContext, text: str):
    await ctx.send(f"You said '{text}'!")

@bot.command(
    name="test 2",
    description="This is **TEST** command 2",
    options = [
        interactions.Option(
            name="text",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def my_second_command(ctx: interactions.CommandContext, text: str):
    await ctx.send(f"You said '{text}'!")

bot.start()