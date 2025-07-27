# GROUP 1
# TP123456, TP987654, TP0129834

DELIVERIES_FILE = 'deliveries.txt'

def load_file(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def track_deliveries(outlet_id):
    deliveries = load_file(DELIVERIES_FILE)
    filtered = [line for line in deliveries if line.startswith(outlet_id)]

    if not filtered:
        print(f"No deliveries found for {outlet_id}.")
        return

    print(f"\n--- All Deliveries for {outlet_id} ---")
    for delivery in filtered:
        print(delivery)
        
if __name__ == "__main__":
    outlet = input("Enter your outlet ID (e.g. STD001): ").strip().upper()
    print("\n1. View All Deliveries\n2. View Estimated (Pending) Deliveries")
    choice = input("Choose option (1/2): ").strip()
    if choice == '1':
        track_deliveries(outlet)
    elif choice == '2':
        view_estimated_delivery(outlet)
    else:
        print("Invalid option.")
