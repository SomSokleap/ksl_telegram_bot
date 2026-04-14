from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils.dataset_loader import get_all_classes, get_sample_video
from bot.keyboard import build_class_keyboard

CLASSES = get_all_classes()


# ===================== START =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Browse Classes", callback_data="browse")],
        [InlineKeyboardButton("🔍 Search", callback_data="search")],
    ]

    await update.message.reply_text(
        "🇰🇭 Khmer Sign Language Bot\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===================== CALLBACK =====================
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # ---------- HOME ----------
    if data == "home":
        keyboard = [
            [InlineKeyboardButton("📚 Browse Classes", callback_data="browse")],
            [InlineKeyboardButton("🔍 Search", callback_data="search")],
        ]

        await query.message.edit_text(
            "🇰🇭 Khmer Sign Language Bot\n\nChoose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---------- BROWSE ----------
    elif data == "browse":
        keyboard = build_class_keyboard(CLASSES)

        await query.message.edit_text(
            "📚 Select a class:",
            reply_markup=keyboard
        )

    # ---------- PAGINATION ----------
    elif data.startswith("page:"):
        page = int(data.split(":")[1])
        keyboard = build_class_keyboard(CLASSES, page=page)

        await query.message.edit_reply_markup(reply_markup=keyboard)

    # ---------- CLASS ----------
    elif data.startswith("class:"):
        class_name = data.split(":")[1]

        video_path = get_sample_video(class_name)

        keyboard = [
            [
                InlineKeyboardButton("🔁 Next", callback_data=f"class:{class_name}"),
                InlineKeyboardButton("📂 More", callback_data=f"more:{class_name}")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="browse"),
                InlineKeyboardButton("🏠 Home", callback_data="home")
            ]
        ]

        # ✅ FIX: keep navigation working
        await query.message.edit_text(
            text=f"📂 Class: {class_name}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        # ✅ Send video separately
        if video_path:
            await query.message.reply_document(
                document=open(video_path, "rb")
            )
        else:
            await query.message.reply_text("⚠️ No video found.")

    # ---------- MORE ----------
    elif data.startswith("more:"):
        class_name = data.split(":")[1]

        for _ in range(3):
            video_path = get_sample_video(class_name)
            if video_path:
                await query.message.reply_document(
                    document=open(video_path, "rb")
                )

    # ---------- SEARCH ----------
    elif data == "search":
        await query.message.reply_text("🔍 Type class name:")
        context.user_data["search_mode"] = True


# ===================== TEXT =====================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("search_mode"):
        query_text = update.message.text.lower()

        results = [c for c in CLASSES if query_text in c.lower()]

        if results:
            keyboard = build_class_keyboard(results)
            await update.message.reply_text(
                "Results:",
                reply_markup=keyboard
            )
        else:
            await update.message.reply_text("❌ No match found.")

        context.user_data["search_mode"] = False