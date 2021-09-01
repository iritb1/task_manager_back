# C:\projects\relay_manage\relay-manage-back>env\Scripts\python.exe -m scripts.delete_father_tasks

from api.main.model import get_db_con, QUERIES_NAMES, fetch_multiple_rows, get_db_con, QUERIES
import logging
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler(
    dir_path+'/delete_father_tasks_without_childs.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def delete_father_tasks_without_childs():
    conn = get_db_con()
    try:
        father_tasks_to_delete = fetch_multiple_rows(
            QUERIES_NAMES.GET_FATHER_TASKS_WITHOUT_CHILDS)
        if len(father_tasks_to_delete) > 0:
            father_tasks_ids = [(father_task['id'])
                                for father_task in father_tasks_to_delete]
            format_strings = ','.join(['%s'] * len(father_tasks_ids))
            query = QUERIES[QUERIES_NAMES.DELETE_FATHERS_TASKS]
            conn = get_db_con()
            cur = conn.cursor()
            cur.execute(query % format_strings,
                        tuple(father_tasks_ids))
            conn.commit()
            logger.info(
                'Successfully deleted father tasks: ' + str(father_tasks_ids))
    except Exception:
        logger.exception('Failed to deleted father tasks')
    finally:
        conn.close()


delete_father_tasks_without_childs()
