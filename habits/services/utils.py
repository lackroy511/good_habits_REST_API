

def get_schedule(periodicity: str, time: str) -> str:
    
    hours = time.split(':')[0]
    minutes = time.split(':')[1]
    
    return f'{minutes} {hours} * * */{periodicity}'
