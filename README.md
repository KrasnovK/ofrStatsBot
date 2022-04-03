# ofrStatsBot

##### Обращаемся к URL  
___
##### Общие параметры  
```
Params - пусто  
Authorization - пусто  
Headers - стандартные, плюс Content-Type = application/json
Body - JSON запроса, ничего лишнего только {"command":....}
Всегда меняем RequestId - случайный динамический параметр  
```
___

##### Список анкет - GetProjectPeriods
```json
{
  "command": "GetProjectPeriods",
  "RequestId": "RequestId",
  "data": {
    "Token": "Token",
    "ProjectId": "ProjectId"
  }
}
```

##### Список анкет - GetFormsList
```json
{
"command": "GetFormsList",
"RequestId": "RequestId",
  "data": {
    "PhotoFilter": "0",
    "FieldFilters": [],
    "UserRole": "1",
    "Skip": "0",
    "Take": "10000",
    "Token": "Token",
    "PeriodId": "PeriodId",
    "ProjectId": "ProjectId"
  }
}
```

##### Содержимое анкет - GetFormInternalFieldsData

```json
{
  "command": "GetFormInternalFieldsData",
  "RequestId": "RequestId",
  "data": {
    "AnketaId": "AnketaId",
    "Token": "Token",
    "PeriodId": "PeriodId",
    "ProjectId": "ProjectId"
  }
}
```