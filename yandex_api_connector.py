from yandex_tracker_client import TrackerClient
from config import YANDEX_TOKEN, ORG_ID, twenty_min_past, time_format


client = TrackerClient(token=YANDEX_TOKEN, org_id=ORG_ID)


def get_user_id(email: str):
    """
    Функция принимает email пользователя и возвращает его id в трекере.
    """
    # Получаем список юзеров данного трекера.
    users = client.users
    user = list(filter(lambda x: (x.email == email), users))
    if len(user) == 0:
        return None
    user_id = user[0].uid
    return user_id


def get_user_tasks(user_id: str):
    """
    Функция фильтрует задачи по юзеру и возвращает список задач.
    """
    # Код очереди - название очереди Яндекс.Трекер, которое отображается в http запросе.
    queue = client.queues["PERVAA"]
    # Фильтруем задачи по юзеру.
    # Название приложения Яндекс.Трекер, которое отображается в http запросе.
    queue = client.queues["код очереди вашего трекера"]
    # Фильтруем задачи по юзеру.
    filtered_issues = client.issues.find(filter={'queue': queue.key,
                                                 'assignee': user_id,
                                                 'status': ['open', 'inProgress']},
                                         order=['-status'])
    print(type(filtered_issues))
    return filtered_issues


def get_latest_tasks_dict(user_id: str):
    """
    Функция фильтрует задачи по юзеру и времени и возвращает обновления за последние 20 миинут.
    """
    queue = client.queues["PERVAA"]
    # Фильтруем задачи с учетом временных рамок.
    queue = client.queues["код очереди вашего трекера"]
    # Задаем таймзону и время, чтобы отфильтровать новые задачи за последние 20 минут.
    # Фильтруем задачи с учетом временных рамок.
    filtered_issues = client.issues.find(filter={'queue': queue.key,
                                                 'assignee': user_id,
                                                 'status': ['open', 'inProgress'],
                                                 'created': {
                                                     "from": twenty_min_past.strftime(time_format)
                                                 }},
                                         order=['-status'])
    return filtered_issues


def get_tasks_dict(issues: list):
    """
    Функция парсит задачи и возвращает список из словарей с интересущими нас полями.
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
    Общая функция, получающая email и возвращающая список всех задач этого юзера.
    """
    id = get_user_id(email)
    # Проверка, что юзер был найден. Если в системе нет такого email адреса, возвращает None.
    if id is None:
        return None
    issues_list = get_user_tasks(id)
    tasks = get_tasks_dict(issues_list)

    return tasks


def get_latest_tasks(email: str):
    """
    Общая функция, получающая email и возвращающая список новых задач за последние 20 минут.
    """
    id = get_user_id(email)
    # Проверка, что юзер был найден. Если в системе нет такого email адреса, возвращает None.
    if id is None:
        return None
    issue_list = get_latest_tasks_dict(id)
    tasks = get_tasks_dict(issue_list)

    return tasks
