#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

print('_'*100)
pa = input('\nEnter Password of your SQL server : ')
print()
print('_'*100)

import mysql.connector as sqltor
mycon = sqltor.connect(host='localhost',user='root',password=f'{pa}')
cursor = mycon.cursor()

#---------------------------------------------------------------------------------------------------------------------------------------------------

cursor.execute('create database if not exists student')
print('_'*100)
print("\nDatabase 'Student' created successfully !!\n")

mycon = sqltor.connect(host='localhost',user='root',password=f'{pa}',database='student')
cursor = mycon.cursor()

#---------------------------------------------------------------------------------------------------------------------------------------------------

cursor.execute(''' 
create table if not exists tasks 
(
task_id int primary key auto_increment,
title varchar(75) not null,
subject varchar(25) not null,
due_date date not null,
status varchar(25) default 'Not_Done'
)
''')

cursor.execute('''
create table if not exists expense 
(
ex_id int primary key auto_increment,
date date not null,
amount float not null,                 
category varchar(45) not null,              
description text
)               
''')

cursor.execute('''
create table if not exists notes 
(
event_id int primary key auto_increment,
title varchar(75) not null,
subject varchar(25) not null,                               
content text
)               
''')

cursor.execute('''
create table if not exists events 
(
event_id int primary key auto_increment,
title varchar(75) not null,
event_date date not null              
)               
''')

print('Tables Created : \n1. Tasks \n2. Expense \n3. Events \n')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ++++++++++ MAIN MENU ++++++++++
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main_menu() :

    while True :
        print('_'*100)
        print('\n----------  Student Utility Manager  ----------')
        print('1. Task Manager')
        print('2. Notes Archive')
        print('3. Expenses Tracker')
        print('4. Events Planner')
        print('5. Insight Centre')
        print('6. Exit')
        print('-----------------------------------------------\n')

        ui = int(input('Enter your choice (1,2,3,4,5,6) : '))

        if ui in [1,2,3,4,5,6] :
                if ui == 1 :
                    task_manager()
                if ui == 2 :
                    notes_archive()
                if ui == 3:
                    expenses_tracker()
                if ui == 4 :
                    event_planner()
                if ui == 5 :
                    insight_centre()
                if ui == 6 :
                    print('\nExiting ...')                    
                    break
        elif ui not in [1,2,3,4,5,6] :
            print('\nNot a Valid Option !!\n')





#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ++++++++++ TASK MANAGER ++++++++++
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
def Add_task():
    print("\nYou choose 'Add New Task'\n")

    ui11 = int(input('How many tasks do you want to add ? '))

    for i1 in range(ui11):
        print('\nTask No.',i1+1)
        title = input('Enter title of the task : ')

        cursor.execute(f"select * from tasks where title = '{title}'")
        data = cursor.fetchall()

        if len(data) > 0 :
            print(f"Task '{title}' already exists")
        else :
            subj = input('Enter subject of the task : ')
            dud = str(input('Enter due date for the task (YYYY-MM-DD): '))
            cursor.execute( f"insert into tasks (title,subject,due_date) values ('{title}','{subj}','{dud}') " )
            mycon.commit()
            print("\nTask Added Successfully !!")
    print()

def Mark_task():
    print("You chose 'Mark Task as Done'\n")

    cursor.execute("select title from tasks where status = 'Not_Done'")
    data = cursor.fetchall()

    nu1 = 1
    for row in data :
        print(nu1,row[0])
        nu1 += 1

    ttl = input('\nEnter Title of the task to mark as done : ')

    cursor.execute(f"select * from tasks where title = '{ttl}' ")
    data1 = cursor.fetchall()

    if len(data1) > 0 :
        cursor.execute(f"update tasks set status = 'Done' where title = '{ttl}' ")
        mycon.commit()
        print(f"Task '{ttl}' marked as Done")
    else :
        print('Task',ttl,'doesn\'t exists')

