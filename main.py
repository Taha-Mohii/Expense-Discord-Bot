
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
        if len(parts) < 3 :
            await message.channel.send(" Format: add <name> <amount>")
        else:
            name = parts[1]
            amount = float(parts[2])
            today_date = datetime.now().strftime("%Y-%m-%d")
            with open("expenses.csv","a",newline="") as f:
                writer = csv.writer(f)
                writer.writerow([today_date,name,amount])
                await message.channel.send(f"✅ Saved! {name} - ₹{amount}")


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
            df = pd.read_csv("expenses.csv", names=["date","name","amount"])
            df["amount"] = pd.to_numeric(df["amount"],errors="coerce")
            category_spending = df.groupby("name")["amount"].sum().dropna()

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

client.run(os.getenv("DISCORD_TOKEN"))
