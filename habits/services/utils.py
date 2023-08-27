

from habits.models import Habit
from telegram_conn.services.tg_api import TelegramAPI


def get_schedule(periodicity: str, time: str) -> str:
    
    hours = time.split(':')[0]
    minutes = time.split(':')[1]
    
    return f'{minutes} {hours} * * */{periodicity}'


# def send_success_created_message(habit: Habit) -> None:
    
#     text = f'''
#     Вы создали привычку:\n{habit.deed} в {str(habit.time)} {habit.place}
#     '''
#     TelegramAPI.send_message(text, habit.user.tg_chat_id)