def Delete_task():
    print("You choose 'Delete a Task'\n")

    cursor.execute('select title from tasks')
    data = cursor.fetchall()

    nu1 = 1
    for row in data :
        print(nu1,row[0])
        nu1 += 1

    ttl = input('\nEnter Title of the task to be deleted : ')

    cursor.execute(f"select * from tasks where title = '{ttl}' ")
    data2 = cursor.fetchall()

    if len(data2) > 0 :
        cursor.execute(f"delete from tasks where title = '{ttl}' ")
        mycon.commit()
        print(f"Task '{ttl}' Deleted")
    else :
        print('Task',ttl,'doesn\'t exists')

def view_all_tasks():
    print("\nYou chose 'View All Tasks'\n")
    cursor.execute('select * from tasks')
    data = cursor.fetchall()
    for row in data :
        print('ID -',row[0],'  ||  Title -',row[1],'  ||  Subject -',row[2],'  ||  Due Date -',row[3],'  ||  Status -',row[4])  

def viewTaskBySubject():
    print("\nYou chose 'View Tasks by Subject'\n")
    cursor.execute(f"select subject from tasks ")
    data1 = cursor.fetchall()

    i=1
    for row in data1 :
        print(i,row[0])
        i+=1

    subj = input("\nWhich subject's tasks do you want to view ? ")

    cursor.execute(f"select * from tasks where subject = '{subj}'")
    data = cursor.fetchall()

    if len(data) > 0:
        print()
        view_tasks()
    else :
        print('Task subject',subj,'doesn\'t exists')

def viewPendingTasks():
    print("\nYou chose 'View Pending Tasks'\n")
    cursor.execute("select * from tasks where status = 'Not_Done'")
    data = cursor.fetchall()

def viewTaskStats():
    print("\nYou chose 'View Task Statistics'\n")

    cursor.execute("select title,status,due_date from tasks where status = 'Not_Done' order by due_date ")
    data = cursor.fetchall()

    from datetime import datetime

    for row in data :
        today = datetime.today().date()
        du_dt = row[2]
        rm_dt = (du_dt - today).days

        if rm_dt > 0 :
            print('Title -',row[0],'  ||  Status -',row[1],'  ||  Days Remaining -',rm_dt)
        elif rm_dt < 0 :
            print('Title -',row[0],'  ||  Status -',row[1],'  ||  Task Overdue')
        elif rm_dt == 0 :
            print('Title -',row[0],'  ||  Status -',row[1],'  ||  Due Today')

    cursor.execute("select title,status from tasks where status = 'Done' order by due_date ")
    data = cursor.fetchall()

    for row1 in data :
        print('Title -',row1[0],'  ||  Status -',row1[1],)

def task_viewer():
    while True : 
        print('\n----------  Task Viewer  ----------')
        print('1. View All Tasks')
        print('2. View Tasks by Subject')
        print('3. View Pending Tasks')
        print('4. View Task Statistics')
        print('5. Back to Task Manager Menu')
        print('-----------------------------------\n')

        ui12 = input('Enter your choice (1,2,3,4,5) : ')
        if ui12.isdigit() :
            ui12 = int(ui12)
            if ui12 in [1,2,3,4,5,6] :
                print('\n-----------------------------------\n')
                print('_'*100)

                if ui12 == 1 :                        
                    view_all_tasks()

                if ui12 == 2 :
                    viewTaskBySubject()
                if ui12 == 3 :
                    viewPendingTasks()
                if ui12 == 4 :
                    viewTaskStats()

                if ui12 == 5 :
                    print('\nExiting ...')
                    print()
                    break
            else:
                   print('\nEnter a Valid Option !!')
        else:
            print('\nEnter a Valid Option !!')

def task_manager() :
    while True :
        print('_'*100)
        print('\n----------  Task Manager  ----------')
        print('1. Add a New Task')
        print('2. View Tasks')
        print('3. Mark a Task as Done')
        print('4. Delete a Task')
        print('5. Back to Main Menu')
        print('------------------------------------\n')

        ui1 = input('Enter your choice (1,2,3,4,5) : ')
        print('\n------------------------------------\n')
        print('_'*100)
        if ui1.isdigit() :
            ui1 = int(ui1)
            if ui1 in [1,2,3,4,5] :
                if ui1 == 1 :            
                    Add_task()
                
                if ui1 in [2,3,4] :
                    cursor.execute('select * from tasks')
                    data3 = cursor.fetchall()
                    if len(data3) > 0 :

                        if ui1 == 2:
                            task_viewer()
                        if ui1 == 3 :
                            Mark_task()
                        if ui1 == 4 :
                            Delete_task()
                if ui1 == 5 :
                    print('\nExiting ...')
                    print()
                    break
            else:
                 print('\nEnter a Valid menu Option------------------- !!\n')
        else:

            print('\nEnter an Valid menu Option------------------- !!\n')





