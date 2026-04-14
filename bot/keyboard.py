from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def build_class_keyboard(classes, page=0, per_page=8):
    start = page * per_page
    end = start + per_page

    keyboard = []

    for cls in classes[start:end]:
        keyboard.append([
            InlineKeyboardButton(f"👉 {cls}", callback_data=f"class:{cls}")
        ])

    navigation = []

    if start > 0:
        navigation.append(
            InlineKeyboardButton("⬅️", callback_data=f"page:{page-1}")
        )

    if end < len(classes):
        navigation.append(
            InlineKeyboardButton("➡️", callback_data=f"page:{page+1}")
        )

    if navigation:
        keyboard.append(navigation)

    keyboard.append([
        InlineKeyboardButton("🏠 Home", callback_data="home")
    ])

    return InlineKeyboardMarkup(keyboard)