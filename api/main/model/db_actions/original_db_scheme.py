import datetime
import mysql.connector

cnx = mysql.connector.connect(host='localhost',
                              user='root',
                              password='9261953',
                              database="relay_tasks_manager", auth_plugin='mysql_native_password')

cur = cnx.cursor()
# cur.execute("""CREATE DATABASE RELAY_TASKS_MANAGER""")


# cur.execute("""CREATE TABLE father_task(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(30) NOT NULL,
#     description VARCHAR(300) NOT NULL,
#     domain_id INT UNSIGNED,
#     FOREIGN KEY (domain_id) REFERENCES domain(id),
#     urgency ENUM ('רגיל',
#     'דחוף',
#     'דחוף במיוחד') DEFAULT 'רגיל',
#     deadline DATETIME,
#     added_files VARCHAR(100),
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
#     modify_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# # )""")


# cur.execute("""CREATE TABLE task(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(30) NOT NULL,
#     description VARCHAR(300) NOT NULL,
#     type_id INT UNSIGNED,
#     FOREIGN KEY (type_id) REFERENCES task_type(id),
#     domain_id INT UNSIGNED,
#     FOREIGN KEY (domain_id) REFERENCES domain(id),
#     father_id INT UNSIGNED,
#     FOREIGN KEY (father_id) REFERENCES father_task(id),
#     crew VARCHAR(300),
#     start DATETIME,
#     end DATETIME,
#     allDay BOOLEAN,
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
#     modify_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# )""")


# cur.execute("""INSERT INTO father_task ( title,description,domain_id) VALUES('תחנת שנאים גני תקווה',
# 'הקמת תחנה חדשה בתקן יורו 2 בהספק 200 מגה ואט'
# ,4)""")

# cur.execute("""INSERT INTO father_task ( title,description,domain_id) VALUES('עבודות תחזוקה אתר ירקון מזרח',
# 'בדיקת עשור - כולל הכפלת שנאי תת קרקעי'
# ,3)""")


# cur.execute("""INSERT INTO task ( title,description,type_id,domain_id,father_id,crew) VALUES('X עבודה ',
# 'ציוד דרוש YAMAHAR 40T X 2', 1,1,1,
# '["אבי כהן" ,"דן שלום"]'
# )""")


# cur.execute("""INSERT INTO task ( title,description,type_id,domain_id,father_id,crew) VALUES('הנחת תשתית צנרת',
# 'ציוד דרוש VOLVO XT500', 2,2,1,
# '["רון כהן" ,"יותם ירון"]'
# )""")


# cur.execute("""INSERT INTO task ( title,description,type_id,domain_id,father_id,crew) VALUES('פריסת כבלים',
# 'ציוד דרוש MACKITA 443', 3,3,1,
# '["שלו דהן" ,"ירון מנשה"]'
# )""")


# cur.execute("""INSERT INTO task ( title,description,type_id,domain_id,father_id,crew) VALUES('חיוות שנאי',
# 'לעבוד על פי מפרט קבלן כפי שפורט',
# 4,4,1,
# '["שמחה מישייב"]')""")


# cur.execute("""INSERT INTO task ( title,description,type_id,domain_id,father_id,crew) VALUES('סידור האתר לקראת מסירה',
# 'לשים לב שמפסל לא חורג מ3 מעלות',
# 5,5,1,'["עוז רוזן", "שלום אברגיל"]')""")

# cur.execute("""INSERT INTO task ( title,description,type_id,domain_id,father_id,crew) VALUES('הוצאת שנאי תת קרקעי ירקון מזרח',
# 'ציוד דרוש YAMAHAR 40T X 2', 1,1,2,'["אבי כהן", "דן שלום"]')""")


# cur.execute("""INSERT INTO task ( title,description,type_id,domain_id,father_id,crew) VALUES('הכפלת שנאי ירקון מזרח',
# 'ציוד דרוש VOLVO XT500', 2,2,2,
# '["ליאור גורן", "רון שלום"]')""")