#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ++++++++++ NOTES ARCHIVE ++++++++++
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def addNote():
    print("\nYou chose 'Add a Note'\n")
    print('-------------------------------------\n')

    ttl = input('Enter Title of note : ')

    cursor.execute(f"select title from notes where title = '{ttl}'")
    data = cursor.fetchall()

    if len(data) > 0 :
        print(f"Note '{ttl}' already exists")

    else :
        sub = input('Enter Subject of note : ')

        print()
        print('_'*100)
        print("\nEnter Content for note (Type 'END' in a new line when you're done) : \n")

        txt = []
        while True :
            line = input()
            if line.strip().upper() == "END" :
                break
            txt.append(line)

        f_text = '\n'.join(txt)
        cursor.execute(f"insert into notes (title,subject,content) values('{ttl}','{sub}','{f_text}')")
        mycon.commit()

        print()
        print('_'*100)
        print('\nNote Added Successfully !!')

def viewNotes():
    cursor.execute('select * from notes')
    data1 = cursor.fetchall()
    print("\nYou chose 'View Notes'\n")
    print('-------------------------------------\n')

    cursor.execute('select title from notes')
    data2 = cursor.fetchall()

    ni1 = 1
    for row1 in data2 :
        print(ni1,row1[0])
        ni1 += 1 

    print('\n-------------------------------------\n')
    ui72 = input("\nEnter title of notes to view : ")

    cursor.execute(f"select * from notes where title = '{ui72}'")
    data4 = cursor.fetchall()

    if len(data4) > 0 :
        cursor.execute(f"select content from notes where title = '{ui72}'")
        data = cursor.fetchall()

        print()
        for row in data :
            print(row[0])
    else :
        print(f"No note of title '{ui72}' exists")

def editNotes():
    cursor.execute('select * from notes')
    data1 = cursor.fetchall()
    print("\nYou chose 'Edit a Note'\n")
    print('-------------------------------------\n')

    cursor.execute('select title from notes')
    data2 = cursor.fetchall()

    ni1 = 1
    for row1 in data2 :
        print(ni1,row1[0])
        ni1 += 1 

    print('\n-------------------------------------\n')
    ui73 = input("\nEnter title of notes to edit : ")

    cursor.execute(f"select * from notes where title = '{ui73}'")
    data4 = cursor.fetchall()

    if len(data4) > 0 :
        cursor.execute(f"select content from notes where title = '{ui73}'")
        data = cursor.fetchall()

        print()
        print('_'*100)
        print('\nCurrent Note : \n')
        for row in data :
            print(row[0])

        print('\n-------------------------------------\n')
        print("Enter New Note (Type 'END' in a new line when you're done): \n")
        txt1 = []
        while True :
            line1 = input()
            if line1.strip().upper() == "END" :
                break
            txt1.append(line1)

        f_text1 = '\n'.join(txt1)
        cursor.execute(f"update notes set content = '{f_text1}' where title = '{ui73}'")
        mycon.commit()

        print('\nNote Updated Successfully !!')

    else :
        print(f"No note of title '{ui73}' exists")

def deleteNotes():
    print("\nYou chose 'Delete a Note'\n")
    print('-------------------------------------\n')

    cursor.execute('select title from notes')
    data2 = cursor.fetchall()

    ni1 = 1
    for row1 in data2 :
        print(ni1,row1[0])
        ni1 += 1 

    print('\n-------------------------------------\n')
    ui74 = input("\nEnter title of notes to delete : ")

    cursor.execute(f"select * from notes where title = '{ui74}'")
    data4 = cursor.fetchall()

    if len(data4) > 0 :
        cursor.execute(f"delete from notes where title = '{ui74}'")
        mycon.commit()

        print('Note Deleted Successfully !!')
    else :
        print(f"No note of title '{ui74}' exists")

