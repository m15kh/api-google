import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

creds = None

#token = '7138018453:AAHlrep8ra64s_Sfimn4wzgXgmZhyXto7KQ'

# This function checks if there is existing Authentation Token,
# otherwise it generates a new one 
def getCredentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/tasks"])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("secretfile.json",
                                                             ["https://www.googleapis.com/auth/tasks"])
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


# This object is used for building the service
credsTasks = getCredentials()


# This methods builds the service and returns it
def getService():
    return build("tasks", "v1", credentials=credsTasks)


# This object holds the instance of the google service
serviceTasks = getService()


# Show Tasklists and ID
def listTaskList():
    lst_header_tasks = []
    result = serviceTasks.tasklists().list(maxResults=10).execute()
    taskList = result.get("items", [])
    for item in taskList:
        itemID = item.get('id')
        itemName = item.get('title')
        lst_header_tasks.append((itemName, itemID))
    print(lst_header_tasks)
    return  lst_header_tasks


# Show Task from a Tasklist
def getTaskFromList(listID, filter=True):
    lst_detail_tasks = []
    tasklist = serviceTasks.tasks().list(tasklist=listID, showHidden=filter).execute()
    tasks = tasklist.get("items", [])
    for task in tasks:
        title = task.get('title')
        id = task.get('id')
        lst_detail_tasks.append((title, id))
    print(lst_detail_tasks)
    print(tasks)
    return lst_detail_tasks


# Status:
# completed - checked in google tasks
# needsAction - unchecked in google tasks
def setTaskStatus(itemID, status):
    mainList = serviceTasks.tasklists().list(maxResults=10).execute()
    mainItems = mainList.get("items", [])
    parentKey = None
    toComplete = None
    for item in mainItems:
        ID = item.get('id')
        child = serviceTasks.tasks().list(tasklist=ID, pageToken=None).execute()
        tasks = child.get("items", [])
        for task in tasks:
            if task.get('id') == itemID:
                parentKey = item.get('id')
                toComplete = task
                break

    if toComplete != None:
        toComplete['status'] = status
        serviceTasks.tasks().update(tasklist=parentKey, task=toComplete['id'], body=toComplete).execute()
        print('successfully updated')
    else:
        print('item not found')


def maincode():
    try:
        # LEt's check if a token.json is created
        getCredentials()

        # LEt's try to read the task list
        listTaskList()

        # get Task from List
        # true here is whether to show completed tasks
        getTaskFromList('REpLbnhrS1JCZ1JrMFBsVA',False)

        # mark a task to complete
        # setTaskStatus('cnJ4M2lFRlJPUXRvUV9RWg','needsAction')

    except HttpError as err:
        print(err)


listTaskList()
getTaskFromList('REpLbnhrS1JCZ1JrMFBsVA',False)
