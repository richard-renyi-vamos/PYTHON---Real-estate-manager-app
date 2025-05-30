import csv
import os

FILENAME = "properties.csv"

def load_properties():
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Location", "Price", "Bedrooms", "Status"])
    with open(FILENAME, mode="r") as file:
        return list(csv.DictReader(file))

def save_properties(properties):
    with open(FILENAME, mode="w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Location", "Price", "Bedrooms", "Status"])
        writer.writeheader()
        writer.writerows(properties)

def add_property():
    props = load_properties()
    new_id = str(len(props) + 1)
    location = input("Location: ")
    price = input("Price ($): ")
    bedrooms = input("Bedrooms: ")
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
        print(f"{p['ID']:<5}{p['Location']:<20}${p['Price']:<10}{p['Bedrooms']:<7}{p['Status']}")

def update_property():
    props = load_properties()
    view_properties()
    id_to_update = input("\nEnter Property ID to update: ")
    found = False
    for p in props:
        if p["ID"] == id_to_update:
            p["Location"] = input("New Location: ")
            p["Price"] = input("New Price: ")
            p["Bedrooms"] = input("New Bedrooms: ")
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
    criteria = input("Search by (location/price): ").lower()
    if criteria == "location":
        loc = input("Enter location keyword: ").lower()
        result = [p for p in props if loc in p["Location"].lower()]
    elif criteria == "price":
        min_p = float(input("Min Price: "))
        max_p = float(input("Max Price: "))
        result = [p for p in props if min_p <= float(p["Price"]) <= max_p]
    else:
        print("❗ Invalid criteria.")
        return
    print("\n🔍 Search Results:")
    for p in result:
        print(p)

def menu():
    while True:
        print("\n🏘️ Real Estate Manager 🏘️")
        print("1. View All Properties")
        print("2. Add New Property")
        print("3. Update Property")
        print("4. Delete Property")
        print("5. Search Property")
        print("6. Exit")

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
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    menu()
