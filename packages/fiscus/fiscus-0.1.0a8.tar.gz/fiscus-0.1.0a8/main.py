import sys
import os

# from sdk_toolkit import (
#     client, user,
#     add_gmail_connector, authenticate_gmail_connector, execute_gmail_get_email,
#     execute_gmail_list_emails, execute_gmail_send_email, execute_ai_task,
#     on_fetch_categories, on_category_selection, on_fetch_connectors,
#     on_connector_selection, on_fetch_operations, on_operation_selection,
#     on_fetch_operation_details, on_task_creation,
#     test_coinbase_authentication, test_coinbase_deauthentication,
#     execute_plaid_task
# )

# # authenticate_gmail_connector()

# # execute_gmail_get_email()

# # Add the 'src' directory to the Python path for access to the SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from fiscus import FiscusClient, FiscusLogLevel, FiscusConnectionType, FiscusFile

client = FiscusClient(
    api_key='fiscus_production_394a5d73_f3cbabd01364dde698bea9bb8125d1f7cab7606c429d644ebc7869651a094e92',
    user_id='1234',
	logging_level=FiscusLogLevel.DEBUG,
	connection_type=FiscusConnectionType.REST
)

# execute_ai_task()

# response = client.execute(
# 	connector_name='microsoft_graph',
# 	operation='create_event',
# 	params={
# 		"subject": "Meeting with team",
# 		"startDateTime": "2024-11-17T10:00:00",
# 		"endDateTime": "2024-11-17T11:00:00",
# 		"timeZone": "Pacific Standard Time"
# 	}
# )

# response = client.execute(
#     connector_name='zoom',
#     operation='create_meeting',
#     params={
#         "topic": "Test Zoom Meeting",
#         "agenda": "Discuss project updates",
#         "start_time": "2024-11-12T09:00:00Z",  # Today's date in ISO format
#         "duration": 60,  # Duration in minutes
#         "timezone": "America/Los_Angeles",
#         # "password": "123456",
#         "settings": {
#             "host_video": True,
#             "participant_video": False,
#             "join_before_host": False,
#             "mute_upon_entry": True,
#             "waiting_room": True,
#             "audio": "both",
#             "auto_recording": "cloud"
#         },
# 		"meeting_invitees": [
# 			{"email": "hearsch@fiscusflows.com"}
# 		],
#         "type": 2  # Type 2 for a scheduled meeting
#     }
# )


# connector_response = client.user.add_connector('office_365')
# connector_response = client.user.authenticate_connector('office_365')

# connector_response = client.user.deauthenticate_connector('office_365')

# if connector_response.success:
# 	print(connector_response.result)
# else:
# 	print(connector_response.error)

# tasks = [
#     {
#       "id": "fetch_bitcoin_price",
#       "connector": "CoinDeskAPI",
#       "operation": "get_current_bitcoin_price",
#       "params": {},
#       "onSuccess": {
#         "updateContext": {
#           "btc_price": "context.response.bpi.USD.rate_float"
#         }
#       }
#     },
#     {
#       "id": "check_price_threshold",
#       "connector": "LogicAPI",
#       "operation": "evaluate_expression",
#       "params": {
#         "expression": "context.btc_price > 50000"
#       },
#       "conditions": [
#         {
#           "type": "if",
#           "expression": "context.btc_price > 50000",
#           "nestedTasks": [
#             {
#               "id": "log_high_price",
#               "connector": "LoggingAPI",
#               "operation": "log_message",
#               "params": {
#                 "message": "Bitcoin price is high: $${context.btc_price}"
#               }
#             }
#           ]
#         },
#         {
#           "type": "else",
#           "nestedTasks": [
#             {
#               "id": "log_low_price",
#               "connector": "LoggingAPI",
#               "operation": "log_message",
#               "params": {
#                 "message": "Bitcoin price is relatively low: $${context.btc_price}"
#               }
#             }
#           ]
#         }
#       ]
#     }
#   ]

# response = client.execute(
# 	# tasks=tasks
# 	connector_name='coindesk',
# 	operation='get_current_bitcoin_price'
# )


#### Zach Flow ####
# 1A. Create a Task List
# response = client.execute(
# 	connector_name='office_365',
# 	operation='create_task_list',
# 	params={
# 		"displayName": "Memories",
# 	}
# )

# 1B. Get All Task Lists
# response = client.execute(
# 	connector_name='office_365',
# 	operation='get_task_lists',
# )

