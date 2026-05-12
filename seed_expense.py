import os, sys, random, datetime, traceback

# --- Step 1 — Parse arguments ---
args = sys.argv[1:]
if len(args) != 3:
    print("Usage: /seed-expenses <user_id> <count> <months>")
    print("Example: /seed-expenses 1 50 6")
    sys.exit(1)

try:
    user_id = int(args[0])
    count = int(args[1])
    months = int(args[2])
except ValueError:
    print("Usage: /seed-expenses <user_id> <count> <months>")
    print("Example: /seed-expenses 1 50 6")
    sys.exit(1)

if user_id < 1 or count < 1 or months < 1:
    print("Usage: /seed-expenses <user_id> <count> <months>")
    print("Example: /seed-expenses 1 50 6")
    sys.exit(1)

# --- Imports and DB setup ---
project_root = r"C:\Users\athar\Downloads\expense-tracker"
sys.path.insert(0, project_root)
os.chdir(project_root)

from database.db import get_db

db = get_db()

# --- Step 2 — Verify user exists ---
cursor = db.execute("SELECT id FROM users WHERE id = ?", (user_id,))
if cursor.fetchone() is None:
    print(f"No user found with id {user_id}.")
    db.close()
    sys.exit(1)

# --- Step 3 — Generate and insert expenses ---

# Category definitions: (category, min_amount, max_amount)
category_ranges = {
    "Food":          (50, 800),
    "Transport":     (20, 500),
    "Bills":         (200, 3000),
    "Health":        (100, 2000),
    "Entertainment": (100, 1500),
    "Shopping":      (200, 5000),
    "Other":         (50, 1000),
}

# Weighted distribution — Food most common, Health/Entertainment least
categories_weighted = (
    ["Food"] * 25 +
    ["Transport"] * 15 +
    ["Bills"] * 12 +
    ["Shopping"] * 12 +
    ["Other"] * 10 +
    ["Entertainment"] * 8 +
    ["Health"] * 6
)

# Realistic Indian descriptions per category
descriptions = {
    "Food": [
        "Lunch at Swad restaurant", "Grocery shopping at Big Bazaar",
        "Street food at Connaught Place", "Dinner at home — dal & roti",
        "Chai and samosa at local stall", "BBQ with friends",
        "Monthly veg box delivery", "Cafe latte and croissant",
        "Biryani treat at Saravana Bhavan", "Snacks for evening chai",
        "Paneer tikka at dhaba", "Sweets from Haldiram's",
        "Mutton curry dinner", "Idli-sambar breakfast",
        "Pizza delivery on Sunday", "Thali at Gujarati restaurant",
        "Fish fry at food court", "Momos and noodles",
        "Weekend brunch buffet", "Pickle and papad order",
        "Ice cream outing", "Fruit juice cart visit"
    ],
    "Transport": [
        "Auto-rickshaw to office", "Ola cab to airport",
        "Metro monthly pass recharge", "Fuel refill — two-wheeler",
        "BMTC bus pass monthly", "Uber ride to mall",
        "Train ticket — local", "Taxi to railway station",
        "Bolt ride home late night", "Parking fee at mall",
        "Toll charges NH48", "Shared cab to office",
        "Rental scooter weekend", "Bus fare daily commute",
        "Meru cab to hospital", "Delivery bike fuel top-up"
    ],
    "Bills": [
        "Electricity bill — BESCOM", "Mobile recharge — Jio",
        "Water bill — municipality", "Broadband — ACT Fibernet",
        "Gas cylinder refill", "Rent — April",
        "DTH recharge — Tata Play", "LIC premium payment",
        "Credit card bill payment", "Society maintenance charge",
        "Municipal tax payment", "Internet bill — Airtel",
        "Cooking gas booking", "Annual insurance premium",
        "Property tax payment", "Netflix and Hotstar subscription"
    ],
    "Health": [
        "Doctor consultation — general physician", "Pharmacy — cough syrup",
        "Dental check-up", "Lab test — blood work",
        "Gym membership renewal", "Medicine for fever",
        "Eye check-up and spectacles", "Yoga class drop-in",
        "Vitamin supplements", "Ayurvedic massage therapy",
        "COVID booster shot", "Health insurance premium",
        "Dentist — root canal", "Skin treatment at clinic",
        "Physiotherapy session", "Homeopathy consultation"
    ],
    "Entertainment": [
        "Movie tickets — INOX", "Netflix annual plan",
        "Concert tickets — Arijit Singh live", "Bowling with friends",
        "Video game purchase — Steam", "Book from Crossword",
        "Amusement park entry", "Cricket match tickets — IPL",
        "Karaoke night out", "Museum entry ticket",
        "Board games order online", "Comedy show tickets",
        "Zoo visit with family", "Streaming subscription — Spotify",
        "Escape room tickets", "Stand-up comedy show"
    ],
    "Shopping": [
        "Clothes at Pantaloons", "Electronics — new earphones",
        "Grocery monthly stock-up", "Shoes from Bata",
        "Amazon order — books", "Diwali gifts shopping",
        "Furniture — bookshelf", "Makeup and skincare",
        "Stationery for kids", "Saree shopping",
        "Mobile accessories", "Kitchen utensils order",
        "Backpack for college", "Watch purchase",
        "Bed linens and pillows", "Fruits and veggies weekly"
    ],
    "Other": [
        "Haircut at local salon", "Laundry service",
        "Courier parcel charges", "Pet food supplies",
        "Flower shop — temple offering", "Charity donation",
        "Printing and photocopy", "Newspaper subscription",
        "Magazine subscription", "Gift wrapping supplies",
        "Candles and incense", "Plant nursery visit",
        "Hardware store — nails and paint", "Tailoring charges",
        "Dry cleaning", "Courier speed post"
    ]
}

today = datetime.date.today()

expenses = []
for _ in range(count):
    category = random.choice(categories_weighted)
    lo, hi = category_ranges[category]
    amount = round(random.uniform(lo, hi), 2)
    # Spread across past <months> months
    days_ago = random.randint(0, months * 30)
    expense_date = today - datetime.timedelta(days=days_ago)
    date_str = expense_date.strftime("%Y-%m-%d")
    desc = random.choice(descriptions[category])
    expenses.append((user_id, amount, category, date_str, desc))

# Insert all in a single transaction
try:
    for exp in expenses:
        db.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            exp,
        )
    db.commit()
except Exception:
    db.rollback()
    traceback.print_exc()
    db.close()
    sys.exit(1)

# --- Step 4 — Confirm ---
print(f"\n[OK] {count} expenses seeded for user_id {user_id}!\n")

# Fetch back to confirm and show sample
rows = db.execute(
    "SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC LIMIT 5", (user_id,)
).fetchall()

dates_in_db = db.execute(
    "SELECT MIN(date), MAX(date) FROM expenses WHERE user_id = ?", (user_id,)
).fetchone()

print(f"Total inserted: {count}")
print(f"Date range:     {dates_in_db[0]} -> {dates_in_db[1]}")
print(f"\nSample of 5 records:")
print(f"{'id':<5} {'amount':>8}  {'category':<14} {'date':<12} description")
print("-" * 70)
for r in rows:
    print(f"{r['id']:<5} Rs.{r['amount']:>7.2f}  {r['category']:<14} {r['date']:<12} {r['description']}")

db.close()