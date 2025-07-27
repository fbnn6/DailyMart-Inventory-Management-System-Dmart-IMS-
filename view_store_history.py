# GROUP 1
# TP123456, TP987654, TP0129834

STOCK_FILE = 'stock_data.txt'
STORE_HISTORY_FILE = 'store_history.txt'

def view_stock(outlet_id):
    try:
        with open(STOCK_FILE, 'r') as file:
            lines = file.readlines()
            print(f"\n--- Current Stock for Outlet {outlet_id} ---")
            found = False
            for line in lines:
                if line.startswith("#"):  # Skip comment/header
                    continue
                parts = line.strip().split(',')
                if parts[0] == outlet_id:
                    print(f"Category: {parts[1]}, Product: {parts[2]}, ID: {parts[3]}, Quantity: {parts[4]}")
                    found = True
            if not found:
                print("No stock found for this outlet.")
    except FileNotFoundError:
        print("Error: stock_data.txt file not found.")

def load_file(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def view_store_history(outlet_id):
    history = load_file(STORE_HISTORY_FILE)
    filtered = [line for line in history if outlet_id in line]

    if not filtered:
        print(f"No history found for {outlet_id}.")
        return

    print(f"\n--- Store History for {outlet_id} ---")
    for line in filtered:
        print(line)

if __name__ == "__main__":
    outlet = input("Enter your outlet ID (e.g. STD001): ").strip().upper()
    view_store_history(outlet)
