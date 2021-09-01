# C:\projects\relay_manage\relay-manage-back>env\Scripts\python.exe -m scripts.create_schedule_tasks
# C:\projects\relay_manage\relay-manage-back>python -m scripts.create_schedule_tasks

from api.main.model import get_db_con, QUERIES_NAMES, create_row, fetch_one_row, fetch_multiple_rows, get_db_con, QUERIES
import logging
import os
from dateutil.rrule import rrule, WEEKLY
from datetime import date, datetime, timedelta
import pprint
import sys
from api.main.controller.task_controller import Utils as TaskUtils
from api.main.controller.father_task_controller import Utils as FatherTaskUtils
from api.main.controller.tasks_schedulers import Utils as TaskSchedulersUtils

dir_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler(dir_path+'/create_schedule_tasks.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def create_schedule_tasks():
    try:
        scheulers = fetch_multiple_rows(
            QUERIES_NAMES.GET_ALL_RELEVANT_SCHEDULERS)
        today = datetime.today().date()
        tomorrow = (datetime.today()+timedelta(days=1)).date()
        # today = tomorrow
        # tomorrow = (datetime.today()+timedelta(days=2)).date()
        for scheduler in scheulers:
            try:
                if scheduler['specific_value']:
                    scheduler['specific_value'] = eval(
                        scheduler['specific_value'])
                if scheduler['next_date']:
                    if scheduler['next_date'] == today:
                        father_task = fetch_one_row(
                            QUERIES_NAMES.GET_FATHER_TASK_BY_ID, {'id': scheduler['template_father_task_id']})
                        father_task['is_template'] = False
                        father_task['creator_id'] = 'scheduler'
                        created_father_task = FatherTaskUtils.create_father_task(
                            father_task)
                        tasks = fetch_multiple_rows(
                            QUERIES_NAMES.GET_TASKS_BY_FATHER_ID, {'father_id': scheduler['template_father_task_id']})
                        for task in tasks:
                            task['is_template'] = False
                            task['father_id'] = created_father_task['id']
                            task['creator_id'] = 'scheduler'
                            # task['start'] = today.isoformat() + \
                            #     'T00:00:00.000Z'
                            # task['end'] = (
                            #     today + timedelta(days=1)).isoformat() + 'T00:00:00.000Z'
                            created_task = TaskUtils.create_task(task)
                        next_date = TaskSchedulersUtils.calc_next_dates(
                            scheduler, 2)
                        if len(next_date) > 1:
                            scheduler['next_date'] = next_date[1]
                        else:
                            scheduler['next_date'] = None
                        if scheduler['specific_value']:
                            scheduler['specific_value'] = str(
                                scheduler['specific_value'])
                        create_row(QUERIES_NAMES.UPDATE_SCHEDULER,
                                   scheduler)
                        logger.info('Successfully created task for schduler {}, father_task id {}'.format(
                            scheduler['id'], created_father_task['id']))
            except Exception:
                logger.exception(
                    'Faild to create task for template number '+str(scheduler['id']))
        # logger.info('Successfully created tasks:')
    except Exception:
        logger.exception('Failed to rescechdule tasks')
    # finally:
    #     conn.close()


# create_schedule_tasks()
# pprint.pprint(list(rrule(MONTHLY, interval=1, dtstart=date.fromisoformat('2020-11-01'), count=10, bysetpos=None, bymonth=None, bymonthday=[12, 15],
#                          byweekday=None, byhour=None, byminute=None, bysecond=None, cache=False)))
# pprint.pprint(list(rrule(1, interval=3,
#                          dtstart=date.fromisoformat('2020-11-11'),  count=2,  bymonthday=[10])))


create_schedule_tasks()
