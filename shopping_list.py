#!/usr/bin/env python3
"""
Smart Shopping List Application
Manages supplies for multiple offices, merges them, and finds the cheapest store.
"""

from collections import defaultdict
from typing import Dict, List, Tuple


class Office:
    """Represents an office with its supply needs."""
    
    def __init__(self, name: str):
        self.name = name
        self.supplies = defaultdict(int)  # item_name -> quantity
    
    def add_item(self, item: str, quantity: int = 1):
        """Add an item to this office's supply list."""
        self.supplies[item] += quantity
    
    def get_supplies(self) -> Dict[str, int]:
        """Get all supplies for this office."""
        return dict(self.supplies)


class Store:
    """Represents a store with its prices."""
    
    def __init__(self, name: str):
        self.name = name
        self.prices = {}  # item_name -> price
    
    def set_price(self, item: str, price: float):
        """Set the price for an item."""
        self.prices[item] = price
    
    def get_price(self, item: str) -> float:
        """Get the price of an item, return infinity if not available."""
        return self.prices.get(item, float('inf'))


class SmartShoppingList:
    """Main application class for managing the smart shopping list."""
    
    def __init__(self):
        self.offices = []
        self.stores = []
    
    def add_office(self, office: Office):
        """Add an office to the system."""
        self.offices.append(office)
    
    def add_store(self, store: Store):
        """Add a store to the system."""
        self.stores.append(store)
    
    def merge_supplies(self) -> Dict[str, int]:
        """Merge supplies from all offices into one consolidated list."""
        merged = defaultdict(int)
        for office in self.offices:
            for item, quantity in office.get_supplies().items():
                merged[item] += quantity
        return dict(merged)
    
    def calculate_store_total(self, store: Store, shopping_list: Dict[str, int]) -> Tuple[float, List[str]]:
        """Calculate total cost for a store and identify unavailable items."""
        total = 0.0
        unavailable = []
        
        for item, quantity in shopping_list.items():
            price = store.get_price(item)
            if price == float('inf'):
                unavailable.append(item)
            else:
                total += price * quantity
        
        return total, unavailable
    
    def find_cheapest_store(self) -> Tuple[Store, float, Dict[str, int]]:
        """
        Find the store with the cheapest total for the merged shopping list.
        Returns: (cheapest_store, total_cost, merged_shopping_list)
        """
        merged_list = self.merge_supplies()
        
        if not merged_list:
            return None, 0.0, {}
        
        if not self.stores:
            return None, 0.0, merged_list
        
        cheapest_store = None
        cheapest_total = float('inf')
        
        for store in self.stores:
            total, unavailable = self.calculate_store_total(store, merged_list)
            
            # Only consider stores that have all items
            if not unavailable and total < cheapest_total:
                cheapest_total = total
                cheapest_store = store
        
        return cheapest_store, cheapest_total, merged_list
    
    def get_price_comparison(self) -> Dict[str, Dict[str, float]]:
        """Get a comparison of all stores and their total costs."""
        merged_list = self.merge_supplies()
        comparison = {}
        
        for store in self.stores:
            total, unavailable = self.calculate_store_total(store, merged_list)
            comparison[store.name] = {
                'total': total if not unavailable else float('inf'),
                'unavailable_items': unavailable
            }
        
        return comparison


def demo():
    """Demo function to show how to use the Smart Shopping List."""
    
    # Create the smart shopping list system
    smart_list = SmartShoppingList()
    
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
    
    # Add offices to the system
    smart_list.add_office(office1)
    smart_list.add_office(office2)
    smart_list.add_office(office3)
    smart_list.add_office(office4)
    
    # Create stores with prices
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
    
    # Add stores to the system
    smart_list.add_store(store_a)
    smart_list.add_store(store_b)
    smart_list.add_store(store_c)
    
    # Display merged shopping list
    print("=" * 60)
    print("SMART SHOPPING LIST - CONSOLIDATED FROM 4 OFFICES")
    print("=" * 60)
    merged = smart_list.merge_supplies()
    print("\nMerged Shopping List:")
    for item, quantity in sorted(merged.items()):
        print(f"  - {item}: {quantity}")
    
    # Display price comparison
    print("\n" + "=" * 60)
    print("PRICE COMPARISON BY STORE")
    print("=" * 60)
    comparison = smart_list.get_price_comparison()
    for store_name, data in sorted(comparison.items()):
        print(f"\n{store_name}:")
        if data['unavailable_items']:
            print(f"  Status: Unavailable items - {', '.join(data['unavailable_items'])}")
        else:
            print(f"  Total Cost: ${data['total']:.2f}")
    
    # Find and display the cheapest store
    print("\n" + "=" * 60)
    print("CHEAPEST OPTION")
    print("=" * 60)
    cheapest_store, cheapest_total, _ = smart_list.find_cheapest_store()
    
    if cheapest_store:
        print(f"\nCheapest Store: {cheapest_store.name}")
        print(f"Total Cost: ${cheapest_total:.2f}")
        
        # Show itemized breakdown
        print("\nItemized Breakdown:")
        for item, quantity in sorted(merged.items()):
            price = cheapest_store.get_price(item)
            subtotal = price * quantity
            print(f"  - {item}: {quantity} x ${price:.2f} = ${subtotal:.2f}")
    else:
        print("\nNo store has all required items in stock.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
