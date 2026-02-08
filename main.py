from x_fast_trie import XFastTrie

def main():
    import sys

    print("=== X-Fast Trie Interactive Menu ===")
    trie = XFastTrie()

    menu = """
Choose an option:
1. Insert a value
2. Remove a value
3. Find predecessor
4. Find successor
5. Show all values
6. Show min and max
7. Search for a value
0. Exit
"""

    while True:
        print(menu)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            val = input("Enter value to insert: ").strip()
            try:
                trie.insert(int(val))
                print(f"Inserted {val}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            val = input("Enter value to remove: ").strip()
            try:
                trie.remove(int(val))
                print(f"Removed {val}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "3":
            val = input("Enter value to find predecessor for: ").strip()
            try:
                pred = trie.predecessor(int(val))
                print(f"Predecessor: {pred}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            val = input("Enter value to find successor for: ").strip()
            try:
                succ = trie.successor(int(val))
                print(f"Successor: {succ}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            print("Values in trie:", list(trie))

        elif choice == "6":
            print(f"Min: {trie._min.value if trie._min else None}")
            print(f"Max: {trie._max.value if trie._max else None}")

        elif choice == "7":
            val = input("Enter value to search for: ").strip()
            try:
                node = trie.search(int(val))
                if node:
                    print(f"Value {val} exists in the trie.")
                else:
                    print(f"Value {val} not found in the trie.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "0":
            print("Exiting...")
            sys.exit()

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()