def notes_archive() :
    while True:
        print('_'*100)
        print('\n----------  Notes Archive  ----------')
        print('1. Add a Note')
        print('2. View Notes')
        print('3. Edit a Note')
        print('4. Delete a Note')
        print('5. Back to Main Menu')
        print('-------------------------------------\n')

        ui7 = input('Enter your choice (1,2,3,4,5) : ')
        if ui7.isdigit() :
            ui7 = int(ui7)
            print('\n-------------------------------------\n')
            print('_'*100)

            if ui7 in [1,2,3,4,5] :
                if ui7 == 1 :
                    addNote()
                if ui7 == 2 :
                    viewNotes()
                if ui7 == 3 :
                    editNotes()
                if ui7 == 4 :
                    deleteNotes()
                if ui7 == 5 :
                    break
            else :
                print('\nNo Notes Added !!')
        else:
            print('\nEnter a Valid Option !!')





#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ++++++++++ EXPENSE TRACKER ++++++++++
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def addAnExpense():
    print("\nYou chose 'Add an Expense'\n")
    date1 = input('Enter Date (YYYY-MM-DD) : ')
    amt = float(input('Enter Amount : '))
    cat = input('Enter Category : ')
    des = input('Enter Description : ')

    cursor.execute(f"insert into expense (date,amount,category,description) values('{date1}','{amt}','{cat}','{des}')")
    mycon.commit()

    print('\nExpense Added Successfully !!')

def viewAllExpense():
    print("\nYou chose 'View All Expenses'\n")
    cursor.execute('select * from expense')
    data = cursor.fetchall()
    for row in data :
        print('ID -',row[0],'  ||  Date -',row[1],'  ||  Amount -',row[2],'  ||  Category -',row[3],'  ||  Description -',row[4])

def viewExpensebyCategory():
    print("\nYou chose 'View Expenses by Category'\n")
    cursor.execute('select distinct category from expense')
    data = cursor.fetchall()
    n21 = 1
    for row in data :
        print(n21,row[0])
        n21 += 1
    cat1 = input('\nEnter Category of Expense : ')
    cursor.execute(f"select * from expense where category = '{cat1}'")
    data12 = cursor.fetchall()

    if len(data12) > 0:
        cursor.execute(f"select * from expense where category = '{cat1}'")
        data1 = cursor.fetchall()
        for row1 in data1 :
            print('ID -',row1[0],'  ||  Date -',row1[1],'  ||  Amount -',row1[2],'  ||  Category -',row1[3],'  ||  Description -',row1[4])
    else :
        print('No Expense of',cat1,'exists')

def OverAllTotalExpenses():
    print("\nYou chose 'Total Expense'")
    cursor.execute('select sum(amount) from expense')
    data = cursor.fetchall()

    for row in data :
        print('Total Expense : ',row[0])
    
def expenses7Days():
    print("\nYou chose 'Total Expense per last 7 days'")
    cursor.execute('select sum(amount) from expense where date >= curdate() - interval 7 day')
    data = cursor.fetchall()

    for row in data :
        print('Total Expense in last 7 days : ',row[0])

def expenses30Days():
    print("\nYou chose 'Total Expense per last 30 days'")
    cursor.execute('select sum(amount) from expense where date >= curdate() - interval 30 day')
    data = cursor.fetchall()

    for row in data :
        print('Total Expense in last 30 days : ',row[0])

def expenseViewer():
    cursor.execute('select * from expense')
    data3 = cursor.fetchall()
    if len(data3) > 0 :
        while True:
            print('\n----------  View Expenses  ----------')
            print('1. View All Expenses')
            print('2. View Expenses by category')
            print('3. Back to Expense Tracker Menu')
            print('-------------------------------------\n')

            ui21 = input('Enter your choice (1,2,3) : ')

            if ui21.isdigit() :
                ui21 = int(ui21)
                if ui21 in [1,2,3] :
                    print('\n-------------------------------------\n')
                    print('_'*100)

                    if ui21 == 1 :
                        viewAllExpense()

                    if ui21 == 2 :
                        viewExpensebyCategory()

                    if ui21 == 3 :
                        break
                else:
                    print('\nEnter a Valid Option')
            else:
                print('\nEnter a Valid Option')    
    else:
        print('\nNo Expense Added !!')

