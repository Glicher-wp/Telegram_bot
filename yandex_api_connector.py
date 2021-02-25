import os
import datetime
import pytz

from yandex_tracker_client import TrackerClient



#Айди организации. Находится в профиле рекера
ORG_ID = os.environ.get('ORG_ID')
#Токен приложения трекера
YANDEX_TOKEN = os.environ.get('YANDEX_TOKEN')

client = TrackerClient(token=YANDEX_TOKEN, org_id=ORG_ID)


def get_user_id(email: str):
    """
    Функция принимает email пользователя и возвращает его id в трекере
    """
    #получаем список юзеров данного трекера
    users = client.users
    for user in users:
        # ищем нужного нам юзера
        if user.email == email:
            user_id = user.uid
            print(user.email)
            return user_id
        #если юзер вернул не правильный имейл, либо если такого имейла нет в системе
        else:
            return False


def get_user_tasks(user_id: str):
    """
    Функция фильтрует задачи по юзеру и возвращает список задач
    """
    #название приложения Яндекс.Трекер, которое отображается в http запросе
    queue = client.queues["код очереди вашего трекера"]
    #фильтруем задачи по юзеру
    filtered_issues = client.issues.find(filter={'queue': queue.key,
                                                 'assignee': user_id,
                                                 'status': ['open', 'inProgress']},
                                         order=['-status'])
    print(type(filtered_issues))
    return filtered_issues


def get_latest_tasks_dict(user_id: str):
    """
    Функция фильтрует задачи по юзеру и времени и возвращает обновления за последние 20 миинут
    """
    queue = client.queues["код очереди вашего трекера"]
    #задаем таймзону и время, чтобы отфильтровать новые задачи за последние 20 минут
    tz = pytz.timezone("Europe/Moscow")
    twenty_min_past = datetime.datetime.now(tz) - datetime.timedelta(minutes=20)
    #фильтруем задачи с учетом временных рамок
    filtered_issues = client.issues.find(filter={'queue': queue.key,
                                                 'assignee': user_id,
                                                 'status': ['open', 'inProgress'],
                                                 'created': {
                                                     "from": twenty_min_past.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
                                                 }},
                                         order=['-status'])
    return filtered_issues


def get_tasks_dict(issues: list):
    """
    Функция парсит задачи и возвращает список из словарей с интересущими нас полями
    """
    issues_list = []
    for issue in issues:
        issue_dict = {
                "issue": issue.summary,
                "description": issue.description,
                "status": issue.status.display,
                "deadline": issue.deadline,
        }
        issues_list.append(issue_dict)
    return issues_list


def get_tasks(email: str):
    """
    Общая функция, получающая email и возвращающая список всех задач этого юзера
    """
    id = get_user_id(email)
    #проверка, что юзер был найден. Если в системе нет такого email адреса, возвращает False
    if id is False:
        return False
    issues_list = get_user_tasks(id)
    tasks = get_tasks_dict(issues_list)

    return tasks


def get_latest_tasks(email: str):
    """
    Общая функция, получающая email и возвращающая список новых задач за последние 20 минут
    """
    id = get_user_id(email)
    # проверка, что юзер был найден. Если в системе нет такого email адреса, возвращает False
    if id is False:
        return False
    issue_list = get_latest_tasks_dict(id)
    tasks = get_tasks_dict(issue_list)

    return tasks
