from libraries import *

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

        # The purpose of this function is to create a excel file
        create_excel_file(excel_file_path,combined_data,data1)

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

        # Modify the HTML table using the function
        modified_html_table = modify_html_table(html_table)

        body = generate_email_body(image1_base64,image2_base64)
  
        html_content = f"<p>Process Date: {process_date_value}</p>\n\n{modified_html_table}\n{body}"

        # Set up the email details
        sender_email = "danny-wong-02@hotmail.com"
        receiver_email = ["danny-wong-02@hotmail.com"]
        cc_emails = ["whysodamn2012@gmail.com"]

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] =  ','.join(receiver_email)
        message['Cc'] = ','.join(cc_emails)
        message["Subject"] = f"[Testing Email] BTX Start Of Day process monitoring {process_date_value} - checking @ 4.30am "

        # Add HTML table to the email body
        message.attach(MIMEText(html_content, "html"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("172.21.5.60", 25) as server:
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email successfully sent!")

        # time.sleep(10)
        # driver.quit()