# cur.execute("""INSERT INTO task ( title,description,type_id,domain_id,father_id,crew) VALUES('פריסת כבלים',
# 'ציוד דרוש MACKITA 443', 3,3,2,'["אור שבתאי"]')""")


# cur.execute("""INSERT INTO task ( title,description,type_id,domain_id,father_id,crew) VALUES('בדיקה כוללת ירקון מזרח',
# 'לעבוד על פי מפרט קבלן כפי שפורט',
# 4,4,2,
# '["שמחה מישייב"]')""")


# cur.execute("""INSERT INTO task ( title,description,type_id,domain_id,father_id,crew) VALUES( 'ציפוי לכלל המתקן ירקון מזרח',
# 'לשים לב שמפסל לא חורג מ3 מעלות',
# 5,5,1,'["עוז רוזן", "שלום אברגיל"]')""")

# --------------------------------------------------------------------------------------------


# cur.execute("""CREATE TABLE father_task(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(40) NOT NULL,
#     description VARCHAR(1000) NOT NULL,
#     creator_id VARCHAR(100),
#     is_template BOOLEAN DEFAULT false,
#     creation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
#     modify_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)""")

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


# cur.execute("""CREATE TABLE status(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(30) NOT NULL,
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP
#  )""")

# cur.execute("""INSERT INTO status (name)
# VALUES('ממתין')""")

# cur.execute("""INSERT INTO status (name)
# VALUES('בביצוע')""")

# cur.execute("""INSERT INTO status (name)
# VALUES('הושלם')""")


# cur.execute("""CREATE TABLE urgency(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(30) NOT NULL,
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP
# )""")

# cur.execute("""INSERT INTO urgency (name)
# VALUES('נמוך')""")

# cur.execute("""INSERT INTO urgency (name)
# VALUES('רגיל')""")

# cur.execute("""INSERT INTO urgency (name)
# VALUES('גבוהה')""")


# cur.execute("""CREATE TABLE domain(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(30) NOT NULL,
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP
# )""")

# cur.execute("""INSERT INTO domain (name)
# VALUES('צוות עבודות עפר')""")

# cur.execute("""INSERT INTO domain (name)
# VALUES('צוות תשתיות')""")
# cur.execute("""INSERT INTO domain (name)
# VALUES('צוות סיבים')""")
# cur.execute("""INSERT INTO domain (name)
# VALUES('צוות התמעה')""")
# cur.execute("""INSERT INTO domain (name)
# VALUES('צוות עבודות גמר')""")

# cur.execute("""CREATE TABLE task_type(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(30) NOT NULL,
#     create_time DATETIME DEFAULT CURRENT_TIMESTAMP
# )""")


# cur.execute("""INSERT INTO task_type (name)
# VALUES('משימה כללית')""")


# cur.execute("""INSERT INTO task_type (name)
# VALUES('תיקון תקלה')""")

# cur.execute("""INSERT INTO task_type (name)
# VALUES('לחפור הכנה לתשתית')""")

# cur.execute("""INSERT INTO task_type (name)
# VALUES('להניח תשתית צנרת')""")

# cur.execute("""INSERT INTO task_type (name)
# VALUES('להניח תשתית כבלים')""")

# cur.execute("""INSERT INTO task_type (name)
# VALUES('לחוות את הכבלים')""")

# cur.execute("""INSERT INTO task_type (name)
# VALUES('לסדר את האתר למסירה')""")


# cur.execute("""INSERT INTO father_task ( title,description,creator_id, is_template) VALUES('תחנת שנאים גני תקווה',
# 'הקמת תחנה חדשה בתקן יורו 2 בהספק 200 מגה ואט'
# ,1,1)""")


# cur.execute("""INSERT INTO task (title,description,type_id,domain_id,father_id,status_id,urgency_id,crew,creator_id) VALUES('חפירת תעלה לצנרת ',
# 'ציוד דרוש YAMAHAR 40T X 2', 3,1,1,1,1,
# '[1,2]','P-1310'
# )""")


