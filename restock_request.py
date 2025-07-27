#GROUP 1
#TP123456, TP987654, TP0129834

from datetime import datetime

RESTOCK_REQUESTS_FILE = 'restock_requests.txt'
STORE_HISTORY_FILE = 'store_history.txt'

def append_to_file(filename, line):
    with open(filename, 'a') as file:
        file.write(line + '\n')

def request_restock():
    outlet_id = input("Enter your outlet ID (e.g. STD001): ").strip().upper()
    product_id = input("Enter Product ID: ").strip().upper()
    product_name = input("Enter Product Name: ").strip()
    quantity = input("Enter quantity to request: ").strip()

    if not quantity.isdigit():
        print("Quantity must be a number.")
        return

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"{outlet_id},{product_id},{product_name},{quantity},{timestamp}"

    append_to_file(RESTOCK_REQUESTS_FILE, line)
    append_to_file(STORE_HISTORY_FILE, f"RestockRequest:{line}")

    print("Restocking request submitted.")

if __name__ == "__main__":
    request_restock()
