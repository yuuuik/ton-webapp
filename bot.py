from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

# 🔐 Токены твоих ботов
TOKENS = {
    "registration": "8067394334:AAH_3TQzhEmUxDnQa2qIp9h1_jC4IveBI3E",
    "fd": "7715772145:AAFd3tcitQ2Xuvp3P5xo3NdAm2TppZEbqUs",
    "rd": "7715772145:AAFd3tcitQ2Xuvp3P5xo3NdAm2TppZEbqUs",
    "launch": "7858033672:AAFuLLyxNoAnYk1AnWgUQdXaieeHMcb40Co"
}

CHAT_ID = "1135347132"

# 🌍 Список стран (код → флаг + название)
country_map = {
    "ru": "🇷🇺 Россия", "in": "🇮🇳 Индия", "uz": "🇺🇿 Узбекистан", "ua": "🇺🇦 Украина",
    "kg": "🇰🇬 Киргизия", "tj": "🇹🇯 Таджикистан", "az": "🇦🇿 Азербайджан", "am": "🇦🇲 Армения",
    "md": "🇲🇩 Молдова", "by": "🇧🇾 Беларусь", "tr": "🇹🇷 Турция", "mx": "🇲🇽 Мексика",
    "cl": "🇨🇱 Чили", "ar": "🇦🇷 Аргентина", "ve": "🇻🇪 Венесуэла", "co": "🇨🇴 Колумбия",
    "ec": "🇪🇨 Эквадор", "cr": "🇨🇷 Коста-Рика", "br": "🇧🇷 Бразилия", "id": "🇮🇩 Индонезия",
    "bd": "🇧🇩 Бангладеш", "th": "🇹🇭 Таиланд", "kh": "🇰🇭 Камбоджа", "lk": "🇱🇰 Шри-Ланка",
    "pk": "🇵🇰 Пакистан", "my": "🇲🇾 Малайзия", "ph": "🇵🇭 Филиппины", "kr": "🇰🇷 Южная Корея",
    "jp": "🇯🇵 Япония", "ca": "🇨🇦 Канада", "vn": "🇻🇳 Вьетнам", "qa": "🇶🇦 Катар",
    "ae": "🇦🇪 ОАЭ", "ci": "🇨🇮 Кот-д’Ивуар", "cm": "🇨🇲 Камерун", "bf": "🇧🇫 Буркина-Фасо",
    "ke": "🇰🇪 Кения", "sn": "🇸🇳 Сенегал", "ug": "🇺🇬 Уганда", "gh": "🇬🇭 Гана",
    "bj": "🇧🇯 Бенин", "tg": "🇹🇬 Того", "eg": "🇪🇬 Египет", "tz": "🇹🇿 Танзания",
    "rw": "🇷🇼 Руанда", "cd": "🇨🇩 ДР Конго", "zm": "🇿🇲 Замбия", "ng": "🇳🇬 Нигерия"
}

def send_to_telegram(token, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

@app.route("/postback", methods=["GET"])
def postback():
    event = request.args.get("event", "unknown")
    user_id = request.args.get("user_id", "—")
    amount = request.args.get("amount", "—")
    country = request.args.get("country", "—")
    sub1 = request.args.get("sub1", "—")
    sub3 = request.args.get("sub3", "—")
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M МСК")

    country_name = country_map.get(country.lower(), country.upper())

    if event == "fd":
        msg = f"""💰 <b>Первый депозит</b>\n\n🆔 1win ID: <code>{user_id}</code>\n🌍 GEO: {country_name}\n🔹 Sub1: {sub1}\n🔹 Sub3: {sub3}\n💵 Сумма: <b>{amount} $</b>\n🕒 Дата: {timestamp}"""
    elif event == "rd":
        msg = f"""🔁 <b>Повторный депозит</b>\n\n🆔 1win ID: <code>{user_id}</code>\n🌍 GEO: {country_name}\n🔹 Sub1: {sub1}\n🔹 Sub3: {sub3}\n💵 Сумма: <b>{amount} $</b>\n🕒 Дата: {timestamp}"""
    elif event == "registration":
        msg = f"""🟢 <b>Регистрация</b>\n\n🆔 1win ID: <code>{user_id}</code>\n🌍 GEO: {country_name}\n🔹 Sub1: {sub1}\n🔹 Sub3: {sub3}\n🕒 Дата: {timestamp}"""
    elif event == "launch":
        msg = f"""🚀 <b>Запуск приложения</b>\n\n🆔 1win ID: <code>{user_id}</code>\n🌍 GEO: {country_name}\n🔹 Sub1: {sub1}\n🔹 Sub3: {sub3}\n🕒 Дата: {timestamp}"""
    else:
        msg = f"⚠️ Неизвестное событие: {event}"

    token = TOKENS.get(event)
    if token:
        send_to_telegram(token, msg)
        return "OK"
    else:
        return "Invalid event", 400

@app.route("/", methods=["GET"])
def home():
    return "1win postback bot is online!"
