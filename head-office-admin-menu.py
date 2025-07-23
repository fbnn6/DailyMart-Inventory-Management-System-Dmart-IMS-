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
