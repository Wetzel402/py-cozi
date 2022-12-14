

import asyncio
from cozi import Cozi

username = 'johndoe@gmail.com'
password = 'MySuperSecretPassword!'
list_id = '' #test list
item_id = '' #test item
items_list = {'',''} #test items
item_text = 'api test item'
item_pos = 0
item_status = "complete"
list_title = "api test list"
list_type = "shopping"
attendees = {''}
appt_id = ''

cozi = Cozi(username, password)
asyncio.run(cozi.login())

"""get_lists = asyncio.run(cozi.get_lists())
print(get_lists)

add_list = asyncio.run(cozi.add_list(list_title, list_type))
print(add_list)

# untested
remove_list = asyncio.run(cozi.remove_list(list_id))
print(remove_list)

add_item = asyncio.run(cozi.add_item(list_id, item_text, item_pos))
print(add_item)

edit_item = asyncio.run(cozi.edit_item(list_id, item_id, item_text))
print(edit_item)

complete = asyncio.run(cozi.mark_item(list_id, item_id, item_status))
print(complete)

new_list = asyncio.run(cozi.add_list(list_title, list_type))
print(new_list)

remove = asyncio.run(cozi.remove_items(list_id, items_list))
print(remove)

calendar = asyncio.run(cozi.get_calendar(2022, 9))
print(calendar)

add_appt = asyncio.run(cozi.add_appointment(2022, 9, 23, "11:00", "13:00", 2, attendees, "the web", "this is a test note", "test appointment"))
print(add_appt)

# untested
edit_appt = asyncio.run(cozi.edit_appointment(appt_id, 2022, 9, 23, "11:00", "13:00", 2, attendees, "the web", "test appointment edit"))
print(edit_appt)

rem_appt = asyncio.run(cozi.remove_appointment(2022, 9, appt_id))
print(rem_appt)"""
