
import discord
import os
import csv
import io
from datetime import datetime,date
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

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
            with open("expenses.csv","a",newline="") as f:
                writer = csv.writer(f)
                writer.writerow([today_date,name,amount,category])
                await message.channel.send(f"✅ Saved! {name} - ₹{amount} ({category})")


    elif message.content == "summary":
        try:
            total = 0
            with open("expenses.csv","r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3:
                        try:
                            total += float(row[2])
                        except ValueError:
                            pass
            await message.channel.send(f"💰 Total spent: ₹{total}")
        except FileNotFoundError:
            await message.channel.send("No expenses yet!..")

    elif message.content == "today":
        try:
            df = pd.read_csv("expenses.csv", names=["date", "name", "amount"])
            today = str(date.today())
            today_df = df[df["date"] == today]
            if today_df.empty:
                await message.channel.send("No expenses today!..")
            else:
                result = "📅 Today's expenses:\n"
                for _, row in today_df.iterrows():
                    result += f"• {row['name']} - ₹{row['amount']}\n"
                result += f"\n💰 Total: ₹{today_df['amount'].sum()}"
                await message.channel.send(result)
        except FileNotFoundError:
            await message.channel.send("No expenses yet..")


    elif message.content == "chart":
        try:
            df = pd.read_csv("expenses.csv", names=["date","name","amount","category"])
            df["amount"] = pd.to_numeric(df["amount"],errors="coerce")
            category_spending = df.groupby("category")["amount"].sum().dropna()

            if category_spending.empty:
                await message.channel.send("No data to display..")
                return

            plt.figure(figsize=(6,6))
            category_spending.plot(kind="pie",autopct="%1.1f%%",startangle=90)
            plt.title("Spending Breakdown")
            plt.ylabel("")
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf,format="png")
            buf.seek(0)
            plt.close()

            await message.channel.send(file=discord.File(buf,filename="chart.png"))
        except FileNotFoundError:
            await message.channel.send("No expenses yet..")

    elif message.content.startswith("month"):
        parts = message.content.split()
        if len(parts) < 2:
            await message.channel.send("❌ Format: month <YYYY-MM>")
        else:
            try:
                month = parts[1]
                df = pd.read_csv("expenses.csv",names=["date","name","amount","category"])
                df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
                month_df = df[df["date"].str.startswith(month)]

                if month_df.empty:
                    await message.channel.send(f"No expenses for {month}")
                else:
                    result = f"📅 Expenses for {month}:\n"
                    for _, row in month_df.iterrows():
                        result += f"• {row['name']} - ₹{row['amount']} ({row['category']})\n"
                    result += f"\n💰 Total: ₹{month_df['amount'].sum()}"
                    await message.channel.send(result)
            except FileExistsError:
                await message.channel.send("No expenses yet..")

    elif message.content.startswith("delete"):
        parts = message.content.split()
        if len(parts) < 2:
            await message.channel.send("❌ Format: delete <name>")
        else:
            try:
                name_to_delete = parts[1].lower()
                df = pd.read_csv("expenses.csv", names=["date","name","amount","category"])
                df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

                original_len = len(df)
                df = df[df["name"].str.lower() != name_to_delete]
                if len(df) == original_len:
                    await message.channel.send(f"❌ No expense found with name: {parts[1]}")
                else:
                    df.to_csv("expenses.csv" , index = False , header = False)
                    await message.channel.send(f"✅ Deleted all entries for: {parts[1]}")
            except FileNotFoundError:
                await message.channel.send("NO expenses yet..")
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
        `help` — Show this message
        """
            await message.channel.send(help_text)
client.run(os.getenv("DISCORD_TOKEN"))