# cur.execute("""INSERT INTO task (title,description,type_id,domain_id,father_id,status_id,urgency_id,crew,creator_id) VALUES('הנחת תשתית צנרת',
# 'ציוד דרוש VOLVO XT500', 4,2,1,1,1,
# '[]','P-1310'
# )""")


# cur.execute("""INSERT INTO task (title,description,type_id,domain_id,father_id,status_id,urgency_id,crew,creator_id) VALUES('פריסת כבלים',
# 'ציוד דרוש MACKITA 443', 5,3,1,1,1,
# '[]','P-1310'
# )""")


# cur.execute("""INSERT INTO task (title,description,type_id,domain_id,father_id,status_id,urgency_id,crew,creator_id) VALUES('חיוות שנאי',
# 'לעבוד על פי מפרט קבלן כפי שפורט',
# 6,4,1,1,1,
# '[]',1)""")


# cur.execute("""INSERT INTO task (title,description,type_id,domain_id,father_id,status_id,urgency_id,crew,creator_id) VALUES('סידור האתר לקראת מסירה',
# 'לשים לב שמפסל לא חורג מ3 מעלות',
# 7,5,1,1,1,'[]',1)""")


# ----------------------------------------
# Create templates

# cur.execute("""INSERT INTO father_task ( title,description,creator_id, is_template) VALUES('תחנת שנאים גני תקווה',
# 'הקמת תחנה חדשה בתקן יורו 2 בהספק 200 מגה ואט'
# ,1,1)""")


# cur.execute("""INSERT INTO task (title,description,type_id,domain_id,father_id,status_id,urgency_id,crew,creator_id,is_template) VALUES('חיוות שנאי',
# 'לעבוד על פי מפרט קבלן כפי שפורט',
# 1,1,18,1,1,
# '[]',1,1)""")


# cur.execute("""INSERT INTO task (title,description,type_id,domain_id,father_id,status_id,urgency_id,crew,creator_id,is_template) VALUES('תת משימה 2',
# 'אבגדהו זחוי',
# 1,1,18,1,1,
# '[]',1,1)""")


#####################################


# cur.execute("""INSERT INTO father_task ( title,description,creator_id, is_template) VALUES('התקמת שנאי',
# 'התקנת שנאי יורו 2 בהספק 200 מגה ואט'
# ,1,1)""")


# cur.execute("""INSERT INTO task (title,description,type_id,domain_id,father_id,status_id,urgency_id,crew,creator_id,is_template) VALUES('חיוות שנאי',
# 'לעבוד על פי מפרט קבלן כפי שפורט',
# 1,1,19,1,1,
# '[]',1,1)""")

# cur.execute("""INSERT INTO task (title,description,type_id,domain_id,father_id,status_id,urgency_id,crew,creator_id,is_template) VALUES('קינפוג שנאי',
# 'אבגדהו זחוי',
# 1,1,19,1,1,
# '[]',1,1)""")


# -----------------------------------------------------------------------------------------------


# cur.execute("""CREATE TABLE schedule_task(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     template_father_task_id INT NOT NULL,
#     start_date DATETIME,
#     schedule_value  VARCHAR(100),
#     next_date DATETIME,
#     creation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
#     modify_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# )""")

# cur.execute("""CREATE TABLE task_scheduler(
#     id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     template_father_task_id INT NOT NULL,
#     start_date DATE  DEFAULT (CURRENT_DATE),
#     end_date DATE,
#     freq INT,
#     interval_value INT,
#     specific_value VARCHAR(100),
#     next_date DATE,
#     creator_id VARCHAR(50),
#     creation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
#     modify_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# )""")

# cur.execute("""INSERT INTO task_scheduler (template_father_task_id, freq, interval_value,specific_value, creator_id )
# VALUES(1, 2,3,'[0,3]', 'P-1309')""")

cnx.commit()
cnx.close()
