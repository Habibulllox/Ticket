# 🎫 Customer Support Ticket System

Mijozlar murojaatlarini boshqarish tizimi (Django + DRF).

## 📌 Loyiha haqida

Bu tizim orqali foydalanuvchilar muammo (ticket) yaratadi, admin esa ularni ko'radi, javob yozadi va statusini boshqaradi.

## ✨ Xususiyatlar

- 🔐 Auth (admin va client rollari)
- 🎫 Ticket yaratish, ko'rish, tahrirlash
- 📊 Status boshqaruvi (new, in_progress, closed)
- ⚡ Priority (low, normal, high)
- 🖼️ Rasm yuklash
- 💬 Comment tizimi
- 🌐 REST API (DRF)

## 🚀 O'rnatish

```bash
git clone <repo_url>
cd support_system
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver