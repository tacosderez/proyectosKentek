# Budget Tracker

expenses = []

def add_expense():
    name = input("Enter expense name: ")
    amount = float(input("Enter amount: "))
    expense = {"name": name, "amount": amount}
    expenses.append(expense)
    print("Expense added!\n")

def show_expenses():
    if not expenses:
        print("No expenses yet.")
        return
    print("\nYour expenses:")
    total = 0
    for expense in expenses:
        print(f"- {expense['name']}: ${expense['amount']:.2f}")
        total += expense["amount"]
    print(f"Total spent: ${total:.2f}\n")

def main():
    while True:
        print("1. Add expense")
        print("2. Show all expenses")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.\n")

main()
