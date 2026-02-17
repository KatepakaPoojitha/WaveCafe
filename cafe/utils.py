from datetime import datetime

def get_current_season():
    month = datetime.now().month
    
    if 3 <= month <= 6:
        return 'SUMMER', 'Summer Coolers', 'June'
    elif 7 <= month <= 10:
        return 'MONSOON', 'Monsoon Snacks', 'October'
    else:
        return 'WINTER', 'Winter Warmers', 'February'
