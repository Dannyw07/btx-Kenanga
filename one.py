from libraries import *
from emailBody import generate_email_body, image1_base64, image2_base64

class one(tk.Frame):

    def process_html_content(html_content):
        # Parse the HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the first table
        table1 = soup.find("table")

        # Find the second table with the id "gvEodEnqSumm"
        table2 = soup.find("table", id="gvEodEnqSumm")

        process_date_label = soup.find("span", id="Label1").text
        process_date_value = soup.find("span", id="lblProcDate").text

        # Print the extracted data
        print(process_date_label + ":", process_date_value)
       
        # Extract data from the first table
        data1 = []
        for row in table1.find_all("td", id="tdBG"):
            row_data = []
            for cell in row.find_all(["span"]):
                cell_text = cell.get_text(strip=True)
                if cell_text:  # Check if cell text is not empty
                    row_data.append(cell_text)
            if row_data:  # Only append if row_data is not empty
                data1.append(row_data)

        # Extract table headers from the second table
        table2_headers = []
        for th in table2.find_all("th"):
            header_text = th.get_text(strip=True)
            if header_text:  # Check if header text is not empty
                table2_headers.append(header_text)

        # Extract data from the second table
        data2 = []
        for row in table2.find_all("tr"):
            row_data = []
            for cell in row.find_all(["td"]):
                cell_text = cell.get_text(strip=True)
                if cell_text:  # Check if cell text is not empty
                    row_data.append(cell_text)
            if row_data:  # Only append if row_data is not empty
                data2.append(row_data)

        # Combine data from table1 and table2
        combined_data = data1 + [table2_headers] + data2 

        # Create a folder named "xlsx_files" if it doesn't exist
        folder_name = "xlsx_files"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Get current date
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')

        # Create a new folder with the current date inside the 'xlsx_files'
        subfolder_name = os.path.join(folder_name, current_date)
        if not os.path.exists(subfolder_name):
            os.makedirs(subfolder_name)

        # Path to the Excel file inside the subfolder
        excel_file_path = os.path.join(subfolder_name, "tableOne.xlsx")

        # Create a new workbook and add a worksheet
        workbook = xlsxwriter.Workbook(excel_file_path)
        worksheet = workbook.add_worksheet('Sheet1')

        # Define colors in hexadecimal format
        white_color_hex = '#FFFFFF'
        grey_color_hex = '#f5f5f5'
        deep_grey_color_hex = '#d7dae1'
        blue_font_hex = '#0b14fe'

        # Define bold format
        bold_format = workbook.add_format({'bold': True})

        # Write combined data to XLSX
        for row_index, row_data in enumerate(combined_data):
            # Choose color based on row index
            if row_index == len(data1):  # Header row
                cell_format = workbook.add_format({'bg_color': deep_grey_color_hex, 'font_color': blue_font_hex})
            elif row_index % 2 == 0:
                cell_format = workbook.add_format({'bg_color': white_color_hex})  # White color
            else:
                cell_format = workbook.add_format({'bg_color': grey_color_hex})  # Grey color

            for col_index, cell_data in enumerate(row_data):
                if row_index == len(data1):  # Header row
                    if cell_data == "Task ID":  # Adjust width for "Task Name" header
                        worksheet.set_column(col_index, col_index, 25)  # Set width to 300px (approx.)
                    elif cell_data == "Task Name":
                        worksheet.set_column(col_index, col_index, 40)  # Set width for "Start Time" header
                    elif cell_data == "Start Time":
                        worksheet.set_column(col_index, col_index, 20)  # Set width for "Start Time" header
                    elif cell_data == "Actual Start Time":
                        worksheet.set_column(col_index, col_index, 20)  # Set width for "Actual Start Time" header
                    elif cell_data == "Actual End Time":
                        worksheet.set_column(col_index, col_index, 20)  # Set width for "Actual End Time" header
                    elif cell_data == "Duration":
                        worksheet.set_column(col_index, col_index, 20)  # Set width for "Duration" header
                    elif cell_data == "Status":
                        worksheet.set_column(col_index, col_index, 25)  # Set width for "Status" header
                    worksheet.write(row_index, col_index, cell_data, bold_format)
                else:
                    worksheet.write(row_index, col_index, cell_data, cell_format)

        # Adjust column widths
        for i, column in enumerate(zip(*combined_data)):
            max_length = max(len(str(cell)) for cell in column)
            worksheet.set_column(i, i, max_length +5)  # Add a little extra space

        workbook.close()

        # Load the Excel file
        file_path = excel_file_path
        try:
            df = pd.read_excel(file_path,header=None)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            exit()
        
        df = df.fillna('')

        # Convert the DataFrame to an HTML table with no index
        html_table = df.to_html(index=False, header=False)

        # Modify the HTML table to make the header grey
        soup = BeautifulSoup(html_table, "html.parser")
        tr_elements = soup.find_all("tr")[1:]  # Select rows starting from the third row

        for idx, element in enumerate(soup.find_all(["td"])):
            if element.name == "td":
                if element.text.strip() in ["Task ID", "Task Name", "Start Time", "Actual Start Time", "Actual End Time", "Duration", "Next Day", "Status"]:
                    element['style'] = 'background-color:#d7dae1; color:#0b14fe; font-weight:bold;'
          
        for tr_element in tr_elements:
            # Find all table cells within the current row
            td_elements = tr_element.find_all("td")
            
            # Get the last table cell in the current row
            last_td_element = td_elements[-1]
            
            # Add padding to the last cell
            last_td_element['style'] = 'padding: 5px;'
            
            # Check if the text content of the last cell contains "Process Succeeded!"
            if "Process Succeeded!" in last_td_element.text.strip():
                # If it does, set the background color to green and text color to white
                last_td_element['style'] += 'background-color: green; color: white;'
            else:
                # If not, set the background color to red and text color to white
                last_td_element['style'] += 'background-color: red; color: white;'


        html_table = str(soup)
        # print(html_table)

        body = generate_email_body(image1_base64,image2_base64)
  
        html_content = f"<p>Process Date: {process_date_value}</p>\n\n{html_table}\n{body}"

        # Set up the email details
        sender_email = "dannywong@kenanga.com.my"
        receiver_email = ["dannywong@kenanga.com.my"]
        # cc_emails = ["itklm@kenanga.com.my"]

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] =  ','.join(receiver_email)
        # message['Cc'] = ','.join(cc_emails)
        message["Subject"] = f"[Testing Email] BTX Start Of Day process monitoring {process_date_value} - checking @ 4.30am "

        # Add HTML table to the email body
        message.attach(MIMEText(html_content, "html"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("172.21.5.60", 25) as server:
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email successfully sent!")

        time.sleep(10)
        # driver.quit()
