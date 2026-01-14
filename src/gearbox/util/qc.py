
def is_number(s: str):
    try:
        float(s)
        return True
    except ValueError:
        return False