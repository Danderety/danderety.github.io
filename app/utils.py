from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None


def filter_tickets(tickets, room=None, status=None, date_from=None, date_to=None):
    if room:
        tickets = [t for t in tickets if t.room == room]
    if status:
        tickets = [t for t in tickets if t.status == status]
    if date_from:
        tickets = [t for t in tickets if t.timestamp.date() >= date_from]
    if date_to:
        tickets = [t for t in tickets if t.timestamp.date() <= date_to]
    return tickets
