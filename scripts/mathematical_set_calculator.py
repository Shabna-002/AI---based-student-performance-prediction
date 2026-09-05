

def display_menu():
    print("===== MATHEMATICAL SET CALCULATOR =====")
    print("1. Union")
    print("2. Intersection")
    print("3. A - B")
    print("4. B - A")
    print("5. Symmetric Difference")
    print("6. Check Subset")
    print("7. Check Superset")
    print("8. Check Disjoint")
    print("9. Cardinality")
    print("10. Membership Check")
    print("0. Exit")


def read_set(name):
    values = input(f"Enter elements of Set {name}, separated by spaces: ")
    return set(values.split())


A = read_set("A")
B = read_set("B")

while True:
    display_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        print("A Union B =", A | B)

    elif choice == "2":
        print("A Intersection B =", A & B)

    elif choice == "3":
        print("A - B =", A - B)

    elif choice == "4":
        print("B - A =", B - A)

    elif choice == "5":
        print("A Symmetric Difference B =", A ^ B)

    elif choice == "6":
        print("A is subset of B:", A.issubset(B))
        print("B is subset of A:", B.issubset(A))

    elif choice == "7":
        print("A is superset of B:", A.issuperset(B))
        print("B is superset of A:", B.issuperset(A))

    elif choice == "8":
        print("A and B are disjoint:", A.isdisjoint(B))

    elif choice == "9":
        print("|A| =", len(A))
        print("|B| =", len(B))

    elif choice == "10":
        element = input("Enter element to search: ")
        print(f"{element} belongs to A:", element in A)
        print(f"{element} belongs to B:", element in B)

    elif choice == "0":
        print("Thank you!")
        break

    else:
        print("Invalid choice. Please try again.")