from database import init_db, add_expense, get_all, get_today, get_month, delete_expense
import discord
import os
import io
from datetime import datetime,date
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import openpyxl
import io

load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print(f"bot is ready as {client.user}: ")
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == "ping":
        await message.channel.send("Pong! 🏓")

    elif message.content.startswith("add"):
        parts = message.content.split()
        if len(parts) < 4 :
            await message.channel.send(" Format: add <name> <amount> <category>")
        else:
            name = parts[1]
            amount = float(parts[2])
            category = parts[3]
            today_date = datetime.now().strftime("%Y-%m-%d")
            add_expense(today_date,name,amount,category)
            await message.channel.send(f"✅ Saved! {name} - ₹{amount} ({category})")


    elif message.content == "summary":
        
        rows = get_all()
        if not rows:
            await message.channel.send("No expenses yet!..")
        else:
            total = sum(row[3] for row in rows)
            await message.channel.send(f"💰 Total spent: ₹{total}")
        

    elif message.content == "today":
        today = str(date.today())
        rows = get_today(today)
        if not rows:
            await message.channel.send("No expenses today!..")
        else:
            result = "📅 Today's expenses:\n"
            total = 0
            for row in rows:
                result += f"• {row[2]} - ₹{row[3]} ({row[4]})\n"
                total += row[3]
            result += f"\n💰 Total: ₹{total}"
            await message.channel.send(result)


    elif message.content == "chart":
        rows = get_all()
        if not rows:
            await message.channel.send("No expenses yet!")
        else:
            category_totals = {}
            for row in rows:
                category = row[4]
                amount = row[3]
                category_totals[category] = category_totals.get(category, 0) + amount

            plt.figure(figsize=(6, 6))
            plt.pie(
                category_totals.values(),
                labels=category_totals.keys(),
                autopct="%1.1f%%",
                startangle=90
            )
            plt.title("Spending Breakdown")
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            plt.close()

            await message.channel.send(file=discord.File(buf, filename="chart.png"))

    elif message.content.startswith("month"):
        parts = message.content.split()
        if len(parts) < 2:
            await message.channel.send("❌ Format: month <YYYY-MM>")
        else:
            month = parts[1]
            rows = get_month(month)
            if not rows:
                await message.channel.send(f"No expenses for {month}")
            else:
                result = f"📅 Expenses for {month}:\n"
                total = 0
                for row in rows:
                    result += f"• {row[2]} - ₹{row[3]} ({row[4]})\n"
                    total += row[3]
            result += f"\n💰 Total: ₹{total}"
            await message.channel.send(result)


    elif message.content.startswith("delete"):
        parts = message.content.split()
        if len(parts) < 2:
            await message.channel.send("❌ Format: delete <name>")
        else:
            affected = delete_expense(parts[1])
            if affected == 0:
                await message.channel.send(f"❌ No expense found with name: {parts[1]}")
            else:
                await message.channel.send(f"✅ Deleted all entries for: {parts[1]}")

    elif message.content == "export":
        rows = get_all()
        if not rows:
            await message.channel.send("No expense yet..!")
        else:
            

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Expenses"

            ws.append(["ID" , "Date" , "Name" , "Amount" , "Category"])

            for row in rows:
                ws.append([str(col) if hasattr(col, 'tzinfo') else col for col in row])

            buf = io.BytesIO()
            wb.save(buf)
            buf.seek(0)

            await message.channel.send(
                " 📊 Expense Data..!",
                file = discord.File(buf , filename = "expenses.xlsx")
            )


    elif message.content == "help":
            help_text = """
        📖 **ExpenseBot Commands**

        `add <name> <amount> <category>` — Save an expense
        `delete <name>` — Delete all entries for a name
        `today` — Show today's expenses
        `summary` — Show total spent
        `month <YYYY-MM>` — Show monthly report
        `chart` — Show spending pie chart
        `ping` — Test the bot
        `export`  — export expenses file 
        `help` — Show this message
        """
            await message.channel.send(help_text)
client.run(os.getenv("DISCORD_TOKEN"))
