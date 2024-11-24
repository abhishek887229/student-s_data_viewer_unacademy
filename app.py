import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Google Sheets setup
SERVICE_ACCOUNT_FILE = 'key.json'  # Path to your service account key file
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']  # Define read-only scope

# Authenticate with the service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
sheet_service = build('sheets', 'v4', credentials=credentials)

# Google Sheet details
SPREADSHEET_ID = '1ziAE7ipLx_NFXZP-2MvjQtPmHBpUj-RT-GfIPOqwqOA'  # Replace with your actual sheet ID
RANGE_NAME = 'Sheet1!A:F'  # Adjusted range to include all relevant columns (A to F)

# Streamlit app title
st.title("Student Result Checker")
st.subheader("by Unacademy offline center Dugri")
st.write("---")

# Input for roll number
roll_no = st.text_input("Enter your Roll Number:")

if st.button("Get Result"):
    if roll_no:
        try:
            # Fetch data from Google Sheets
            result = sheet_service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME
            ).execute()

            rows = result.get('values', [])
            if not rows:
                st.error("No data found in the spreadsheet.")
            else:
                # Assuming the first row contains headers
                headers = rows[0]  # Header row
                data = rows[1:]    # Data rows
                
                # Ensure proper column names exist in the header
                try:
                    roll_no_index = headers.index("Roll no.")  # Roll no. column
                    name_index = headers.index("CANDIDATE NAME")  # Name column
                    phy_index = headers.index("PHY")  # Physics column
                    chem_index = headers.index("CHEM")  # Chemistry column
                    total_index = headers.index("Total")  # Total column
                except ValueError as e:
                    st.error("Header mismatch! Please ensure the sheet headers match: Roll no., CANDIDATE NAME, PHY, CHEM, Total.")
                    st.stop()

                # Search for the roll number
                found = False
                for row in data:
                    # Ensure row length matches header length
                    if len(row) >= total_index + 1 and row[roll_no_index] == roll_no:
                        st.success(f"Result for Roll Number {roll_no}:")
                        st.write(f"**Name:** {row[name_index]}")
                        st.write(f"**Physics Marks:** {row[phy_index]}")
                        st.write(f"**Chemistry Marks:** {row[chem_index]}")
                        st.write(f"**Total Marks:** {row[total_index]}")
                        found = True
                        break

                if not found:
                    st.error("Roll Number not found. Please check and try again.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a Roll Number.")
