#!/usr/bin/env python3
"""
Unit tests for Smart Shopping List Application
"""

import unittest
from shopping_list import Office, Store, SmartShoppingList


class TestOffice(unittest.TestCase):
    """Test Office class functionality."""
    
    def test_add_single_item(self):
        office = Office("Test Office")
        office.add_item("Pens", 5)
        self.assertEqual(office.get_supplies()["Pens"], 5)
    
    def test_add_multiple_same_items(self):
        office = Office("Test Office")
        office.add_item("Pens", 5)
        office.add_item("Pens", 3)
        self.assertEqual(office.get_supplies()["Pens"], 8)
    
    def test_add_different_items(self):
        office = Office("Test Office")
        office.add_item("Pens", 5)
        office.add_item("Paper", 10)
        supplies = office.get_supplies()
        self.assertEqual(supplies["Pens"], 5)
        self.assertEqual(supplies["Paper"], 10)


class TestStore(unittest.TestCase):
    """Test Store class functionality."""
    
    def test_set_and_get_price(self):
        store = Store("Test Store")
        store.set_price("Pens", 1.50)
        self.assertEqual(store.get_price("Pens"), 1.50)
    
    def test_get_unavailable_item_price(self):
        store = Store("Test Store")
        self.assertEqual(store.get_price("NonexistentItem"), float('inf'))


class TestSmartShoppingList(unittest.TestCase):
    """Test SmartShoppingList functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.smart_list = SmartShoppingList()
        
        # Create offices
        self.office1 = Office("Office 1")
        self.office1.add_item("Pens", 10)
        self.office1.add_item("Paper", 5)
        
        self.office2 = Office("Office 2")
        self.office2.add_item("Pens", 5)
        self.office2.add_item("Folders", 10)
        
        # Create stores
        self.store1 = Store("Store A")
        self.store1.set_price("Pens", 1.00)
        self.store1.set_price("Paper", 5.00)
        self.store1.set_price("Folders", 0.50)
        
        self.store2 = Store("Store B")
        self.store2.set_price("Pens", 1.50)
        self.store2.set_price("Paper", 4.00)
        self.store2.set_price("Folders", 0.75)
    
    def test_merge_supplies_from_multiple_offices(self):
        self.smart_list.add_office(self.office1)
        self.smart_list.add_office(self.office2)
        
        merged = self.smart_list.merge_supplies()
        
        self.assertEqual(merged["Pens"], 15)  # 10 + 5
        self.assertEqual(merged["Paper"], 5)
        self.assertEqual(merged["Folders"], 10)
    
    def test_merge_supplies_empty_offices(self):
        merged = self.smart_list.merge_supplies()
        self.assertEqual(merged, {})
    
    def test_calculate_store_total(self):
        self.smart_list.add_office(self.office1)
        merged = self.smart_list.merge_supplies()
        
        total, unavailable = self.smart_list.calculate_store_total(self.store1, merged)
        
        # 10 pens * 1.00 + 5 paper * 5.00 = 35.00
        self.assertEqual(total, 35.00)
        self.assertEqual(unavailable, [])
    
    def test_calculate_store_total_with_unavailable_items(self):
        shopping_list = {"Pens": 10, "NonexistentItem": 5}
        
        total, unavailable = self.smart_list.calculate_store_total(self.store1, shopping_list)
        
        self.assertIn("NonexistentItem", unavailable)
    
    def test_find_cheapest_store(self):
        self.smart_list.add_office(self.office1)
        self.smart_list.add_office(self.office2)
        self.smart_list.add_store(self.store1)
        self.smart_list.add_store(self.store2)
        
        cheapest_store, total, merged = self.smart_list.find_cheapest_store()
        
        # Store A: 15 pens * 1.00 + 5 paper * 5.00 + 10 folders * 0.50 = 45.00
        # Store B: 15 pens * 1.50 + 5 paper * 4.00 + 10 folders * 0.75 = 50.00
        self.assertEqual(cheapest_store.name, "Store A")
        self.assertEqual(total, 45.00)
    
    def test_find_cheapest_store_no_stores(self):
        self.smart_list.add_office(self.office1)
        
        cheapest_store, total, merged = self.smart_list.find_cheapest_store()
        
        self.assertIsNone(cheapest_store)
        self.assertEqual(total, 0.0)
        self.assertEqual(len(merged), 2)  # Still returns the merged list
    
    def test_find_cheapest_store_no_supplies(self):
        self.smart_list.add_store(self.store1)
        
        cheapest_store, total, merged = self.smart_list.find_cheapest_store()
        
        self.assertIsNone(cheapest_store)
        self.assertEqual(total, 0.0)
        self.assertEqual(merged, {})
    
    def test_get_price_comparison(self):
        self.smart_list.add_office(self.office1)
        self.smart_list.add_store(self.store1)
        self.smart_list.add_store(self.store2)
        
        comparison = self.smart_list.get_price_comparison()
        
        self.assertIn("Store A", comparison)
        self.assertIn("Store B", comparison)
        self.assertEqual(comparison["Store A"]["total"], 35.00)
        self.assertEqual(comparison["Store B"]["total"], 35.00)
    
    def test_four_offices_integration(self):
        """Integration test with 4 offices as per requirements."""
        office1 = Office("Office 1")
        office1.add_item("Pens", 5)
        
        office2 = Office("Office 2")
        office2.add_item("Pens", 10)
        
        office3 = Office("Office 3")
        office3.add_item("Paper", 5)
        
        office4 = Office("Office 4")
        office4.add_item("Pens", 5)
        office4.add_item("Paper", 5)
        
        self.smart_list.add_office(office1)
        self.smart_list.add_office(office2)
        self.smart_list.add_office(office3)
        self.smart_list.add_office(office4)
        
        merged = self.smart_list.merge_supplies()
        
        self.assertEqual(merged["Pens"], 20)  # 5 + 10 + 5
        self.assertEqual(merged["Paper"], 10)  # 5 + 5


if __name__ == "__main__":
    unittest.main()
