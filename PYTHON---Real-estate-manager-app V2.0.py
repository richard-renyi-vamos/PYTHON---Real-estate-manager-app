import csv
import os
import shutil

FILENAME = "properties.csv"

def backup_file():
    if os.path.exists(FILENAME):
        shutil.copy(FILENAME, FILENAME + ".bak")

def load_properties():
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Location", "Price", "Bedrooms", "Status"])
    with open(FILENAME, mode="r") as file:
        return list(csv.DictReader(file))

def save_properties(properties):
    backup_file()
    with open(FILENAME, mode="w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Location", "Price", "Bedrooms", "Status"])
        writer.writeheader()
        writer.writerows(properties)

def get_valid_number(prompt, number_type=float):
    while True:
        try:
            return number_type(input(prompt))
        except ValueError:
            print("🚫 Invalid input. Please enter a number.")

def get_next_id(properties):
    if not properties:
        return "1"
    return str(max(int(p["ID"]) for p in properties) + 1)

def color_status(status):
    colors = {"Available": "\033[92m", "Sold": "\033[91m", "Rented": "\033[93m"}
    return f"{colors.get(status, '')}{status}\033[0m"

def add_property():
    props = load_properties()
    new_id = get_next_id(props)
    location = input("Location: ")
    price = str(get_valid_number("Price ($): "))
    bedrooms = str(get_valid_number("Bedrooms: ", int))
    status = input("Status (Available/Sold/Rented): ")

    props.append({"ID": new_id, "Location": location, "Price": price, "Bedrooms": bedrooms, "Status": status})
    save_properties(props)
    print("✅ Property added!")

def view_properties():
    props = load_properties()
    if not props:
        print("No properties found.")
        return
    print(f"\n{'ID':<5}{'Location':<20}{'Price':<10}{'Beds':<7}{'Status'}")
    print("-"*50)
    for p in props:
        print(f"{p['ID']:<5}{p['Location']:<20}${p['Price']:<10}{p['Bedrooms']:<7}{color_status(p['Status'])}")

def update_property():
    props = load_properties()
    view_properties()
    id_to_update = input("\nEnter Property ID to update: ")
    found = False
    for p in props:
        if p["ID"] == id_to_update:
            p["Location"] = input("New Location: ")
            p["Price"] = str(get_valid_number("New Price: "))
            p["Bedrooms"] = str(get_valid_number("New Bedrooms: ", int))
            p["Status"] = input("New Status: ")
            found = True
            break
    if found:
        save_properties(props)
        print("🔄 Property updated.")
    else:
        print("❌ Property not found.")

def delete_property():
    props = load_properties()
    view_properties()
    id_to_delete = input("\nEnter Property ID to delete: ")
    new_props = [p for p in props if p["ID"] != id_to_delete]
    if len(new_props) != len(props):
        save_properties(new_props)
        print("🗑️ Property deleted.")
    else:
        print("❌ Property not found.")

def search_property():
    props = load_properties()
    criteria = input("Search by (location/price/status/bedrooms): ").lower()
    result = []

    if criteria == "location":
        loc = input("Enter location keyword: ").lower()
        result = [p for p in props if loc in p["Location"].lower()]
    elif criteria == "price":
        min_p = get_valid_number("Min Price: ")
        max_p = get_valid_number("Max Price: ")
        result = [p for p in props if min_p <= float(p["Price"]) <= max_p]
    elif criteria == "status":
        stat = input("Enter status: ").lower()
        result = [p for p in props if stat == p["Status"].lower()]
    elif criteria == "bedrooms":
        min_bed = int(get_valid_number("Min Bedrooms: ", int))
        max_bed = int(get_valid_number("Max Bedrooms: ", int))
        result = [p for p in props if min_bed <= int(p["Bedrooms"]) <= max_bed]
    else:
        print("❗ Invalid criteria.")
        return

    print("\n🔍 Search Results:")
    if not result:
        print("No matching properties found.")
        return
    for p in result:
        print(p)

def sort_properties():
    props = load_properties()
    key = input("Sort by (price/bedrooms): ").lower()
    reverse = input("Descending? (y/n): ").lower() == "y"
    if key in ["price", "bedrooms"]:
        props.sort(key=lambda x: float(x[key.capitalize()]), reverse=reverse)
        for p in props:
            print(p)
    else:
        print("❗ Invalid sort key.")

def export_report():
    props = load_properties()
    with open("property_report.txt", "w") as f:
        f.write(f"{'ID':<5}{'Location':<20}{'Price':<10}{'Beds':<7}{'Status'}\n")
        f.write("-"*50 + "\n")
        for p in props:
            f.write(f"{p['ID']:<5}{p['Location']:<20}${p['Price']:<10}{p['Bedrooms']:<7}{p['Status']}\n")
    print("📄 Report saved to property_report.txt")

def menu():
    while True:
        print("\n🏘️ Real Estate Manager 🏘️")
        print("1. View All Properties")
        print("2. Add New Property")
        print("3. Update Property")
        print("4. Delete Property")
        print("5. Search Property")
        print("6. Sort Properties")
        print("7. Export Report")
        print("8. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            view_properties()
        elif choice == "2":
            add_property()
        elif choice == "3":
            update_property()
        elif choice == "4":
            delete_property()
        elif choice == "5":
            search_property()
        elif choice == "6":
            sort_properties()
        elif choice == "7":
            export_report()
        elif choice == "8":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    menu()
