# 🇰🇭 Khmer Sign Language Telegram Bot

A Telegram bot for browsing and exploring a **Khmer Sign Language (KSL)** video dataset with 100 classes.

---

## 🚀 Features

* 📚 Browse sign language classes
* 🎥 View random video samples
* 🔁 Get different examples (Next)
* 📂 View multiple videos per class
* 🔍 Search by class name
* 🏠 Simple and clean navigation

---

## 📁 Dataset Structure

Each folder represents one class:

```
dataset/
├── class_name/
│   ├── video1.mp4
│   ├── video2.mp4
```

---

## ⚙️ Setup

1. Install dependencies:

```
pip install python-telegram-bot==20.0
```

2. Create a bot using BotFather and get your token

3. Add token in `config.py`:

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

---

## ▶️ Run

```
python -m bot.main
```

---

## 📱 Usage

* Open your bot in Telegram
* Type `/start`
* Browse or search classes
* Click a class to view videos

---

## ⚠️ Notes

* Use `.mp4` videos (recommended)
* Videos are sent as files to preserve quality
* Keep file size under Telegram limits (~50MB)

---

## 📌 Future Work

* AI sign recognition
* Quiz / learning mode
* Favorites system

---

## 📄 License

For educational and research purposes.
# sign_language_reocognition_telegram_bot
