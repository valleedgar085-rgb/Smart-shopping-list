#!/usr/bin/env python3
"""
Command-line interface for Smart Shopping List Application
Provides an interactive way to manage offices, supplies, and stores.
"""

import sys
from shopping_list import Office, Store, SmartShoppingList


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def add_office_interactive(smart_list):
    """Interactively add an office and its supplies."""
    print_header("ADD OFFICE")
    
    office_name = input("Enter office name: ").strip()
    if not office_name:
        print("Office name cannot be empty.")
        return
    
    office = Office(office_name)
    
    print(f"\nAdding supplies for {office_name}")
    print("Enter items (type 'done' when finished):")
    
    while True:
        item_name = input("  Item name (or 'done'): ").strip()
        if item_name.lower() == 'done':
            break
        
        if not item_name:
            print("  Item name cannot be empty.")
            continue
        
        try:
            quantity = int(input(f"  Quantity for {item_name}: "))
            if quantity <= 0:
                print("  Quantity must be positive.")
                continue
            office.add_item(item_name, quantity)
            print(f"  ✓ Added {quantity} {item_name}")
        except ValueError:
            print("  Invalid quantity. Please enter a number.")
    
    smart_list.add_office(office)
    print(f"\n✓ Office '{office_name}' added successfully!")


def add_store_interactive(smart_list):
    """Interactively add a store and its prices."""
    print_header("ADD STORE")
    
    store_name = input("Enter store name: ").strip()
    if not store_name:
        print("Store name cannot be empty.")
        return
    
    store = Store(store_name)
    
    print(f"\nAdding prices for {store_name}")
    print("Enter item prices (type 'done' when finished):")
    
    while True:
        item_name = input("  Item name (or 'done'): ").strip()
        if item_name.lower() == 'done':
            break
        
        if not item_name:
            print("  Item name cannot be empty.")
            continue
        
        try:
            price = float(input(f"  Price for {item_name}: $"))
            if price < 0:
                print("  Price cannot be negative.")
                continue
            store.set_price(item_name, price)
            print(f"  ✓ Set {item_name} price to ${price:.2f}")
        except ValueError:
            print("  Invalid price. Please enter a number.")
    
    smart_list.add_store(store)
    print(f"\n✓ Store '{store_name}' added successfully!")


def show_results(smart_list):
    """Display the merged list, price comparison, and cheapest option."""
    print_header("CONSOLIDATED SHOPPING LIST")
    
    merged = smart_list.merge_supplies()
    if not merged:
        print("\nNo supplies added yet.")
        return
    
    print("\nMerged Shopping List from All Offices:")
    for item, quantity in sorted(merged.items()):
        print(f"  • {item}: {quantity}")
    
    if not smart_list.stores:
        print("\nNo stores added yet. Add stores to see price comparison.")
        return
    
    print_header("PRICE COMPARISON")
    
    comparison = smart_list.get_price_comparison()
    for store_name, data in sorted(comparison.items()):
        print(f"\n{store_name}:")
        if data['unavailable_items']:
            print(f"  Status: ⚠ Missing items - {', '.join(data['unavailable_items'])}")
        else:
            print(f"  Total Cost: ${data['total']:.2f}")
    
    print_header("CHEAPEST OPTION")
    
    cheapest_store, total, _ = smart_list.find_cheapest_store()
    
    if cheapest_store:
        print(f"\n🏆 Best Choice: {cheapest_store.name}")
        print(f"Total Cost: ${total:.2f}")
        
        print("\nItemized Breakdown:")
        for item, quantity in sorted(merged.items()):
            price = cheapest_store.get_price(item)
            subtotal = price * quantity
            print(f"  • {item}: {quantity} × ${price:.2f} = ${subtotal:.2f}")
        
        # Calculate savings
        all_totals = [
            data['total'] for data in comparison.values()
            if data['total'] != float('inf')
        ]
        if len(all_totals) > 1:
            max_cost = max(all_totals)
            savings = max_cost - total
            if savings > 0:
                savings_pct = (savings / max_cost) * 100
                print(f"\n💰 You save ${savings:.2f} ({savings_pct:.1f}%) vs. most expensive option!")
    else:
        print("\n⚠ No store has all required items in stock.")


def main_menu():
    """Display and handle the main menu."""
    smart_list = SmartShoppingList()
    
    print("\n" + "=" * 60)
    print("SMART SHOPPING LIST - Multi-Office Management System")
    print("=" * 60)
    
    while True:
        print("\n" + "-" * 60)
        print("MENU:")
        print("  1. Add an office with supplies")
        print("  2. Add a store with prices")
        print("  3. View results (merged list & cheapest store)")
        print("  4. Load sample data (demo)")
        print("  5. Exit")
        print("-" * 60)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            add_office_interactive(smart_list)
        elif choice == '2':
            add_store_interactive(smart_list)
        elif choice == '3':
            show_results(smart_list)
        elif choice == '4':
            load_sample_data(smart_list)
            print("\n✓ Sample data loaded successfully!")
        elif choice == '5':
            print("\nThank you for using Smart Shopping List!")
            sys.exit(0)
        else:
            print("\n⚠ Invalid choice. Please enter 1-5.")


def load_sample_data(smart_list):
    """Load sample data for demonstration."""
    # Create 4 offices
    office1 = Office("Office 1 - New York")
    office1.add_item("Pens", 10)
    office1.add_item("Paper Reams", 5)
    office1.add_item("Staplers", 2)
    
    office2 = Office("Office 2 - Boston")
    office2.add_item("Pens", 15)
    office2.add_item("Paper Reams", 3)
    office2.add_item("Folders", 20)
    
    office3 = Office("Office 3 - Chicago")
    office3.add_item("Paper Reams", 7)
    office3.add_item("Folders", 10)
    office3.add_item("Markers", 8)
    
    office4 = Office("Office 4 - Seattle")
    office4.add_item("Staplers", 3)
    office4.add_item("Markers", 12)
    office4.add_item("Pens", 5)
    
    smart_list.add_office(office1)
    smart_list.add_office(office2)
    smart_list.add_office(office3)
    smart_list.add_office(office4)
    
    # Create stores
    store_a = Store("Office Depot")
    store_a.set_price("Pens", 1.50)
    store_a.set_price("Paper Reams", 8.00)
    store_a.set_price("Staplers", 5.00)
    store_a.set_price("Folders", 0.50)
    store_a.set_price("Markers", 2.00)
    
    store_b = Store("Staples")
    store_b.set_price("Pens", 1.25)
    store_b.set_price("Paper Reams", 8.50)
    store_b.set_price("Staplers", 4.50)
    store_b.set_price("Folders", 0.60)
    store_b.set_price("Markers", 1.75)
    
    store_c = Store("Amazon")
    store_c.set_price("Pens", 1.00)
    store_c.set_price("Paper Reams", 7.50)
    store_c.set_price("Staplers", 4.00)
    store_c.set_price("Folders", 0.45)
    store_c.set_price("Markers", 1.80)
    
    smart_list.add_store(store_a)
    smart_list.add_store(store_b)
    smart_list.add_store(store_c)


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting... Thank you for using Smart Shopping List!")
        sys.exit(0)
