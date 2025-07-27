# GROUP 1s
# TP123456, TP987654, TP0129834

from datetime import datetime

STOCK_UPDATES_FILE = 'stock_updates.txt'
APPROVED_STOCK_FILE = 'approved_stock.txt'
STORE_HISTORY_FILE = 'store_history.txt'

def load_file(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def save_file(filename, lines):
    with open(filename, 'w') as file:
        for line in lines:
            file.write(line + '\n')

def append_to_file(filename, line):
    with open(filename, 'a') as file:
        file.write(line + '\n')

def receive_delivery(outlet_id):
    updates = load_file(STOCK_UPDATES_FILE)
    pending = [u for u in updates if u.endswith('pending') and u.startswith(outlet_id)]

    if not pending:
        print(f"No pending stock changes for {outlet_id}.")
        return

    print(f"\nPending Deliveries for {outlet_id}:")
    for i, update in enumerate(pending):
        print(f"{i + 1}. {update}")

    choice = input("Enter number to approve: ").strip()
    if not choice.isdigit():
        print("Invalid input.")
        return

    index = int(choice) - 1
    if index < 0 or index >= len(pending):
        print("Choice out of range.")
        return

    approved_line = pending[index]
    parts = approved_line.split(',')
    parts[-1] = 'approved'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    approved_entry = ','.join(parts) + f",{timestamp}"

    append_to_file(APPROVED_STOCK_FILE, approved_entry)
    append_to_file(STORE_HISTORY_FILE, f"Approved: {approved_entry}")

    updates.remove(approved_line)
    save_file(STOCK_UPDATES_FILE, updates)

    print("Stock delivery approved and recorded.")

# Optional for testing this file alone
if __name__ == "__main__":
    outlet = input("Enter your outlet ID (e.g. STD001): ").strip().upper()
    receive_delivery(outlet)
