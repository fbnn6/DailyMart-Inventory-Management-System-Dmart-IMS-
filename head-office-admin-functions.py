# === HEAD OFFICE ADMIN MENU ===
def head_office_admin_menu():
    while True:
        print("\n===== HEAD OFFICE ADMIN MENU =====")
        print("1. View Multi-Store Inventory")
        print("2. Manage Suppliers & Products")
        print("3. Approve Restock Requests")
        print("4. Generate Reports")
        print("5. Logout")

        choice = input("Select option (1–5): ").strip()

        if choice == "1":
            view_multi_store_inventory()
        elif choice == "2":
            manage_suppliers_and_products()
        elif choice == "3":
            approve_restock_requests()
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
            print(f"{'ProductID':<8} {'ProductName':<20} {'Category':<15} {'OutletID':8} {'Outlet':<12} {'Qty':<5} {'Threshold':<9}")
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 7:
                    print(f"{parts[0]:<8} {parts[1]:<20} {parts[2]:<15} {parts[3]:<8} {parts[4]:<12} {parts[5]:<5} {parts[6]:<9}")
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
            outlet = input("Outlet Name (e.g., Outlet_A): ")
            quantity = input("Initial Quantity: ")
            threshold = input("Reorder Threshold: ")
            with open("inventory.txt", "a") as f:
                f.write(f"{product_id},{name},{category},{outlet_id},{outlet},{quantity},{threshold}\n")
            print("Product added to inventory.")

        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")


# === APPROVE RESTOCK REQUESTS ===
def approve_restock_requests():
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
            else:
                updated_lines.append(line.strip())

        with open("restock_requests.txt", "w") as file:
            for line in updated_lines:
                file.write(line + "\n")

        if changes_made:
            print("Restock requests approved.")
        else:
            print("No changes made.")
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
                outlet, pid, action, qty, timestamp = line.strip().split(",")
                qty = int(qty)
                if outlet not in store_stats:
                    store_stats[outlet] = {"sale": 0, "receive": 0}
                if action == "sale":
                    store_stats[outlet]["sale"] += qty
                elif action == "receive":
                    store_stats[outlet]["receive"] += qty

        # Read inventory for low stock count
        with open("inventory.txt", "r") as f:
            for line in f:
                pid, name, cat, outlet, qty, threshold = line.strip().split(",")
                if int(qty) < int(threshold):
                    low_stock[outlet] = low_stock.get(outlet, 0) + 1

        # Write to reports.txt
        with open("reports.txt", "w") as f:
            for outlet in store_stats:
                sale = store_stats[outlet]["sale"]
                received = store_stats[outlet]["receive"]
                low_items = low_stock.get(outlet, 0)
                f.write(f"{outlet},TotalSold:{sale},Restocked:{received},LowStockItems:{low_items}\n")

        print("Reports generated and saved to reports.txt.")
    except FileNotFoundError as e:
        print(f"Missing file: {e.filename}")

