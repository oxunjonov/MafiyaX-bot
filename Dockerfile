FROM python:3.11-slim

WORKDIR /app

# Barcha fayllarni avval nusxa qilish
COPY . .

# Keyin kutubxonalarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Botni ishga tushirish
CMD ["python", "bot.py"]
