import sqlite3
import hashlib

# Fungsi untuk hash password agar lebih aman
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Inisialisasi database & tabel admin
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# Tambahkan admin baru jika belum ada
def add_admin(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Admin sudah ada
    conn.close()

# Fungsi untuk login
def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Inisialisasi database saat pertama kali dijalankan
init_db()
