import sys

from api.main.model.pushers import execute_sql



def create_schema(actions=['insert']):

    if 'create' in actions:
        execute_sql('DROP TABLE status')
        sql = '''
       CREATE TABLE `status` (
        `id` int unsigned NOT NULL AUTO_INCREMENT,
        ` name` varchar(30) NOT NULL,
        `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`)
        ) '''
        execute_sql(sql)
    
    if 'insert' in actions:
        # Insert task types
        execute_sql("DELETE FROM task_type")
        sql = """INSERT INTO task_type (name,equipment_required,create_time) VALUES 
                ('משימה כללית',0,'2020-10-12 18:01:15')
                ,('תיקון תקלה',0,'2020-10-12 18:01:15')
                ,('ריתוך סיב',1,'2020-10-12 18:01:15')
                ,('להניח תשתית צנרת',0,'2020-10-12 18:01:15')
                ,('להניח תשתית כבלים',0,'2020-10-12 18:01:15')
                ,('לחוות את הכבלים',0,'2020-10-12 18:01:15')
                ,('התקנת ציוד',1,'2020-10-12 18:01:15')
                ,('תקלת מוניטור',0,'2020-10-27 10:21:54')
                ,('',0,'2021-08-22 12:51:48')
                ;
                """
        execute_sql(sql)

        # Insert urgency
        execute_sql("DELETE FROM urgency")
        sql = """INSERT INTO urgency (name,create_time) VALUES 
                ('נמוך','2020-09-30 14:41:10')
                ,('רגיל','2020-09-30 14:41:10')
                ,('גבוהה','2020-09-30 14:41:10')
                ;
                """
        execute_sql(sql)

        # Insert status
        execute_sql("DELETE FROM status")
        sql = """INSERT INTO status (name,create_time) VALUES 
                ('ממתין','2020-10-01 11:01:25')
                ,('בביצוע','2020-10-01 11:01:25')
                ,('הושלם','2020-10-01 11:01:25')
                ;
                """
        execute_sql(sql)