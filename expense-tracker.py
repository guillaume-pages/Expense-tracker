import argparse
from expense_manager import add_expense, delete_expense, list_expenses, get_summary, update_expense
from utils import validate_amount

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('--description', required=True, help='Description of the expense')
    add_parser.add_argument('--amount', type=float, required=True, help='Amount of the expense')

    delete_parser = subparsers.add_parser('delete', help='Delete an expense')
    delete_parser.add_argument('--id', type=int, required=True, help='ID of the expense to delete')

    subparsers.add_parser('list', help='List all expenses')

    summary_parser = subparsers.add_parser('summary', help='Show summary of expenses')
    summary_parser.add_argument('--month', type=int, help='Month for the summary (1-12)')

    update_parser = subparsers.add_parser('update', help='Update an existing expense')
    update_parser.add_argument('--id', type=int, required=True, help='ID of the expense to update')
    update_parser.add_argument('--description', required=True, help='New description of the expense')
    update_parser.add_argument('--amount', type=float, required=True, help='New amount of the expense')



    args = parser.parse_args()

    if args.command == 'add':
        try:
            validate_amount(args.amount)
            expense = add_expense(args.description, args.amount)
            print(f"Expense added successfully (ID: {expense['id']})")
        except ValueError as e:
            print(e)
    
    elif args.command == 'delete':
        if delete_expense(args.id):
            print("Expense deleted successfully")
        else:
            print("Expense not found")

    elif args.command == 'list':
        expenses = list_expenses()
        if expenses:
            print("ID  Date       Description  Amount")
            for expense in expenses:
                print(f"{expense['id']} {expense['date']} {expense['description']} ${expense['amount']}")
        else:
            print("No expenses found.")

    elif args.command == 'summary':
        total = get_summary(args.month) if args.month else get_summary()
        if args.month:
            print(f"Total expenses for month {args.month}: ${total}")
        else:
            print(f"Total expenses: ${total}")

    elif args.command == 'update':
        if update_expense(args.id, args.description, args.amount):
            print("Expense updated successfully")
        else:
            print("Expense not found")

if __name__ == '__main__':
    main()
