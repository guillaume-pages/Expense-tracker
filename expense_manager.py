import json
from datetime import datetime

EXPENSES_FILE = 'expenses.json'

def load_expenses():
    try:
        with open(EXPENSES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open(EXPENSES_FILE, 'w') as file:
            json.dump([], file, indent=4)
        return []
    except json.JSONDecodeError:
        raise ValueError("Expenses file is corrupted. Please fix or delete it.")

def save_expenses(expenses):
    with open(EXPENSES_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

def get_next_id(expenses):
    if not expenses:
        return 1
    return max(expense['id'] for expense in expenses) + 1

def add_expense(description, amount):
    expenses = load_expenses()
    next_id = get_next_id(expenses)
    expense = {
        'id': next_id,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'description': description,
        'amount': amount
    }
    expenses.append(expense)
    save_expenses(expenses)
    return expense

def delete_expense(expense_id):
    expenses = load_expenses()
    try:
        expense_id = int(expense_id)
    except ValueError:
        return False

    expense = next((e for e in expenses if e['id'] == expense_id), None)
    if expense:
        expenses.remove(expense)
        save_expenses(expenses)
        return True
    return False

def list_expenses():
    expenses = load_expenses()
    return expenses

def get_summary(month=None):
    expenses = load_expenses()
    if month:
        expenses = [e for e in expenses if int(e['date'].split('-')[1]) == month]
    total = sum(e['amount'] for e in expenses)
    return total

def update_expense(expense_id, description, amount):
    expenses = load_expenses()
    try:
        expense_id = int(expense_id)
    except ValueError:
        return False

    expense = next((e for e in expenses if e['id'] == expense_id), None)
    if expense:
        expense['description'] = description
        expense['amount'] = amount
        save_expenses(expenses)
        return True
    return False

