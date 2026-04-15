import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

DATASET_PATH = "dataset"


# Load classes
def get_classes():
    return sorted(os.listdir(DATASET_PATH))


# Get random video from class
def get_random_video(class_name):
    class_path = os.path.join(DATASET_PATH, class_name)
    videos = [v for v in os.listdir(class_path) if v.endswith(".mp4")]
    return os.path.join(class_path, random.choice(videos))


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    classes = get_classes()

    keyboard = []
    for cls in classes:
        keyboard.append([InlineKeyboardButton(cls, callback_data=f"class|{cls}")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📚 Choose a class:",
        reply_markup=reply_markup
    )


# HANDLE BUTTONS
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("|")

    # 👉 SELECT CLASS
    if data[0] == "class":
        class_name = data[1]

        # save class in memory
        context.user_data["class"] = class_name

        video_path = get_random_video(class_name)

        keyboard = [
            [
                InlineKeyboardButton("🔁 Next", callback_data="next"),
                InlineKeyboardButton("⬅️ Back", callback_data="back")
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_video(
            video=open(video_path, "rb"),
            caption=f"Class: {class_name}",
            reply_markup=reply_markup
        )

    # 👉 NEXT VIDEO
    elif data[0] == "next":
        class_name = context.user_data.get("class")

        if not class_name:
            await query.message.reply_text("⚠️ No class selected")
            return

        video_path = get_random_video(class_name)

        keyboard = [
            [
                InlineKeyboardButton("🔁 Next", callback_data="next"),
                InlineKeyboardButton("⬅️ Back", callback_data="back")
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_video(
            video=open(video_path, "rb"),
            caption=f"Class: {class_name}",
            reply_markup=reply_markup
        )

    # 👉 BACK TO MENU
    elif data[0] == "back":
        classes = get_classes()

        keyboard = []
        for cls in classes:
            keyboard.append([InlineKeyboardButton(cls, callback_data=f"class|{cls}")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "📚 Choose a class:",
            reply_markup=reply_markup
        )