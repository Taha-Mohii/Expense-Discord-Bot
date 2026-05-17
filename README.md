<div align="center">

# 💸 ExpenseBot

### A personal finance tracker that lives inside Discord.

Log expenses, analyze spending, visualize trends, and export data — all from a single Discord server. No apps. No spreadsheets. Just type and go.

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://python.org)
[![Discord](https://img.shields.io/badge/Discord.py-2.0-5865F2?style=flat-square&logo=discord)](https://discordpy.readthedocs.io)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=flat-square&logo=supabase)](https://supabase.com)
[![Railway](https://img.shields.io/badge/Deployed-Railway-0B0D0E?style=flat-square&logo=railway)](https://railway.app)

</div>

---

## 📸 What It Does

> Type `add Lords 250 Food` in Discord → expense saved to cloud database instantly.
> Type `chart` → get a pie chart of your spending breakdown.
> Type `export` → receive an Excel file with all your data.

No login. No UI. Just your Discord server.

---

## ⚡ Commands

| Command | What it does |
|---|---|
| `add <name> <amount> <category>` | Log a new expense |
| `today` | View all expenses from today |
| `summary` | Total amount spent (all time) |
| `month <YYYY-MM>` | Full breakdown for any month |
| `chart` | Pie chart of spending by category |
| `export` | Download data as `.xlsx` Excel file |
| `delete <name>` | Remove all entries for a merchant |
| `ping` | Check bot status |
| `help` | List all commands |

---

## 🏗 Architecture

```
Discord Server
      │
      ▼
  discord.py bot (main.py)
      │
      ├──► database.py (psycopg2)
      │         │
      │         ▼
      │    Supabase (PostgreSQL)
      │    Cloud database — persists 24/7
      │
      ├──► matplotlib → pie chart → Discord
      │
      └──► openpyxl → .xlsx file → Discord
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Bot Framework | discord.py |
| Database | PostgreSQL via Supabase |
| DB Driver | psycopg2 |
| Charts | matplotlib |
| Excel Export | openpyxl |
| Secrets | python-dotenv |
| Deployment | Railway (24/7) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A Discord account and bot token
- A free Supabase account

### 1. Clone the repo
```bash
git clone https://github.com/Taha-Mohii/expense-tracker-bot.git
cd expense-tracker-bot
```

### 2. Install dependencies
```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Mac/Linux

pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the root:
```env
DISCORD_TOKEN=your_discord_bot_token
DATABASE_URL=your_supabase_connection_string
```

### 4. Set up the database
In your Supabase project, create a table called `expenses`:

```sql
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    date TEXT,
    name TEXT,
    amount REAL,
    category TEXT
);
```

### 5. Run locally
```bash
python main.py
```

---

## ☁️ Deployment

This bot is deployed on **Railway** and runs 24/7 without keeping your PC on.

1. Push code to GitHub
2. Connect repo to [Railway](https://railway.app)
3. Add `DISCORD_TOKEN` and `DATABASE_URL` as environment variables
4. Railway auto-deploys on every `git push`

---

## 📁 Project Structure

```
expense-tracker-bot/
│
├── main.py            # Bot logic and all command handlers
├── database.py        # All database functions (Supabase/PostgreSQL)
├── requirements.txt   # Python dependencies
├── Procfile           # Railway deployment config
│
├── .env               # Secret keys — never pushed to GitHub
└── .gitignore
```

---

## 🔒 Security

- API keys and database credentials stored in `.env`
- `.env` excluded from version control via `.gitignore`
- No sensitive data pushed to GitHub

---

## 🗺 Roadmap

- [ ] Budget limits with overspending alerts
- [ ] Weekly spending report
- [ ] Multi-currency support
- [ ] Web dashboard

---

## 👤 Author

**Taha Mohii** — CS Student, graduating 2028

[![GitHub](https://img.shields.io/badge/GitHub-Taha--Mohii-181717?style=flat-square&logo=github)](https://github.com/Taha-Mohii)

---

<div align="center">

⭐ If you found this useful, consider starring the repo!

</div>
