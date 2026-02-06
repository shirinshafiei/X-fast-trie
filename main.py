from x_fast_trie import XFastTrie


def main():
    print("--- X-Fast Trie Initialization ---")
    try:
        w = int(input("Enter bit-width (e.g., 8 for 0-255, 32 for larger): "))
    except ValueError:
        print("Invalid width. Defaulting to 8.")
        w = 8

    trie = XFastTrie(w)

    actions = {
        '1': "Insert",
        '2': "Delete",
        '3': "Search (Exists?)",
        '4': "Predecessor",
        '5': "Successor",
        '6': "Exit"
    }

    while True:
        print("\n" + "=" * 30)
        for k, v in actions.items():
            print(f"{k}. {v}")
        choice = input("Select an option: ")

        if choice == '1':
            val = int(input("Integer to insert: "))
            if trie.insert(val):
                print(f"Success: {val} inserted.")
            else:
                print(f"Failed: {val} is invalid or already exists.")

        elif choice == '2':
            val = int(input("Integer to delete: "))
            if trie.delete(val):
                print(f"Success: {val} deleted.")
            else:
                print(f"Failed: {val} not found.")

        elif choice == '3':
            val = int(input("Search for: "))
            print(f"Result: {'Found' if trie.exists(val) else 'Not Found'}")

        elif choice == '4':
            val = int(input("Predecessor of: "))
            print(f"Predecessor: {trie.predecessor(val)}")

        elif choice == '5':
            val = int(input("Successor of: "))
            print(f"Successor: {trie.successor(val)}")

        elif choice == '6':
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()