# (Optional)
# response = client.execute(
# 	connector_name='office_365',
# 	operation='get_tasks',
# 	params={
# 		'tastListId': 'AAMkADMzNmI3Y2RhLWYyMDYtNDkwZC1hN2Q0LWJiMmFhZjE3NTQxNAAuAAAAAAD56FJcDClqRYa_ivLLO0fNAQD3WR3C90ZuQ5nQMrfQwFhuAAAAAAESAAA='
# 	}
# )

# 2. Create an Individual Task
# response = client.execute(
#     connector_name='office_365',
#     operation='create_task',
#     params={
#         "todoTaskListId": "AAMkADMzNmI3Y2RhLWYyMDYtNDkwZC1hN2Q0LWJiMmFhZjE3NTQxNAAuAAAAAAD56FJcDClqRYa_ivLLO0fNAQD3WR3C90ZuQ5nQMrfQwFhuAAA0QEP5AAA=",
#         "title": "A new task",
#         "categories": ["Important"],
#         "linkedResources": [
#             {
#                 "webUrl": "http://microsoft.com",
#                 "applicationName": "Microsoft",
#                 "displayName": "Microsoft"
#             }
#         ]
#     }
# )

# 3. Create an Event
# response = client.execute(
# 	connector_name='office_365',
# 	operation='create_event',
# 	params={
# 		"subject": "Meeting with team",
# 		"startDateTime": "2024-11-17T10:00:00",
# 		"endDateTime": "2024-11-17T11:00:00",
# 		"timeZone": "Pacific Standard Time"
# 	}
# )

# 4. Get User's Drive
# response = client.execute(
#     connector_name='office_365',
#     operation='get_drive',
# )

# 5. Upload File to User's Drive
response = client.execute(
	connector_name='office_365',
    operation='upload_item',
	params={
		"folderPath": "fiscus",
		"fileName": "Requirements File",
	},
	files=[
		FiscusFile(
			targetField='file',
			name='Requirements File',
			type='text/plain',  # MIME type for plain text
			content='./requirements.txt'  # Replace with the actual content you want to upload
		)
	]
)

# tasks = [
#     {
#       "id": "get_task_lists",
#       "connector": "office_365",
#       "operation": "get_task_lists",
#       "onSuccess": {
#         "updateContext": {
#           "taskLists": "response.value"
#         }
#       }
#     },
#     {
#       "id": "get_tasks",
#       "connector": "office_365",
#       "operation": "get_tasks",
#       "params": {
#         "taskListId": "context.taskLists[0].id"
#       },
#       "onSuccess": {
#         "updateContext": {
#           "tasks": "response.value"
#         }
#       },
#       "conditions": [
#         {
#           "type": "if",
#           "expression": "context.taskLists.length > 0",
#           "nestedTasks": [
#             {
#               "id": "create_task",
#               "connector": "office_365",
#               "operation": "create_task",
#               "params": {
#                 "todoTaskListId": "context.taskLists[0].id",
#                 "title": "Import Task for Dustin",
#                 "categories": ["Important"],
#                 "linkedResources": [
#                   {
#                     "webUrl": "https://fiscusflows.com",
#                     "applicationName": "Fiscus",
#                     "displayName": "Fiscus"
#                   }
#                 ]
#               },
#               "onSuccess": {
#                 "updateContext": {
#                   "taskCreated": True
#                 }
#               }
#             }
#           ]
#         }
#       ]
#     },
#     {
#       "id": "create_event",
#       "connector": "office_365",
#       "operation": "create_event",
#       "params": {
#         "subject": "Dustin Test Meeting",
#         "startDateTime": "2024-11-18T10:00:00",
#         "endDateTime": "2024-11-18T11:00:00",
#         "timeZone": "Pacific Standard Time"
#       },
#       "onSuccess": {
#         "updateContext": {
#           "eventCreated": True
#         }
#       }
#     },
#     {
#       "id": "get_drive",
#       "connector": "office_365",
#       "operation": "get_drive",
#       "onSuccess": {
#         "updateContext": {
#           "drive": "response"
#         }
#       }
#     },
    # {
    #   "id": "upload_file",
    #   "connector": "office_365",
    #   "operation": "upload_item",
    #   "params": {
    #     "folderPath": "fiscus",
    #     "fileName": "Requirements File"
    #   },
    #   "files": [
    #     {
    #       "targetField": "file",
    #       "name": "Requirements File",
    #       "type": "text/plain",
    #       "content": "./requirements.txt"
    #     }
    #   ],
    #   "onSuccess": {
    #     "updateContext": {
    #       "fileUploaded": True
    #     }
    #   }
    # }
# ]

# response = client.execute(
# 	tasks=tasks
# )

if response.success:
	print(response.data)
else:
	print(response.error_message)
