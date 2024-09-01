
from collections import defaultdict

from src.models.api_models import ExpenseDetail
from src.models.schema_models import ExpenseBreakDown


def get_simplified_map_from_db_expense_list(expense_breakdown_list: list[ExpenseBreakDown]):
    
    simplified_map = defaultdict(int)
    for expense_breakdown in expense_breakdown_list:
        simplified_map[expense_breakdown.payer_id] += expense_breakdown.amount
        simplified_map[expense_breakdown.receiver_id] -= expense_breakdown.amount
        
    return simplified_map


def get_simplified_map_from_api_expense_list(expense_breakdown_list: list[ExpenseDetail]):
    
    simplified_map = defaultdict(int)
    for expense_breakdown in expense_breakdown_list:
        simplified_map[expense_breakdown.user_id] += expense_breakdown.amount
    
    return simplified_map


def get_transaction_tuples(simplified_map: dict):
    
    transaction_tuples = []
    for key1, val1 in simplified_map.items():
        total_positive_money = val1
        
        if total_positive_money > 0:
            for key2, val2 in simplified_map.items():
                if key1 == key2:
                    continue
                if val2 >= 0:
                    continue
                
                if (total_positive_money <= -1*val2) :
                    transaction = (key1, key2, total_positive_money)
                    simplified_map[key2] = total_positive_money + val2
                    transaction_tuples.append(transaction)
                    break
                else:
                    transaction = (key1, key2, -1*val2)
                    simplified_map[key2] = 0
                    total_positive_money += val2
                    transaction_tuples.append(transaction)
    
    return transaction_tuples