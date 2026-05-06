import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

labs = ['524', '526', '528', '530', '544', '542']
total_updated = 0

for lab in labs:
    cursor.execute(
        "UPDATE lab_software SET lab = ? WHERE lab = ?",
        ('Lab ' + lab, lab)
    )
    updated = cursor.rowcount
    if updated > 0:
        print(f'  Updated {updated} record(s): "{lab}" → "Lab {lab}"')
    total_updated += updated

conn.commit()
conn.close()

if total_updated == 0:
    print("No records needed migration (already in correct format).")
else:
    print(f"\nDone! {total_updated} record(s) migrated successfully.")