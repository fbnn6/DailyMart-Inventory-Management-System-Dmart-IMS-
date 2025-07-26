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

def login(users):
    print("\n[DailyMart Login System]")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = users.get(username)
    if user and user['password'] == password:
        print(f"\nAccess Granted.Welcome to Daily Mart, {user['fullname']}!")
        print(f"Role: {user['role']}")
        print(f"Outlet: {user['outlet_id']}")
        print(f"Staff ID: {user['staff_id']}")
        print(f"Phone: {user['phone']}")
        return user
    else:
        print("Access Denied. Please try again.")
        return None
if __name__ == "_main_":
    users = load_users("users.txt")
    logged_in_user = login(users)
    if logged_in_user:
        # Trigger outlet-specific or admin functions here
        pass

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

def main():
    users = load_users("users.txt")

    # Show this message only once
    print("\nDailyMart Stocks Login Portal. Please confirm your identity.")

    while True:
        user = login(users)
        if user:
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
                    break  # returns to logi n prompt
                elif choice == '5':
                    print("\nExiting program. Take care!")
                    return
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Access Denied. Please try again.\n")


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

    generate_stock_alerts_from_memory(stocks)
from datetime import datetime
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

if __name__ == "__main__":
    main()














