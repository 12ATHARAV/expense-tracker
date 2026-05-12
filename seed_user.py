import os, sys, random, datetime

# Ensure the project root is on the path
project_root = r"C:\Users\athar\Downloads\expense-tracker"
sys.path.insert(0, project_root)

from werkzeug.security import generate_password_hash
from database.db import get_db

# --- Realistic Indian names by region ---
first_names = [
    'Aarav', 'Aanya', 'Aarush', 'Aditi', 'Advait', 'Ahana', 'Aiden', 'Akash',
    'Amara', 'Ananya', 'Anika', 'Arjun', 'Arnav', 'Arya', 'Avani', 'Bhavna',
    'Chirag', 'Daksh', 'Dev', 'Diya', 'Dhruv', 'Esha', 'Gaurav', 'Gayatri',
    'Ishaan', 'Ishika', 'Jai', 'Janvi', 'Kabir', 'Kaira', 'Karan', 'Kavya',
    'Kiara', 'Krish', 'Lakshya', 'Lavanya', 'Madhav', 'Mahi', 'Meera', 'Mira',
    'Naira', 'Nakul', 'Neha', 'Nikhil', 'Nisha', 'Om', 'Prisha', 'Raghav',
    'Raj', 'Riya', 'Rohan', 'Rudra', 'Saanvi', 'Sadhana', 'Sahil', 'Sanika',
    'Sara', 'Sarthak', 'Shloka', 'Sneha', 'Sooraj', 'Tanvi', 'Tanish',
    'Urvi', 'Vanya', 'Varun', 'Ved', 'Vihaan', 'Yash', 'Zara'
]

last_names = [
    'Sharma', 'Patel', 'Singh', 'Kumar', 'Reddy', 'Nair', 'Gupta', 'Das',
    'Mukherjee', 'Chowdhury', 'Iyer', 'Menon', 'Jain', 'Bansal', 'Kapoor',
    'Malhotra', 'Mehta', 'Pillai', 'Rao', 'Sen', 'Shah', 'Tiwari', 'Verma',
    'Yadav', 'Agarwal', 'Ghosh', 'Banerjee', 'Saxena', 'Bharadwaj',
    'Nambiar', 'Chettiar', 'Lal', 'Bhagat', "D'Souza", 'Fernandes', 'Gonsalves',
    'Kamat', 'Lobo', 'Mascarenhas', 'Noronha', 'Pereira', 'Quadros', 'Rodrigues'
]

# Generate a random Indian user
name = f'{random.choice(first_names)} {random.choice(last_names)}'
number_suffix = random.randint(10, 999)
email = name.lower().replace(' ', '.') + str(number_suffix) + '@gmail.com'
password_hash = generate_password_hash('password123')
created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

os.chdir(project_root)
db = get_db()

# Ensure users table exists
db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")

# Check for unique email, regenerate if needed
cursor = db.execute('SELECT id FROM users WHERE email = ?', (email,))
while cursor.fetchone() is not None:
    number_suffix = random.randint(10, 999)
    email = name.lower().replace(' ', '.') + str(number_suffix) + '@gmail.com'
    cursor = db.execute('SELECT id FROM users WHERE email = ?', (email,))

# Insert the user
db.execute(
    'INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)',
    (name, email, password_hash, created_at)
)
db.commit()

# Fetch back to confirm
user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
db.close()

print('User seeded successfully!')
print(f'  id:         {user["id"]}')
print(f'  name:       {user["name"]}')
print(f'  email:      {user["email"]}')
print(f'  created_at: {user["created_at"]}')