import mysql.connector

cnx = mysql.connector.connect(host='localhost',
                              user='root',
                              password='9261953',
                              database="relay_tasks_manager", auth_plugin='mysql_native_password')

cur = cnx.cursor()


# Create the DATABASE

# cur.execute("""CREATE DATABASE RELAY_TASKS_MANAGER""")
# ____________________________________________________________________________________________
# CREATE TABLE father_task

# cur.execute("""CREATE TABLE father_task(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(40) NOT NULL,
#     description VARCHAR(1000) NOT NULL,
#     creator_id VARCHAR(100),
#     is_template BOOLEAN DEFAULT false,
#     creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     modify_time TIMESTAMP DEFAULT 0)""")
# ____________________________________________________________________________________________
# CREATE TABLE task

cur.execute("""CREATE TABLE task(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    type_id INT UNSIGNED,
    FOREIGN KEY (type_id) REFERENCES task_type(id),
    domain_id VARCHAR(100),
    father_id INT UNSIGNED,
    FOREIGN KEY (father_id) REFERENCES father_task(id),
    status_id INT UNSIGNED,
    FOREIGN KEY (status_id) REFERENCES status(id),
    urgency_id INT UNSIGNED,
    FOREIGN KEY (urgency_id) REFERENCES urgency(id),
    crew VARCHAR(1000) DEFAULT "[]",
    start DATETIME,
    end DATETIME,
    deadline DATETIME,
    files_url VARCHAR(3000) DEFAULT "[]",
    plannings VARCHAR(3000) DEFAULT "[]",
    equipment VARCHAR(3000) DEFAULT "[]",
    check_list VARCHAR(3000) DEFAULT "[]",
    creator_id VARCHAR(100),
    fault_data VARCHAR(2000),
    is_template BOOLEAN DEFAULT false,
    is_reschedule BOOLEAN DEFAULT false,
    creation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    modify_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)""")
# ____________________________________________________________________________________________
# CREATE TABLE status

# cur.execute("""CREATE TABLE status(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(30) NOT NULL,
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP
#  )""")

# INSERT VALUES TO STATUS

# cur.execute("""INSERT INTO status (name)
# VALUES('??????????')""")

# cur.execute("""INSERT INTO status (name)
# VALUES('????????????')""")

# cur.execute("""INSERT INTO status (name)
# VALUES('??????????')""")
# ____________________________________________________________________________________________
# CREATE TABLE urgency

# cur.execute("""CREATE TABLE urgency(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(30) NOT NULL,
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP
# )""")

# cur.execute("""INSERT INTO urgency (name)
# VALUES('????????')""")

# cur.execute("""INSERT INTO urgency (name)
# VALUES('????????')""")

# cur.execute("""INSERT INTO urgency (name)
# VALUES('??????????')""")

# ____________________________________________________________________________________________
# cur.execute("""CREATE TABLE task_type(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(30) NOT NULL,
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP
# )""")


# cur.execute("""INSERT INTO task_type (name)
# VALUES('?????????? ??????????')""")


# cur.execute("""INSERT INTO task_type (name)
# VALUES('?????????? ????????')""")

# cur.execute("""INSERT INTO task_type (name)
# VALUES('?????????? ???????? ????????????')""")

# cur.execute("""INSERT INTO task_type (name)
# VALUES('?????????? ?????????? ????????')""")

# cur.execute("""INSERT INTO task_type (name)
# VALUES('?????????? ?????????? ??????????')""")

# cur.execute("""INSERT INTO task_type (name)
# VALUES('?????????? ???? ????????????')""")

# cur.execute("""INSERT INTO task_type (name)
# VALUES('???????? ???? ???????? ????????????')""")

# cur.execute("""INSERT INTO task_type (name)
# VALUES('???????? ??????????????')""")
# ____________________________________________________________________________________________


# cnx.commit()
# cnx.close()
