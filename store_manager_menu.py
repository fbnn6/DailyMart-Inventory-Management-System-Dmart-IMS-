from view_store_history import view_stock
from verify_approve_stock import receive_delivery
from track_deliveries import track_deliveries, view_estimated_delivery


def store_manager_menu(outlet_id):
    while True:
        print(f"\n--- Store Manager Menu (Outlet {outlet_id}) ---")
        print("1. View Stock")
        print("2. Track Deliveries")
        print("3. View Estimated Delivery Times")
        print("4. Receive Delivery (Add Stock)")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            view_stock(outlet_id)
        elif choice == '2':
            track_deliveries(outlet_id)
        elif choice == '3':
            view_estimated_delivery(outlet_id)
        elif choice == '4':
            receive_delivery(outlet_id)
        elif choice == '5':
            print("Exiting Store Manager Menu.")
            break
        else:
            print("Invalid input. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    store_manager_menu("STD001")