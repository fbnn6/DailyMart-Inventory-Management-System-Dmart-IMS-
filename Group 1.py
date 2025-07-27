#Group 1
#TP081783, TP082608, TP083154


# === DATABASE ===
def load_users(filename):
    users = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue  # Skip comments and empty lines
                parts = line.split(',')
                if len(parts) == 7:
                    outlet_id, role, fullname, username, password, staff_id, phone = [p.strip() for p in parts]
                    users[username] = {
                        'outlet_id': outlet_id,
                        'role': role,
                        'fullname': fullname,
                        'password': password,
                        'staff_id': staff_id,
                        'phone': phone
                    }
                else:
                    print(f" Skipping malformed line: {line}")
    except FileNotFoundError:
        print(" users.txt not found.")
    return users



# === LOGIN PAGE ===
def login(users):
    print("\n[DailyMart Login System]")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = users.get(username)
    if user and user['password'] == password:
        print(f"\nAccess Granted. Welcome to Daily Mart, {user['fullname']}!")
        print(f"Role: {user['role']}")
        print(f"Outlet: {user['outlet_id']}")
        print(f"Staff ID: {user['staff_id']}")
        print(f"Phone: {user['phone']}")
        return user
    else:
        print("Access Denied. Please try again.")
        return None



# === MAIN MENU ===
def main():
    users = load_users("users.txt")

    print("\nDailyMart Stocks Login Portal. Please confirm your identity.")

    while True:
        user = login(users)
        if user:
            role = user["role"]
            outlet_id = user["outlet_id"]

            if role == "Staff":
                store_staff_menu(user)
            elif role == "Manager":
                store_manager_menu(outlet_id)
            elif role == "head_office":
                head_office_admin_menu()
            else:
                print(f"Role '{role}' not recognized. Contact admin.")
                retry = input("Try login again? (Y/N): ").strip().lower()
                if retry != 'y':
                    print("Exiting system.")
                    break
        else:
            print("Access Denied. Please try again.\n")



# === STORE STAFF MENU ===
def store_staff_menu(user):
    while True:
        print("\n<Staff Dashboard>")
        print("1. View Outlet Stocks")
        print("2. View Stocks Update")
        print("3. Search Inventory")
        print("4. Log out")
        print("5. Exit Program")
        choice = input("Please enter your choice: ")
        stock_files = ["STD001_stocks.txt", "STD002_stocks.txt", "STD003_stocks.txt"]

        if choice == '1':
            view_stock_by_user(user, stock_files)
        elif choice == '2':
            update_stock(user, stock_files)
        elif choice == '3':
            search_inventory(stock_files)
        elif choice == '4':
            print("\nLogout Successfully.\n")
            break  # returns to main login screen
        elif choice == '5':
            print("\nExiting program. Take care!")
            exit()
        else:
            print("Invalid choice. Please try again.")



# === VIEW STOCK PER OUTLET ===
def load_inventory(stock_files):
    combined_stocks = {}

    for stocks_file in stock_files:
        try:
            with open(stocks_file, "r") as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) != 5:
                        print(f" Skipping malformed line in {stocks_file}: {line}")
                        continue
                    outlet_id, category, product_name, product_id, quantity = parts
                    if outlet_id not in combined_stocks:
                        combined_stocks[outlet_id] = {}
                    if category not in combined_stocks[outlet_id]:
                        combined_stocks[outlet_id][category] = []
                    combined_stocks[outlet_id][category].append({
                        "Product Name": product_name,
                        "Product ID": product_id,
                        "Quantity": int(quantity)
                    })
        except FileNotFoundError:
            print(f" Stock file '{stocks_file}' not found.")
    return combined_stocks

def view_stock_by_user(user, stock_files):
    stocks = load_inventory(stock_files)
    outlet_id = user['outlet_id']
    role = user['role'].lower()

    if role == 'head_office' and outlet_id == 'all':
        print("\n Head Office Admin Inventory View:")
        for outlet, categories in stocks.items():
            print(f"\n Outlet {outlet}")
            for category, items in categories.items():
                print(f"\n  {category.capitalize()}:")
                for item in items:
                    print(f"    - {item['Product Name']} (ID: {item['Product ID']}, Qty: {item['Quantity']})")
    else:
        if outlet_id not in stocks:
            print(f"\n No inventory found for Outlet {outlet_id}.")
            return
        print(f"\n Stocks for Outlet {outlet_id} (Categorized):")
        for category, items in stocks[outlet_id].items():
            print(f"\n {category.capitalize()}:")
            for item in items:
                print(f"  --- {item['Product Name']} [ID: {item['Product ID']}, Qty: {item['Quantity']}]")



