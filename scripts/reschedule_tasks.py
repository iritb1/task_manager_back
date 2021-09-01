# C:\projects\relay_manage\relay-manage-back>env\Scripts\python.exe -m scripts.reschedule_tasks

from api.main.model import get_db_con, QUERIES_NAMES, fetch_multiple_rows, get_db_con, QUERIES
import logging
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler(dir_path+'/tasks_rescechdule.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def reschedule_task_after_one_week():
    conn = get_db_con()
    try:
        tasks_to_reschedule = fetch_multiple_rows(
            QUERIES_NAMES.GET_TASK_TO_RESCHEDULE)
        if len(tasks_to_reschedule) > 0:
            tasks_ids = [(task['id']) for task in tasks_to_reschedule]
            format_strings = ','.join(['%s'] * len(tasks_ids))
            query = QUERIES[QUERIES_NAMES.RESCHEDULE_TASKS]
            conn = get_db_con()
            cur = conn.cursor()
            cur.execute(query % format_strings,
                        tuple(tasks_ids))
            conn.commit()
            logger.info('Successfully rescechduled tasks: ' + str(tasks_ids))
    except Exception:
        logger.exception('Failed to rescechdule tasks')
    finally:
        conn.close()


reschedule_task_after_one_week()
