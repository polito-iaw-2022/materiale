import sqlite3

if __name__ == '__main__':
    # 1. prepare the SQL query
    sql = 'SELECT * FROM todo'

    # 2. create the connection
    connection = sqlite3.connect('tasks.db')

    # 3. get a cursor
    cursor = connection.cursor()

    # 4. execute the query
    cursor.execute(sql)

    # 5. fetch the results (and print them)
    result = cursor.fetchall()
    print(result)

    # 6. close the cursor
    cursor.close()

    # another SQL query, for inserting elements
    sql_insert = 'INSERT INTO todo(description, urgent) VALUES (?, ?)'
    best_task = 'andare a casa'
    best_task_urgency = 1

    # get a new cursor
    cursor2 = connection.cursor()
    # execute the query
    cursor2.execute(sql_insert, (best_task, best_task_urgency))

    # commit changes
    connection.commit()

    # close the cursor
    cursor2.close()

    # 6a. finally, close the connection
    connection.close()