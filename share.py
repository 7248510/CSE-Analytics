import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
for spreadsheet in client.openall():
#     if spreadsheet.title == '10.96.4.60':
# client.del_spreadsheet("1Qa9cZgN9veVmRVfAoep3TnyN4XrInheig7C7ckcxeX4")
# client.del_spreadsheet("1m13tGTtvb56QTgWM6omTyUXJjSgZdpYznyLWCn5DMX4")
# client.del_spreadsheet("1CzKaCgiB82LUeffwXiBDA37ViTKhmWgq2pqsnI3b_Qw")
# client.del_spreadsheet("1vy-yelmK_47eg9S-eS1aH88Vf9QX1S-YTDVHwuH2RlQ")
    print(spreadsheet)
    spreadsheet.share('', perm_type='user', role='writer')
    spreadsheet.share('', perm_type='user', role='writer')
