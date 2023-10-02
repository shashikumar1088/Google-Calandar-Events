from __future__ import print_function

from datetime import datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from db.eventsTable import EventsTable as et

class Events:
    # If modifying these scopes, delete the file token.json.
    scope = ['https://www.googleapis.com/auth/calendar.readonly']
    ETObj = None
    creds = None
    dateFormat = '%Y-%m-%d %H:%M:%S'
    def __init__(self) -> None:
        self._initiateEt()

    def _initiateEt(self) -> None:
        self.ETObj = et()

    def __getCreds(self):        
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scope)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scope)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def __addToDb(self, eventsList):
        try:
            self.ETObj.add(eventsList)
        except Exception as e:
            raise Exception(e)

    def _formatDateTime(self, dt):
        dt = datetime.fromisoformat(dt)
        return dt.strftime(self.dateFormat)

    def _today(self):
        today = datetime.now()
        return today.strftime(self.dateFormat)

    def _formatDate(self, dt): 
        dt = datetime.strptime(dt, self.dateFormat)
        return dt.date()
    
    def _formatToDateTimeObj(self, dtTime):
        return datetime.strptime(dtTime, self.dateFormat)

    def syncFromGoogle(self):
        creds = self.__getCreds()

        try:
            self.ETObj.clear()
            # Get the current date and time
            now = datetime.utcnow()

            # Define the start and end of the current month
            start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_of_month = (
                (now.replace(day=1, month=now.month % 12 + 1, year=now.year + now.month // 12)) - timedelta(days=1)
            ).replace(hour=23, minute=59, second=59, microsecond=999999)

            # Get the events for the current month            
            service = build('calendar', 'v3', credentials=creds)
            events = service.events().list(
                calendarId='primary',
                timeMin=start_of_month.isoformat() + 'Z',
                timeMax=end_of_month.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime',
            ).execute()
            eList = []
            for event in events.get('items', []):
                start = event['start'].get('dateTime', event['start'].get('date'))
                start = self._formatDateTime(start)

                end = event['end'].get('dateTime', event['end'].get('date'))
                end = self._formatDateTime(end)
                eList.append(tuple((start, end, event['summary'])))
            
            self.__addToDb(eList)

        except HttpError as error:
            print(f'An error occurred: {error}')
        
        except Exception as e:
            print(f'An error occurred: {e}')        

    def getAll(self, page = 0, pagesize = 31):
        try:
            return self.ETObj.getAll(page, pagesize)
        except Exception as e:
            print(e)

    def getUpcoming(self, page = 0, pagesize = 31):
        try:
            return self.ETObj.getAllAfterDate(self._today(), page, pagesize)
        except Exception as e:
            print(e)

    def clear(self):
        try:
            self.ETObj.clear()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    events = Events()
    # events.syncFromGoogle()
    print(events.getUpcoming())