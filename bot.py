
BOT_TOKEN = "BOT_TOKEN = "BOT_TOKEN = "8217667510:AAEho8ILr-t7HrBuPE5Kjx9U1HjZv2DM8v8"


from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Data store
achievements = {}
runs = {}
wickets = {}

ADMIN_ID = "6293455550"

# /add_achievement <text>
async def add_achievement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Sirf admin hi achievement add kar sakta hai.")
        return
    user = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
    text = " ".join(context.args)
    achievements.setdefault(user.id, []).append(text)
    await update.message.reply_text(f"✅ Achievement added for {user.first_name}!")

# /my_achievements
async def my_achievements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_achievements = achievements.get(user_id, [])
    if user_achievements:
        msg = "\n".join(f"🏆 {a}" for a in user_achievements)
    else:
        msg = "😕 No achievements yet."
    await update.message.reply_text(msg)

# /add_runs <number>
async def add_runs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        run = int(context.args[0])
        user = update.effective_user
        runs[user.id] = runs.get(user.id, 0) + run
        await update.message.reply_text(f"✅ {run} runs added for {user.first_name}")
    except:
        await update.message.reply_text("⚠️ Sahi format: /add_runs 100")

# /add_wickets <number>
async def add_wickets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        wicket = int(context.args[0])
        user = update.effective_user
        wickets[user.id] = wickets.get(user.id, 0) + wicket
        await update.message.reply_text(f"✅ {wicket} wickets added for {user.first_name}")
    except:
        await update.message.reply_text("⚠️ Sahi format: /add_wickets 2")

# /most_runs
async def most_runs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_runs = sorted(runs.items(), key=lambda x: x[1], reverse=True)[:5]
    if sorted_runs:
        msg = "🏏 Top 5 Run Scorers:
" + "\n".join(
            [f"{i+1}. {context.bot.get_chat(uid).first_name}: {score} runs" for i, (uid, score) in enumerate(sorted_runs)]
        )
    else:
        msg = "❌ No runs recorded yet."
    await update.message.reply_text(msg)

# /most_wickets
async def most_wickets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_wickets = sorted(wickets.items(), key=lambda x: x[1], reverse=True)[:5]
    if sorted_wickets:
        msg = "🎯 Top 5 Wicket Takers:
" + "\n".join(
            [f"{i+1}. {context.bot.get_chat(uid).first_name}: {score} wickets" for i, (uid, score) in enumerate(sorted_wickets)]
        )
    else:
        msg = "❌ No wickets recorded yet."
    await update.message.reply_text(msg)

# Start Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to the Cricket Bot!")

app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add_achievement", add_achievement))
app.add_handler(CommandHandler("my_achievements", my_achievements))
app.add_handler(CommandHandler("add_runs", add_runs))
app.add_handler(CommandHandler("add_wickets", add_wickets))
app.add_handler(CommandHandler("most_runs", most_runs))
app.add_handler(CommandHandler("most_wickets", most_wickets))

app.run_polling()