# === UPDATE STOCK ===
import time

def update_stock(user, stock_files):
    stocks = load_inventory(stock_files)
    outlet_id = user['outlet_id']
    fullname = user['fullname']

    if outlet_id not in stocks:
        print(f"\n No inventory found for Outlet {outlet_id}.")
        return

    print(f"\n Update Stock for Outlet {outlet_id}")
    product_list = []
    for category, items in stocks[outlet_id].items():
        for item in items:
            product_list.append((category, item))

    for idx, (category, item) in enumerate(product_list, 1):
        print(f"{idx}. {item['Product Name']} (ID: {item['Product ID']}, Qty: {item['Quantity']}) [{category}]")

    choice = input("\nSelect product number to update: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(product_list)):
        print(" Invalid selection.")
        return

    selected_category, selected_item = product_list[int(choice) - 1]

    print("\nUpdate Type:")
    print("1. Receive Stock")
    print("2. Record Sales/Expired")
    action_choice = input("Please enter your choice: ").strip()
    if action_choice not in ['1', '2']:
        print(" Invalid choice. Please try again")
        return

    qty_input = input("Enter quantity to update: ").strip()
    if not qty_input.isdigit():
        print(" Quantity must be a positive number.")
        return

    change = int(qty_input)
    change = change if action_choice == '1' else -change
    selected_item['Quantity'] += change

    action_text = "Received" if change > 0 else "Sold/Expired"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    log_entry = f"{timestamp}, {outlet_id}, {selected_item['Product ID']}, {action_text}, Change: {change}, New Qty: {selected_item['Quantity']}, Staff: {fullname}\n"
    with open("stock_update_log.txt", "a") as log_file:
        log_file.write(log_entry)
    print("\nStock System Update Successful!")
    print(f"Product: {selected_item['Product Name']}")
    print(f"Product ID: {selected_item['Product ID']}")
    print(f"Action: {action_text}")
    print(f"Change: {change}")
    print(f"New Quantity: {selected_item['Quantity']}")
    print(f"Outlet: {outlet_id}")
    print(f"Staff: {fullname}")
    print(f"Timestamp: {timestamp}")



# === GENERATE STOCK ALERTS ===
    generate_stock_alerts_from_memory(stocks)

def generate_stock_alerts_from_memory(stocks, threshold=10, log_file="stock_alerts_log.txt"):
    alerts = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for outlet_id, categories in stocks.items():
        for category, items in categories.items():
            for item in items:
                if item['Quantity'] < threshold:
                    alert_entry = {
                        'Timestamp': timestamp,
                        'Outlet': outlet_id,
                        'Category': category,
                        'Product Name': item['Product Name'],
                        'Product ID': item['Product ID'],
                        'Quantity': item['Quantity']
                    }
                    alerts.append(alert_entry)

    if alerts:
        print("\nStock Alert!: The following items are below threshold and need to be restored:")
        with open(log_file, 'a') as file:
            for alert in alerts:
                log_line = (f"{alert['Timestamp']}, {alert['Outlet']}, {alert['Category']}, "
                            f"{alert['Product Name']}, {alert['Product ID']}, Qty: {alert['Quantity']}")
                file.write(log_line + '\n')
                print(f"--- Outlet {alert['Outlet']} | {alert['Category']} ----> "
                      f"{alert['Product Name']} (ID: {alert['Product ID']}) — Qty: {alert['Quantity']}")
    else:
        print("\nNo stock alerts. All inventories are above the threshold.")



# === SEARCH PRODUCTS ===
def search_inventory(stock_files):
    stocks = load_inventory(stock_files)

    print("\nSearch Inventory")
    print("1. By Product Name")
    print("2. By Product ID")
    print("3. By Category")
    search_choice = input("Please enter your choice : ").strip()

    if search_choice not in ['1', '2', '3']:
        print(" Invalid choices. Please try again")
        return

    search_term = input("Enter search keyword: ").strip().lower()
    if not search_term:
        print(" Search term cannot be empty.")
        return

    print("\nSearch Results:")
    found = False
    for outlet_id, categories in stocks.items():
        for category, items in categories.items():
            for item in items:
                if (
                    (search_choice == '1' and search_term in item['Product Name'].lower()) or
                    (search_choice == '2' and search_term in item['Product ID'].lower()) or
                    (search_choice == '3' and search_term in category.lower())
                ):
                    print(f"Outlet: {outlet_id} | Category: {category} | "
                          f"{item['Product Name']} (ID: {item['Product ID']}, Qty: {item['Quantity']})")
                    found = True

    if not found:
        print(" No matching products found.")



# === STORE MANAGER MENU ===
def store_manager_menu(outlet_id):
    while True:
        print(f"\n--- Store Manager Menu (Outlet {outlet_id}) ---")
        print("1. Very & Approve Stock Changes")
        print("2. Restocking Requests")
        print("3. View Store History")
        print("4.Track Deliveries")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            verify_and_approve_stock_changes(outlet_id)
        elif choice == '2':
            request_restock()
        elif choice == '3':
            view_store_history(outlet_id)
        elif choice == '4':
            track_deliveries(outlet_id)
        elif choice == '5':
            print("Exiting Store Manager Menu.")
            break
        else:
            print("Invalid input. Please enter a number between 1 and 5.")



# === VERIFY & APPROVE STOCK CHANGES ===
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

def verify_and_approve_stock_changes(outlet_id):
    updates = load_file(STOCK_UPDATES_FILE)
    pending = [u for u in updates if u.endswith('pending') and u.startswith(outlet_id)]

    if not pending:
        print(f"No pending stock changes for {outlet_id}.")
        return

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

    print("Stock change approved.")



# === RESTOCKING REQUESTS ===
from datetime import datetime

RESTOCK_REQUESTS_FILE = 'restock_requests.txt'
STORE_HISTORY_FILE = 'store_history.txt'

def append_to_file(filename, line):
    try:
        with open(filename, 'a') as file:
            file.write(line + '\n')
    except Exception as e:
        print(f"Error writing to {filename}: {e}")

def request_restock():
    outlet_id = input("Enter your Outlet ID (e.g. STD001): ").strip().upper()
    product_id = input("Enter Product ID: ").strip().upper()
    product_name = input("Enter Product Name: ").strip()
    quantity = input("Enter quantity to request: ").strip()

    if not quantity.isdigit():
        print("Quantity must be a positive number.")
        return

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    restock_entry = f"{outlet_id},{product_id},{product_name},{quantity},{timestamp}"

    append_to_file(RESTOCK_REQUESTS_FILE, restock_entry)
    append_to_file(STORE_HISTORY_FILE, f"RestockRequest:{restock_entry}")

    print("Restocking request submitted.")



# === VIEW STORE HISTORY ===
def view_store_history(outlet_id):
    history = load_file(STORE_HISTORY_FILE)
    filtered = [line for line in history if outlet_id in line]

    if not filtered:
        print(f"No history found for {outlet_id}.")
        return

    for line in filtered:
        print(line)



# === TRACK DELIVERIES ===
DELIVERIES_FILE = 'deliveries.txt'

def track_deliveries(outlet_id):
    deliveries = load_file(DELIVERIES_FILE)
    filtered = [line for line in deliveries if line.startswith(outlet_id)]

    if not filtered:
        print(f"No deliveries found for {outlet_id}.")
        return

    for delivery in filtered:
        print(delivery)



# === HEAD OFFICE ADMIN MENU ===
def head_office_admin_menu():
    while True:
        print("\n===== HEAD OFFICE ADMIN MENU =====")
        print("1. View Multi-Store Inventory")
        print("2. Manage Suppliers & Products")
        print("3. Approve Reorders")
        print("4. Generate Reports")
        print("5. Logout")

        choice = input("Select option (1–5): ").strip()

        if choice == "1":
            view_multi_store_inventory()
        elif choice == "2":
            manage_suppliers_and_products()
        elif choice == "3":
            approve_reorders()
        elif choice == "4":
            generate_reports()
        elif choice == "5":
            print("Logging out of Admin Portal...")
            break
        else:
            print("Invalid input. Please select from 1 to 5.")



# === MULTI-STORE INVENTORY OVERVIEW ===
def view_multi_store_inventory():
    try:
        with open("inventory.txt", "r") as file:
            print("\n--- MULTI-STORE INVENTORY OVERVIEW ---")
            print(f"{'ProductID':<8} {'ProductName':<20} {'Category':<15} {'OutletID':<8} {'Qty':<5} {'Threshold':<9}")
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 6:
                    print(f"{parts[0]:<8} {parts[1]:<20} {parts[2]:<15} {parts[3]:<8} {parts[4]:<5} {parts[5]:<9}")
    except FileNotFoundError:
        print("Error: inventory.txt not found.")



# === SUPPLIER & PRODUCT MANAGEMENT ===
def manage_suppliers_and_products():
    while True:
        print("\n--- SUPPLIER & PRODUCT MANAGEMENT ---")
        print("1. Add Supplier")
        print("2. Edit Supplier")
        print("3. Add New Product to Inventory")
        print("4. Return to Admin Menu")
        choice = input("Enter choice (1–4): ").strip()

        if choice == "1":
            supplier_id = input("Supplier ID (e.g., SPD001): ")
            name = input("Supplier Name: ")
            category = input("Supplied Category: ")
            route = input("Delivery Route (RouteA, RouteB, RouteC): ")
            with open("suppliers.txt", "a") as f:
                f.write(f"{supplier_id},{name},{category},{route}\n")
            print("Supplier added successfully.")

        elif choice == "2":
            supplier_id = input("Enter Supplier ID to edit: ")
            updated = []
            found = False
            try:
                with open("suppliers.txt", "r") as f:
                    for line in f:
                        parts = line.strip().split(",")
                        if parts[0] == supplier_id:
                            found = True
                            print("Editing supplier:", parts)
                            name = input("New Supplier Name: ")
                            category = input("New Category: ")
                            route = input("New Route: ")
                            updated.append(f"{supplier_id},{name},{category},{route}")
                        else:
                            updated.append(line.strip())
                if found:
                    with open("suppliers.txt", "w") as f:
                        for line in updated:
                            f.write(line + "\n")
                    print("Supplier updated.")
                else:
                    print("Supplier ID not found.")
            except FileNotFoundError:
                print("suppliers.txt not found.")

        elif choice == "3":
            product_id = input("Product ID (e.g., P0001): ")
            name = input("Product Name: ")
            category = input("Category: ")
            outlet_id = input("Outlet ID (e.g., STD001): ")
            quantity = input("Initial Quantity: ")
            threshold = input("Reorder Threshold: ")
            with open("inventory.txt", "a") as f:
                f.write(f"{product_id},{name},{category},{outlet_id},{quantity},{threshold}\n")
            print("Product added to inventory.")

        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")



# === APPROVE REORDERS ===
def approve_reorders():
    try:
        with open("restock_requests.txt", "r") as file:
            lines = file.readlines()

        updated_lines = []
        changes_made = False

        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 5 and parts[4].lower() == "pending":
                print(f"\nRequestID: {parts[0]}, Outlet: {parts[1]}, Product: {parts[2]}, Qty: {parts[3]}")
                approve = input("Approve this request? (y/n): ").lower()
                if approve == "y":
                    parts[4] = "approved"
                    changes_made = True
                updated_lines.append(",".join(parts))

        with open("approved_stock.txt", "w") as file:
            for line in updated_lines:
                file.write(line + "\n")

        if changes_made:
            print("Reorders approved.")
        else:
            print("No reorders were approved.")
    except FileNotFoundError:
        print("restock_requests.txt not found.")



# === GENERATE REPORTS ===
def generate_reports():
    try:
        store_stats = {}
        low_stock = {}

        # Read from store_history.txt
        with open("store_history.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 5:
                    outlet_id, pid, action, qty, timestamp = parts[:5]
                    try:
                        qty = int(qty)
                        if outlet_id not in store_stats:
                            store_stats[outlet_id] = {"sale": 0, "receive": 0}
                        if action.lower() == "sale":
                            store_stats[outlet_id]["sale"] += qty
                        elif action.lower() == "receive":
                            store_stats[outlet_id]["receive"] += qty
                    except ValueError:
                        print(f"Skipping line with invalid quantity: {line.strip()}")
                else:
                    print(f"Skipping malformed line in store_history.txt: {line.strip()}")

        # Read inventory for low stock count
        with open("inventory.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    pid, name, cat, outlet_id, qty, threshold = parts[:6]
                    try:
                        if int(qty) < int(threshold):
                            low_stock[outlet_id] = low_stock.get(outlet_id, 0) + 1
                    except ValueError:
                        print(f"Skipping line with invalid stock values: {line.strip()}")
                else:
                    print(f"Skipping malformed line in inventory.txt: {line.strip()}")

        # Write report
        with open("reports.txt", "w") as f:
            for outlet_id in store_stats:
                sale = store_stats[outlet_id]["sale"]
                received = store_stats[outlet_id]["receive"]
                low_items = low_stock.get(outlet_id, 0)
                f.write(f"{outlet_id}, TotalSold:{sale}, Restocked:{received}, LowStockItems:{low_items}\n")

        print("Reports generated and saved to reports.txt.")

    except FileNotFoundError as e:
        print(f"Missing file: {e.filename}")




# === CLOSING ===
if __name__ == "__main__":
    main()
