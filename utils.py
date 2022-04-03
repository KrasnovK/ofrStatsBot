import json
import uuid

from config import timer, TOKEN, URL, PRID

import pandas as pd
import requests

from actual_fields import actual_fields, status_id


pd.set_option('display.max_rows', None)  # Сброс кол-ва строк
pd.set_option('display.max_columns', None)  # Сброс кол-ва столбцов
pd.set_option('display.max_colwidth', None)  # Сброс кол-ва символов в записи

HEADERS = {"Content-Type": "application/json", "Accept": "text/plain"}


@timer
def get_users():
    get_users_list = json.dumps(
        {
            "command": "GetProjectUsers",
            "RequestId": uuid.uuid4().hex,
            "data": {"Token": TOKEN, "ProjectId": PRID},
        }
    )

    response = requests.post(URL, data=get_users_list, headers=HEADERS).json()
    users = pd.json_normalize(response, ["Data", "Array"]).groupby(["UserIntId", "FullName"], as_index=True).size()
    return users


@timer
def get_last_period():
    get_periods = json.dumps(
        {
            "command": "GetProjectPeriods",
            "RequestId": uuid.uuid4().hex,
            "data": {"Token": TOKEN, "ProjectId": PRID},
        }
    )

    response = requests.post(URL, data=get_periods, headers=HEADERS).json()
    period_id = pd.json_normalize(response, ["Data", "Array"])
    max_period = max(period_id["Id"])
    return str(max_period)


@timer
def get_forms_list():
    get_forms = json.dumps(
        {
            "command": "GetFormsList",
            "RequestId": uuid.uuid4().hex,
            "data": {
                "PhotoFilter": "0",
                "FieldFilters": [],
                "UserRole": "1",
                "Skip": "0",
                "Take": "10000",
                "Token": TOKEN,
                "PeriodId": get_last_period(),
                "ProjectId": PRID,
            },
        }
    )

    file = requests.post(URL, data=get_forms, headers=HEADERS).json()
    forms = pd.json_normalize(file, ["Data", "RowValues"])
    form_list = [int(form_id) for form_id in forms["FormId"]][:500]
    return form_list


@timer
def get_forms_field_data():
    forms = get_forms_list()
    get_forms_data = json.dumps(
        {
            "command": "GetFormInternalFieldsData",
            "RequestId": uuid.uuid4().hex,
            "data": {
                "AnketaId": forms,
                "Token": TOKEN,
                "PeriodId": get_last_period(),
                "ProjectId": PRID,
            },
        }
    )
    file = requests.post(URL, data=get_forms_data, headers=HEADERS).json()
    fields = file["Data"]
    columns = file["Data"]["Fields"]
    values = fields["RowValues"]
    needed_fields_index = [int(columns.index(i)) for i in columns if i in actual_fields]
    df = pd.DataFrame(values, columns=columns).iloc[:, needed_fields_index].replace({"Status_Id": status_id})
    return df


@timer
def group_by_city():
    forms = get_forms_list()
    get_forms_data = json.dumps(
        {
            "command": "GetFormInternalFieldsData",
            "RequestId": uuid.uuid4().hex,
            "data": {
                "AnketaId": forms,
                "Token": TOKEN,
                "PeriodId": get_last_period(),
                "ProjectId": PRID,
            },
        }
    )
    file = requests.post(URL, data=get_forms_data, headers=HEADERS).json()
    fields = file["Data"]
    columns = file["Data"]["Fields"]
    values = fields["RowValues"]
    needed_fields_index = [int(columns.index(i)) for i in columns if i in actual_fields]
    df = (
        pd.DataFrame(values, columns=columns)
        .iloc[:, needed_fields_index]
        .replace({"Status_Id": status_id})
        .groupby(["Город", "Status_Id"], as_index=False)
        .size()
    )
    df.replace(r"\s+", "", regex=True)

    return df

