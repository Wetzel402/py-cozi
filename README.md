# py-cozi

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Methods](#methods)
- [Exceptions](#exceptions)

<a name="introduction"></a>
## Introduction

Unofficial python wrapper for the Cozi API. This library requires `Python >=3.5`.

<a name="installation"></a>
## Installation

```bash
pip install py-cozi
```

<a name="usage"></a>
## Usage

```
import asyncio
from cozi import Cozi

username = ''
password = ''

cozi = Cozi(username, password)
asyncio.run(cozi.login())

get_lists = asyncio.run(cozi.get_lists())
print(get_lists)
```

<a name="methods"></a>
## Methods
```def login()```

Logs into Cozi.

---

```def get_lists()```

Gets all of your lists.

---

```def add_list(list_title, list_type)```

Adds a new list.

| Parameter   | Type        | Description           |
| :---        |    :---     |                  :--- |
| list_title  | string      | Title of your list    |
| list_type   | string      | 'todo' or 'shopping'  |

---

```def remove_list(list_id)```

Removes a list.

| Parameter   | Type        | Description           |
| :---        |    :---     |                  :--- |
| list_id     | string      | Cozi list id          |

---

```def reorder_list(list_id, list_title, items_list, list_type)```

Reorders a list.

| Parameter   | Type        | Description                |
| :---        |    :---     |                       :--- |
| list_id     | string      | Cozi list id               |
| list_title  | string      | Title or name of your list |
| items_list  | list        | List of JSON Cozi items    |
| list_type   | string      | 'todo' or 'shopping'       |

---

```def add_item(list_id, item_text, item_pos)```

Adds an item to a list.

| Parameter   | Type        | Description                      |
| :---        |    :---     |                             :--- |
| list_id     | string      | Cozi list id                     |
| item_text   | string      | Title or name of your item       |
| item_pos    | int         | Array index position of the item |

---

```def edit_item(list_id, item_id, item_text)```

Edits an item in a list.

| Parameter   | Type        | Description                |
| :---        |    :---     |                       :--- |
| list_id     | string      | Cozi list id               |
| item_id     | string      | Cozi item id               |
| item_text   | string      | Title or name of your item |

---

```def mark_item(list_id, item_id, item_status)```

Checks or completes and item in a list.

| Parameter   | Type        | Description                |
| :---        |    :---     |                       :--- |
| list_id     | string      | Cozi list id               |
| item_id     | string      | Cozi item id               |
| item_status | string      | 'complete' or 'incomplete' |

---

```def remove_items(list_id, items_list)```

Removes item(s) from a list.

| Parameter   | Type        | Description                |
| :---        |    :---     |                       :--- |
| list_id     | string      | Cozi list id               |
| items_list  | list        | List of Cozi item IDs      |

---

```def get_calendar(year, month)```

Gets calendar appointments for a given year and month. 

| Parameter   | Type        | Description |
| :---        |    :---     |        :--- |
| year        | int         | Year        |
| month       | int         | Month       |

---

```def add_appointment(year, month, day, start, end, date_span, attendees, location, notes, subject)```

Adds a new calendar appointment.  

| Parameter   | Type        | Description                          |
| :---        |    :---     |                                 :--- |
| year        | int         | Year                                 |
| month       | int         | Month                                |
| day         | int         | Day                                  |
| start       | string      | Start time in 24 hour format `08:00` |
| end         | string      | End time in 24 hour format `21:00`   |
| date_span   | int         | Days the appointment spans           |
| attendees   | list        | List of Cozi person IDs              |
| location    | string      | Location of the appointment          |
| notes       | string      | Notes for the appointment            |
| subject     | string      | The title or name of the appointment |

---

```def edit_appointment(appt_id, year, month, day, start, end, date_span, attendees, location, notes, subject)```

Edits a calendar appointment.  

| Parameter   | Type        | Description                          |
| :---        |    :---     |                                 :--- |
| appt_id     | string      | Cozi appointment ID                  |
| year        | int         | Year                                 |
| month       | int         | Month                                |
| day         | int         | Day                                  |
| start       | string      | Start time in 24 hour format `08:00` |
| end         | string      | End time in 24 hour format `21:00`   |
| date_span   | int         | Days the appointment spans           |
| attendees   | list        | List of Cozi person IDs              |
| location    | string      | Location of the appointment          |
| notes       | string      | Notes for the appointment            |
| subject     | string      | The title or name of the appointment |

---

```def remove_appointment(year, month, appt_id)```

Removes a calendar appointment.  

| Parameter   | Type        | Description                          |
| :---        |    :---     |                                 :--- |
| year        | int         | Year                                 |
| month       | int         | Month                                |
| appt_id     | string      | Cozi appointment ID                  |

<a name="exceptions"></a>
## Exceptions

```CoziException```

---

```InvalidLoginException``` 

Thrown when login fails.

---

```RequestException```

Thrown when the connection is reset.