def totalExpenses():
    while True:
        print("\n----------  Total Expense  ----------")
        print('1. Total Expense per last 7 days')
        print('2. Total Expense per last 30 days')
        print('3. Total All Expense')
        print('4. Back to Expense Tracker Menu')
        print('-------------------------------------\n')

        ui22  = input('Enter your choice (1,2,3,4) : ')

        if ui22.isdigit() :
            ui22 = int(ui22)
            if ui22 in [1,2,3,4] :
                print('\n-------------------------------------\n')
                print('_'*100)
                if ui22 == 1 :
                    expenses7Days()
                if ui22 == 2 :
                    expenses30Days()
                if ui22 == 3 :
                    OverAllTotalExpenses()
                if ui22 == 4 :
                    break
            else:
                print('\nEnter a Valid Option !!')
        else:
            print('\nEnter a Valid Option !!')

def expenses_tracker():
    while True:
        print('_'*100)
        print('\n----------  Expenses Tracker  ----------')
        print('1. Add an Expense')
        print('2. View Expenses')
        print('3. Total Expense')
        print('4. Back to Main Menu')
        print('----------------------------------------\n')

        ui2 = input('Enter your choice (1,2,3,4) : ')
        if ui2.isdigit() :
            ui2 = int(ui2)
            print('\n-------------------------------------\n')
            print('_'*100)
            if ui2 in [1,2,3,4] :
                if ui2 == 1 :
                    addAnExpense()
                if ui2 == 2 :
                    expenseViewer()
                if ui2 == 3 :
                    totalExpenses()
                if ui2 == 4 :
                    break
            else:
                print('\nEnter a Valid Option !!')
        else:
            print('\nEnter a Valid Option !!')





#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ++++++++++ EVENT PLANNER ++++++++++
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def addEvent():
    print("\nYou chose 'Add an Event'\n")

    titl = input('Enter Title of Event : ')

    cursor.execute(f"select * from events where title = '{titl}'")
    data = cursor.fetchall()

    if len(data) > 0 :
        print(f"Event '{titl}' already exists")

    else :
        dt = input('Enter Date (YYYY-MM-DD) : ')

        cursor.execute(f"insert into events (title,event_date) values ('{titl}','{dt}')")
        mycon.commit()

        print(f"\nEvent '{titl}' Added Successfully !!")

def viewEvent():
    print("\nYou chose 'View Events'\n")
    cursor.execute('select title,event_date from events')
    data = cursor.fetchall()

    from datetime import datetime

    for row in data :
        today = datetime.today().date()
        du_dt = row[1]
        rm_dt = (du_dt - today).days
        
        if rm_dt > 0 :
            print('Title -',row[0],'  ||  Date -',row[1],'  ||  Days Remaining -',rm_dt)
        elif rm_dt < 0 :
            print('Title -',row[0],'  ||  Date -',row[1],"  ||  Event's Over")
        elif rm_dt == 0 :
            print('Title -',row[0],'  ||  Date -',row[1],"  ||  Event's Today")  

def cancelEvent():
    print("\nYou chose 'Cancel an Event'\n")
    cursor.execute('select title from events')
    data2 = cursor.fetchall()

    nu1 = 1
    for row in data2 :
        print(nu1,row[0])
        nu1 += 1 

    til1 = input('\nEnter Title of Event to cancel : ')

    cursor.execute(f"select title from events where title = '{til1}' ")
    data2 = cursor.fetchall()

    if len(data2) > 0 :      
        cursor.execute(f"delete from events where title = '{til1}'")
        mycon.commit()
        print(f"\nEvent '{til1}' Canceled Successfully")
    else :
        print('No Event of title',til1,'exists')
    
