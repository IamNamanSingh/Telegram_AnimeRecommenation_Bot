import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ================== CONFIG ==================

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"  # <-- replace with your token

# Anime database with details
GENRE_SHOWS = {
    "shonen": [
        {
            "title": "Naruto",
            "episodes": 220,
            "rating": 7.9,  # MyAnimeList approx rating
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/20/Naruto",
        },
        {
            "title": "One Piece",
            "episodes": 1100,  # Ongoing, huge episode count
            "rating": 8.7,
            "status": "Ongoing",
            "mal_url": "https://myanimelist.net/anime/21/One_Piece",
        },
        {
            "title": "Bleach",
            "episodes": 366,
            "rating": 8.1,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/269/Bleach",
        },
        {
            "title": "Jujutsu Kaisen",
            "episodes": 47,
            "rating": 8.6,
            "status": "Ongoing",
            "mal_url": "https://myanimelist.net/anime/40748/Jujutsu_Kaisen",
        },
        {
            "title": "My Hero Academia",
            "episodes": 138,
            "rating": 7.9,
            "status": "Ongoing",
            "mal_url": "https://myanimelist.net/anime/31964/Boku_no_Hero_Academia",
        },
    ],
    "seinen": [
        {
            "title": "Monster",
            "episodes": 74,
            "rating": 8.9,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/19/Monster",
        },
        {
            "title": "Vinland Saga",
            "episodes": 48,
            "rating": 8.7,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/37521/Vinland_Saga",
        },
        {
            "title": "Psycho-Pass",
            "episodes": 22,
            "rating": 8.3,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/13601/Psycho-Pass",
        },
        {
            "title": "Tokyo Ghoul",
            "episodes": 12,
            "rating": 7.8,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/22319/Tokyo_Ghoul",
        },
        {
            "title": "Berserk (1997)",
            "episodes": 25,
            "rating": 8.4,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/323/Berserk",
        },
    ],
    "psychological": [
        {
            "title": "Death Note",
            "episodes": 37,
            "rating": 8.6,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/1535/Death_Note",
        },
        {
            "title": "Code Geass",
            "episodes": 25,
            "rating": 8.7,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/1575/Code_Geass__Hangyaku_no_Lelouch",
        },
        {
            "title": "Steins;Gate",
            "episodes": 24,
            "rating": 9.0,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/9253/Steins_Gate",
        },
        {
            "title": "Parasyte: The Maxim",
            "episodes": 24,
            "rating": 8.3,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/22535/Kiseijuu__Sei_no_Kakuritsu",
        },
        {
            "title": "Serial Experiments Lain",
            "episodes": 13,
            "rating": 8.0,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/339/Serial_Experiments_Lain",
        },
    ],
    "sports": [
        {
            "title": "Haikyuu!!",
            "episodes": 25,
            "rating": 8.5,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/20583/Haikyuu",
        },
        {
            "title": "Blue Lock",
            "episodes": 24,
            "rating": 8.3,
            "status": "Ongoing",
            "mal_url": "https://myanimelist.net/anime/49596/Blue_Lock",
        },
        {
            "title": "Kuroko no Basket",
            "episodes": 25,
            "rating": 8.2,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/11771/Kuroko_no_Basket",
        },
        {
            "title": "Hajime no Ippo",
            "episodes": 75,
            "rating": 8.7,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/263/Hajime_no_Ippo",
        },
        {
            "title": "Ace of Diamond",
            "episodes": 75,
            "rating": 8.1,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/18689/Diamond_no_A",
        },
    ],
    "romance": [
        {
            "title": "Your Lie in April",
            "episodes": 22,
            "rating": 8.6,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/23273/Shigatsu_wa_Kimi_no_Uso",
        },
        {
            "title": "Horimiya",
            "episodes": 13,
            "rating": 8.2,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/42897/Horimiya",
        },
        {
            "title": "Toradora!",
            "episodes": 25,
            "rating": 8.1,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/4224/Toradora",
        },
        {
            "title": "Clannad: After Story",
            "episodes": 24,
            "rating": 8.9,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/4181/Clannad__After_Story",
        },
        {
            "title": "Kaguya-sama: Love is War",
            "episodes": 12,
            "rating": 8.4,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/37999/Kaguya-sama_wa_Kokurasetai__Tensai-tachi_no_Renai_Zunousen",
        },
    ],
    "slice_of_life": [
        {
            "title": "Anohana: The Flower We Saw That Day",
            "episodes": 11,
            "rating": 8.3,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/9989/Ano_Hi_Mita_Hana_no_Namae_wo_Bokutachi_wa_Mada_Shiranai",
        },
        {
            "title": "Grand Blue",
            "episodes": 12,
            "rating": 8.4,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/37105/Grand_Blue",
        },
        {
            "title": "Insomniacs After School",
            "episodes": 13,
            "rating": 7.9,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/51096/Kimi_wa_Houkago_Insomnia",
        },
        {
            "title": "Barakamon",
            "episodes": 12,
            "rating": 8.4,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/22789/Barakamon",
        },
        {
            "title": "March Comes in Like a Lion",
            "episodes": 22,
            "rating": 8.4,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/31646/3-gatsu_no_Lion",
        },
    ],
    "fantasy": [
        {
            "title": "Fullmetal Alchemist: Brotherhood",
            "episodes": 64,
            "rating": 9.1,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/5114/Fullmetal_Alchemist__Brotherhood",
        },
        {
            "title": "Re:Zero − Starting Life in Another World",
            "episodes": 25,
            "rating": 8.2,
            "status": "Ongoing",
            "mal_url": "https://myanimelist.net/anime/31240/Re_Zero_kara_Hajimeru_Isekai_Seikatsu",
        },
        {
            "title": "Magi: The Labyrinth of Magic",
            "episodes": 25,
            "rating": 8.0,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/14513/Magi__The_Labyrinth_of_Magic",
        },
        {
            "title": "Made in Abyss",
            "episodes": 13,
            "rating": 8.6,
            "status": "Ongoing",
            "mal_url": "https://myanimelist.net/anime/34599/Made_in_Abyss",
        },
        {
            "title": "No Game No Life",
            "episodes": 12,
            "rating": 8.1,
            "status": "Completed",
            "mal_url": "https://myanimelist.net/anime/19815/No_Game_No_Life",
        },
    ],
}

