from langchain_google_calendar_tools.utils import build_resource_service, get_oauth_credentials
from langchain_google_calendar_tools.tools.create_new_event.tool import CreateNewEvent
from langchain_google_calendar_tools.tools.list_events.tool import ListEvents
from langchain_google_calendar_tools.tools.update_exist_event.tool import UpdateExistEvent

from langchain_google_calendar_tools.helper_tools.get_current_datetime import GetCurrentDatetime

credentials = get_oauth_credentials("./calendarToken.json","./utils/credentials.json",["https://www.googleapis.com/auth/calendar"])

api_resource = build_resource_service(credentials=credentials)

calendarToolkit = [ListEvents(api_resource=api_resource),
        CreateNewEvent(api_resource=api_resource),
        UpdateExistEvent(api_resource=api_resource),
        GetCurrentDatetime()]
