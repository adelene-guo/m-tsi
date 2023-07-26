import gspread
from oauth2client.service_account import ServiceAccountCredentials

def clear_data_from_row_2(spreadsheet_name, worksheet_index=0):
    # Set up credentials
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\chase\Downloads\sixth-hawk-393504-f8baa14e8c72.json', scope)
    client = gspread.authorize(creds)

    # Open the specified spreadsheet
    spreadsheet = client.open(spreadsheet_name)
    worksheet = spreadsheet.get_worksheet(worksheet_index)

    # Get total rows
    num_rows = worksheet.row_count

    # Delete rows from 2 to the end
    if num_rows > 1:
        worksheet.delete_rows(2, num_rows)

    print(f"Cleared data from row 2 to end in '{spreadsheet_name}'!")

if __name__ == "__main__":
    clear_data_from_row_2('userSongs')
    clear_data_from_row_2('playlist')