# ============================================
# Logging
# ============================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# ============================================
# Helper functions
# ============================================

def get_all_anime():
    """Return a flat list of all anime dicts across all genres."""
    all_shows = []
    for genre_list in GENRE_SHOWS.values():
        all_shows.extend(genre_list)
    return all_shows


def format_anime_list(genre_name: str, shows: list) -> str:
    """Format a list of anime with details into markdown text."""
    pretty_name = genre_name.replace("_", " ").title()
    lines = [f"🔥 *Top {pretty_name} Anime:*", ""]

    for anime in shows:
        title = anime["title"]
        episodes = anime.get("episodes", "N/A")
        rating = anime.get("rating", "N/A")
        status = anime.get("status", "N/A")
        mal_url = anime.get("mal_url")

        lines.append(f"*{title}*")
        lines.append(f"Episodes: `{episodes}`")
        lines.append(f"MAL Rating (approx): `{rating}`")
        lines.append(f"Status: `{status}`")
        if mal_url:
            lines.append(f"[MyAnimeList]({mal_url})")
        lines.append("")  # empty line between entries

    lines.append("Want more? Use /start to pick another genre or ⭐ Suggestions.")
    return "\n".join(lines)


def format_suggestions(suggestions: list) -> str:
    """Format random suggestions into markdown text."""
    lines = ["⭐ *Anime Suggestions For You:*", ""]
    for anime in suggestions:
        title = anime["title"]
        episodes = anime.get("episodes", "N/A")
        rating = anime.get("rating", "N/A")
        status = anime.get("status", "N/A")
        mal_url = anime.get("mal_url")

        lines.append(f"*{title}*")
        lines.append(f"Episodes: `{episodes}`")
        lines.append(f"MAL Rating (approx): `{rating}`")
        lines.append(f"Status: `{status}`")
        if mal_url:
            lines.append(f"[MyAnimeList]({mal_url})")
        lines.append("")  # gap

    lines.append("Not satisfied? Tap ⭐ Suggestions again or choose a genre with /start.")
    return "\n".join(lines)


# ============================================
# Handlers
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message and show genre buttons + suggestions."""
    user_first_name = update.effective_user.first_name

    text = (
        f"Yo {user_first_name}! 👋\n\n"
        "I'm your Anime Recommendation Bot.\n"
        "Choose a genre below or tap ⭐ Suggestions if you're not sure what to watch.\n\n"
        "I'll show you:\n"
        "• Episodes 📺\n"
        "• MyAnimeList rating ⭐ (approx)\n"
        "• Completed or ongoing ✅"
    )

    keyboard = []
    row = []

    # Genre buttons
    for genre_key in GENRE_SHOWS.keys():
        pretty_name = genre_key.replace("_", " ").title()
        row.append(InlineKeyboardButton(pretty_name, callback_data=f"genre:{genre_key}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Suggestions button row
    keyboard.append([InlineKeyboardButton("⭐ Suggestions", callback_data="suggestions")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        # In case start is triggered from a button later
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Explain how to use the bot."""
    text = (
        "⭐ *How to use this bot:*\n"
        "/start - Show the genre menu + suggestions\n"
        "/help - Show this help message\n\n"
        "• Tap any genre to see detailed anime lists.\n"
        "• Tap ⭐ Suggestions to get random recommendations."
    )
    await update.message.reply_markdown(text)


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle clicks on genre buttons and suggestions."""
    query = update.callback_query
    await query.answer()

    data = query.data

    # Suggestions button
    if data == "suggestions":
        all_shows = get_all_anime()
        # pick up to 3 random shows (or less if db small)
        num = min(3, len(all_shows))
        suggestions = random.sample(all_shows, num)
        reply_text = format_suggestions(suggestions)
        await query.edit_message_text(text=reply_text, parse_mode="Markdown")
        return

    # Genre buttons
    if data.startswith("genre:"):
        genre_key = data.split(":", 1)[1]
        shows = GENRE_SHOWS.get(genre_key, [])
        if not shows:
            pretty_name = genre_key.replace("_", " ").title()
            reply_text = f"Sorry, I don't have recommendations for *{pretty_name}* yet 😢"
            await query.edit_message_text(text=reply_text, parse_mode="Markdown")
            return

        reply_text = format_anime_list(genre_key, shows)
        await query.edit_message_text(text=reply_text, parse_mode="Markdown")
        return


# ============================================
# Main function
# ============================================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