def rescheduleEvent():
    print("\nYou chose 'Reschedule an Event'\n")
    cursor.execute('select title from events')
    data2 = cursor.fetchall()

    nu1 = 1
    for row in data2 :
        print(nu1,row[0])
        nu1 += 1 

    til1 = input('\nEnter Title of Event to reschedule : ')

    cursor.execute(f"select title from events where title = '{til1}' ")
    data2 = cursor.fetchall()

    if len(data2) > 0 :
        dt1 = input('Enter the final date (YYYY-MM-DD) : ')
        cursor.execute(f"update events set event_date = '{dt1}' where title = '{til1}'")
        mycon.commit()
        print(f"\nEvent '{til1}' Rescheduled Successfully")
    else :
        print('No Event of title',til1,'exists')

def event_planner():
    while True:
        print('_'*100)
        print('\n----------  Events Planner  ----------')
        print('1. Add an Event')
        print('2. View Events')
        print('3. Reschedule an Event')
        print('4. Cancel an Event')
        print('5. Back to Main Menu')
        print('--------------------------------------\n')

        ui3 = input('Enter your choice (1,2,3,4,5) : ')

        if ui3.isdigit() :
            ui3 = int(ui3)
            if ui3 in [1,2,3,4,5] :
                print('\n--------------------------------------\n')
                print('_'*100)
                if ui3 == 1 :
                    addEvent()
                if ui3 == 2 :
                    viewEvent()
                if ui3 == 3 :
                    rescheduleEvent()
                if ui3 == 4 :
                    cancelEvent()
                if ui3 == 5 :
                    break
            else:
                print('Enter a Valid Option')
        else:
            print('Enter a Valid Option')





#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ++++++++++ INSIGHT PLANNER ++++++++++
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def motivateMe():
    l_mo_me = ["Discipline beats motivation — show up daily, even when it's hard.","Growth starts where your comfort zone ends.","Don't aim for success; aim to be valuable — success will follow.",
                "Every expert was once a beginner who didn't quit.","Failing is part of learning; staying down is not.","Small consistent steps are more powerful than occasional sprints.",
                "Time will pass anyway. Make it count."]
  
    import random
    n1 = random.randint(0,len(l_mo_me)-1)
    print(l_mo_me[n1])

def didYouKnow():
    l_dyk_f = ["The first computer virus, called Creeper, was created in 1971 — not to harm, but just to display a message : I am the creeper, catch me if you can!",
                "The term 'bug' in programming comes from a real moth found in a Harvard computer in 1947, which caused it to malfunction.",
                "Python was named after the British comedy group Monty Python, not the snake. That's why many tutorials use jokes and references in examples.",
                "Over 90 precent of the world's currency exists only on computers — it's digital, not physical cash.",
                "Linux powers more than 70 percent of the world's servers, including those used by Google, Facebook, and even the International Space Station."]
 
    import random
    n1 = random.randint(0,len(l_dyk_f)-1)
    print(l_dyk_f[n1])

def quoteOfDay():
    l_quo_d = ["Success is not in never failing, but in rising every time you fall.","Don't watch the clock; do what it does — keep going.","The future belongs to those who prepare for it today.",
                "Simplicity is the soul of efficiency.","Hard work beats talent when talent doesn't work hard.","Don't lower your standards. Increase your effort.",
                "It always seems impossible until it's done."]

    import random
    n1 = random.randint(0,len(l_quo_d)-1)
    print(l_quo_d[n1])

def insight_centre():
    while True:
        print('_'*100)
        print('\n----------  Insight Centre  ----------')
        print('1. Motivate Me')
        print('2. Did You Know !?')
        print('3. Quote of the Day')
        print('4. Back')
        print('--------------------------------------\n')

        ui4 = input('Enter your choice (1,2,3,4) : ')
        if ui4.isdigit() :
            ui4 = int(ui4)
            if ui4 in [1,2,3,4] :
                print('\n--------------------------------------\n')
                if ui4 == 1 :
                    motivateMe()
                if ui4 == 2 :
                    didYouKnow()
                if ui4 == 3 :
                    quoteOfDay()
                if ui4 == 4 :
                    break
            else:
                print('Enter a Valid Option !!')
        else:
            print('Enter a Valid Option !!')





#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ++++++++++ OUTRO ++++++++++
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

main_menu()

print()
print('_'*100)
print()
print('THANK YOU \nGOOD BYE')
print()
print('_'*100)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#cursor.execute('drop database student')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------