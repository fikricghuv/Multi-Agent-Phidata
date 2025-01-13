# Gunakan image Python versi terbaru
FROM python:3.12

# Tentukan direktori kerja dalam container
WORKDIR /app

# Salin file requirements.txt ke dalam container
COPY requirements.txt .

# Instal dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi ke dalam container
COPY . .

# Tentukan port yang akan digunakan aplikasi
EXPOSE 8003

# Perintah default untuk menjalankan aplikasi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
