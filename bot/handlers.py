import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

DATASET_PATH = "dataset"


# 📂 Get categories
def get_categories():
    return sorted(os.listdir(DATASET_PATH))


# 📚 Get classes inside category
def get_classes(category):
    path = os.path.join(DATASET_PATH, category)
    return sorted(os.listdir(path))


# 🎥 Get random video
def get_random_video(category, class_name):
    class_path = os.path.join(DATASET_PATH, category, class_name)
    videos = [v for v in os.listdir(class_path) if v.endswith(".mp4")]
    return os.path.join(class_path, random.choice(videos))


# 🚀 START → show categories
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = get_categories()

    keyboard = []
    for cat in categories:
        keyboard.append([InlineKeyboardButton(cat, callback_data=f"cat|{cat}")])

    await update.message.reply_text(
        "📂 ជ្រើសរើសប្រភេទ:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🔘 HANDLE BUTTONS
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("|")

    # 👉 CATEGORY CLICK
    if data[0] == "cat":
        category = data[1]
        context.user_data["category"] = category

        classes = get_classes(category)

        keyboard = []
        for cls in classes:
            keyboard.append([InlineKeyboardButton(cls, callback_data=f"class|{cls}")])

        keyboard.append([InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data="back_home")])

        await query.message.reply_text(
            f"📚 {category}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 👉 CLASS CLICK
    elif data[0] == "class":
        class_name = data[1]
        category = context.user_data.get("category")

        context.user_data["class"] = class_name

        video_path = get_random_video(category, class_name)

        keyboard = [
            [
                InlineKeyboardButton("🔁 បន្ទាប់", callback_data="next"),
                InlineKeyboardButton("⬅️ ត្រឡប់", callback_data="back_category")
            ]
        ]

        await query.message.reply_video(
            video=open(video_path, "rb"),
            caption=f"{category} → {class_name}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 👉 NEXT VIDEO
    elif data[0] == "next":
        category = context.user_data.get("category")
        class_name = context.user_data.get("class")

        video_path = get_random_video(category, class_name)

        keyboard = [
            [
                InlineKeyboardButton("🔁 បន្ទាប់", callback_data="next"),
                InlineKeyboardButton("⬅️ ត្រឡប់", callback_data="back_category")
            ]
        ]

        await query.message.reply_video(
            video=open(video_path, "rb"),
            caption=f"{category} → {class_name}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 👉 BACK TO CLASS LIST
    elif data[0] == "back_category":
        category = context.user_data.get("category")
        classes = get_classes(category)

        keyboard = []
        for cls in classes:
            keyboard.append([InlineKeyboardButton(cls, callback_data=f"class|{cls}")])

        keyboard.append([InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data="back_home")])

        await query.message.reply_text(
            f"📚 {category}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 👉 BACK TO HOME
    elif data[0] == "back_home":
        await start(update, context)