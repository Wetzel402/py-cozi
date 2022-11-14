import asyncio
from cozi import Cozi

username = 'johndoe@email.com'
password = 'MySuperSecretPassword!'
list_id = 'listIdFromCozi'
item_id = 'itemIdFromCozi'
items_list = [{"status":"complete","itemId":"b3e23bcc-b90a-4d0d-9657-67958563e17c","itemType":None,"text":"item 1"},
{"status":"complete","itemId":"a9879ae1-078a-4185-b090-68fffe033905","itemType":"header","text":"item 2"}]
item_text = 'test item'
item_pos = 0
item_status = "complete"
list_title = "Test list"
list_type = "shopping"
attendees = ['personIdFromCozi-1', 'personIdFromCozi-2']
appt_id = 'appointmentIdFromCozi'

cozi = Cozi(username, password)
asyncio.run(cozi.login())

"""
get_lists = asyncio.run(cozi.get_lists())
print(get_lists)

add_list = asyncio.run(cozi.add_list(list_title, list_type))
print(add_list)

remove_list = asyncio.run(cozi.remove_list(list_id))
print(remove_list)

reorder_list = asyncio.run(cozi.reorder_list(list_id, list_title, items_list, list_type))
print(reorder_list)

add_item = asyncio.run(cozi.add_item(list_id, item_text, item_pos))
print(add_item)

edit_item = asyncio.run(cozi.edit_item(list_id, item_id, item_text))
print(edit_item)

complete = asyncio.run(cozi.mark_item(list_id, item_id, item_status))
print(complete)

remove = asyncio.run(cozi.remove_items(list_id, items_list))
print(remove)

calendar = asyncio.run(cozi.get_calendar(2022, 9))
print(calendar)

add_appt = asyncio.run(cozi.add_appointment(2022, 9, 23, "11:00", "13:00", 2, attendees, "the web", "this is a test note", "test appointment"))
print(add_appt)

edit_appt = asyncio.run(cozi.edit_appointment(appt_id, 2022, 11, 14, "11:00", "13:00", 2, attendees, "the web", "some test notes", "test appointment edit"))
print(edit_appt)

rem_appt = asyncio.run(cozi.remove_appointment(2022, 9, appt_id))
print(rem_appt)
"""