# Smart Shopping List

A smart shopping list application that easily lets you add supplies for multiple offices (designed for 4 offices), merges them together into one consolidated shopping list, and compares shopping prices from different stores to find the cheapest option.

## Features

- **Multi-Office Support**: Manage supplies for 4 (or more) different offices
- **Automatic Merging**: Consolidates supply lists from all offices into a single shopping list
- **Price Comparison**: Compare prices across multiple stores
- **Cost Optimization**: Automatically identifies the cheapest store for your complete shopping list
- **Detailed Breakdown**: Shows itemized costs and price comparisons

## Requirements

- Python 3.6 or higher
- No external dependencies (uses Python standard library only)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/valleedgar085-rgb/Smart-shopping-list.git
cd Smart-shopping-list
```

2. No additional installation needed - the application uses only Python standard library!

## Usage

### Interactive CLI (Recommended)

Run the interactive command-line interface:

```bash
python3 cli.py
```

The CLI provides an easy-to-use menu system where you can:
1. Add offices with their supplies
2. Add stores with their prices
3. View the merged shopping list and price comparison
4. Load sample data for demonstration

### Running the Demo

To see the application in action with sample data:

```bash
python3 shopping_list.py
```

This will demonstrate:
- 4 offices with different supply needs
- 3 stores with different prices
- Merged shopping list
- Price comparison across stores
- The cheapest store option

### Using as a Library

```python
from shopping_list import Office, Store, SmartShoppingList

# Create the smart shopping list system
smart_list = SmartShoppingList()

# Create offices and add supplies
office1 = Office("Office 1 - New York")
office1.add_item("Pens", 10)
office1.add_item("Paper Reams", 5)

office2 = Office("Office 2 - Boston")
office2.add_item("Pens", 15)
office2.add_item("Folders", 20)

# Add offices to the system
smart_list.add_office(office1)
smart_list.add_office(office2)

# Create stores with prices
store_a = Store("Office Depot")
store_a.set_price("Pens", 1.50)
store_a.set_price("Paper Reams", 8.00)
store_a.set_price("Folders", 0.50)

store_b = Store("Staples")
store_b.set_price("Pens", 1.25)
store_b.set_price("Paper Reams", 8.50)
store_b.set_price("Folders", 0.60)

# Add stores to the system
smart_list.add_store(store_a)
smart_list.add_store(store_b)

# Get merged shopping list
merged = smart_list.merge_supplies()
print("Merged Shopping List:", merged)

# Find the cheapest store
cheapest_store, total_cost, shopping_list = smart_list.find_cheapest_store()
print(f"Cheapest Store: {cheapest_store.name}")
print(f"Total Cost: ${total_cost:.2f}")

# Get price comparison for all stores
comparison = smart_list.get_price_comparison()
for store_name, data in comparison.items():
    print(f"{store_name}: ${data['total']:.2f}")
```

## Running Tests

Run the unit tests to verify the application:

```bash
python3 -m unittest test_shopping_list.py -v
```

All tests should pass, covering:
- Office supply management
- Store price management
- Supply merging from multiple offices
- Cost calculation and comparison
- Finding the cheapest option

## Architecture

The application consists of three main classes:

1. **Office**: Represents an office with its supply needs
   - Add items with quantities
   - Track supplies per office

2. **Store**: Represents a store with its prices
   - Set prices for items
   - Query prices for items

3. **SmartShoppingList**: Main controller class
   - Manages multiple offices and stores
   - Merges supplies from all offices
   - Calculates costs and finds the cheapest option
   - Provides price comparison across stores

## Example Output

```
============================================================
SMART SHOPPING LIST - CONSOLIDATED FROM 4 OFFICES
============================================================

Merged Shopping List:
  - Folders: 30
  - Markers: 20
  - Paper Reams: 15
  - Pens: 30
  - Staplers: 5

============================================================
PRICE COMPARISON BY STORE
============================================================

Amazon:
  Total Cost: $212.00

Office Depot:
  Total Cost: $245.00

Staples:
  Total Cost: $240.50

============================================================
CHEAPEST OPTION
============================================================

Cheapest Store: Amazon
Total Cost: $212.00

Itemized Breakdown:
  - Folders: 30 x $0.45 = $13.50
  - Markers: 20 x $1.80 = $36.00
  - Paper Reams: 15 x $7.50 = $112.50
  - Pens: 30 x $1.00 = $30.00
  - Staplers: 5 x $4.00 = $20.00
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
