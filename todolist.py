# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def display(rows):
    if rows == []:
        print("Nothing to do!")
    else:
        n = 0
        for row in rows:
            n += 1
            print(n,')', row.task, '. ', row.deadline.strftime('%d %b'), sep='')
    print('\n')

def add(Task):
    print("Enter task")
    new_task = input()
    print("Enter deadline")
    deadline = datetime.strptime(input(), '%Y-%m-%d')
    new_row = Task(task = new_task, deadline = deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added!")

def today_task(Task):
    today = datetime.today().date()
    rows = session.query(Task).filter(Task.deadline == today).all()
    print('Today',today.strftime('%d %b'))
    display(rows)

def weeks_task(Task):
    today = datetime.today().date()
    days = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    for i in range(7):
        date = today + timedelta(days=i)
        rows = session.query(Task).filter(Task.deadline == date).all()
        print(days[date.weekday()],date.strftime('%d %b'))
        display(rows)

def missed_tasks(Task):
    rows = session.query(Task).order_by(Task.deadline).filter(Task.deadline < datetime.today()).all()
    if rows:
        display(rows)
    else:
        print('Nothing is missed!')

def delete_task(Task):
    rows = session.query(Task).order_by(Task.deadline).all()
    if rows:
        print('Choose the number of the task you want to delete:')
        display(rows)
        print('0) Cancel')
        n = int(input())
        if n != 0:
            session.delete(rows[n-1])
            session.commit()
    else:
        print('Nothing to delete!')

while(True):
    print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')
    user_input = int(input())
    if user_input == 1:
        today_task(Task)
    elif user_input == 2:
        weeks_task(Task)
    elif user_input == 3:
        rows = session.query(Task).order_by(Task.deadline).all()
        display(rows)
    elif user_input == 4:
        missed_tasks(Task)
    elif user_input == 5:
        add(Task)
    elif user_input == 6:
        delete_task(Task)
    elif user_input == 0:
        print("Bye!")
        break
