#GROUP 1
#TP123456, TP987654, TP0129834

STORE_HISTORY_FILE = 'store_history.txt'

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

    for line in filtered:
        print(line)

if __name__ == "__main__":
    outlet = input("Enter your outlet ID (e.g. STD001): ").strip().upper()
    view_store_history(outlet)
