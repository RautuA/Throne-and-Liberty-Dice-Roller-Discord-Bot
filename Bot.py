import discord
from discord.ext import commands
import random
from apikeys import BOTTOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=intents, application_id="application id")
        
        self.current_item = None
        self.eligible_roles_for_item = set()
        self.users_rolled = set()  
        self.roll_results = {}  

    async def setup_hook(self):
        try:
            await self.tree.sync()  
            print("Slash commands synced globally.")

            commands = await self.tree.fetch_commands()
            print(f"Registered commands: {commands}")
            
        except discord.errors.Forbidden as e:
            print(f"Failed to sync slash commands due to missing permissions: {e}")
        except Exception as e:
            print(f"An error occurred during sync: {e}")

bot = MyBot()

@bot.tree.command(name="ping", description="Show bot latency")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f'Bot latency is {latency}ms')

@bot.tree.command(name="go_dice", description="Start an item roll")
@commands.has_any_role("STAFF", "GM")  
async def start_roll(interaction: discord.Interaction, item_name: str, allowed_roles: str):
    valid_roles = {"Staff", "Wand", "Crossbow", "Longbow", "Sword & Shield", "Greatsword", "Dagger", "Member"}

    allowed_roles_set = set(role.strip() for role in allowed_roles.split(","))

    if not allowed_roles_set.issubset(valid_roles):
        await interaction.response.send_message(
            "Invalid role(s) specified. Allowed roles are: Staff, Wand, Crossbow, Longbow, Sword & Shield, Greatsword, Dagger",
            ephemeral=True  
        )
        return

    user_roles = {role.name for role in interaction.user.roles}
    print(f"User roles for {interaction.user}: {user_roles}")

    if "STAFF" not in user_roles and "GM" not in user_roles:
        await interaction.response.send_message("You do not have the required role(s) to run this command.", ephemeral=True)  

    bot.current_item = item_name
    bot.eligible_roles_for_item = allowed_roles_set
    bot.users_rolled.clear()  
    bot.roll_results.clear()  
    await interaction.response.send_message(
        f"Rolling started for **{item_name}**! Only users with roles: {', '.join(allowed_roles_set)} can dice. Use /dice."
    )

@bot.tree.command(name="dice", description="Roll for the current item")
@commands.has_any_role("STAFF", "GM")  
async def dice(interaction: discord.Interaction):
    if bot.current_item is None:
        await interaction.response.send_message("No item roll is currently active.", ephemeral=True)  
        return

    if interaction.user.id in bot.users_rolled:
        await interaction.response.send_message("You have already rolled for this item.", ephemeral=True)  
        return

    user_roles = {role.name for role in interaction.user.roles}
    if bot.eligible_roles_for_item & user_roles:  
        roll_result = random.randint(1, 100)
        bot.users_rolled.add(interaction.user.id)  
        bot.roll_results[interaction.user.id] = roll_result  
        
        await interaction.response.send_message(f"{interaction.user.mention} rolled a {roll_result}!")
    else:
        await interaction.response.send_message("You do not have the required role(s) to roll for this item.", ephemeral=True)  

@bot.tree.command(name="end_dice", description="End the current roll session")
@commands.has_any_role("STAFF", "GM")  
async def end_roll(interaction: discord.Interaction):
    
    user_roles = {role.name for role in interaction.user.roles}
    if "STAFF" not in user_roles and "GM" not in user_roles:
        await interaction.response.send_message("You do not have the required role(s) to use this command.", ephemeral=True) 
        return

    if not bot.roll_results:
        await interaction.response.send_message("No one has rolled yet.", ephemeral=True)  
        return

    highest_roll_user_id, highest_roll = max(bot.roll_results.items(), key=lambda x: x[1])
    highest_roll_user = await bot.fetch_user(highest_roll_user_id)

    await interaction.response.send_message(f"**{highest_roll_user.mention}** rolled the highest for **{bot.current_item}** with a roll of **{highest_roll}**!")

    bot.current_item = None
    bot.eligible_roles_for_item.clear()
    bot.users_rolled.clear()  
    bot.roll_results.clear()  

bot.run(BOTTOKEN)
