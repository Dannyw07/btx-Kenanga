from libraries import *
import one

class BTX:
    
    def login(self,driver):
        # Make selenium to automate the login process (username,password,login button)
        username_input = driver.find_element(By.ID, 'ctl00_cntPlcHldrContent_txtUsrID')
        password_input = driver.find_element(By.ID, 'ctl00_cntPlcHldrContent_txtUsrPwd')
        submit_button = driver.find_element(By.ID,'ctl00_cntPlcHldrContent_ibSignIn')

        username_input.send_keys('ITHQOPR')
        password_input.send_keys('Kibb8888')
        submit_button.click()

    # Define a function for navigating to a specific page
    def navigate_to_page(self,driver, url, xpath):
        driver.get(url)
        time.sleep(2)
        driver.maximize_window()
        time.sleep(2)
        element = driver.find_element(By.XPATH, xpath)
        element.click()
        time.sleep(2)

    # Define a function for selecting options from dropdown and performing actions
    def select_dropdown_option(self,driver, id, value):
        select = Select(driver.find_element(By.ID, id))
        select.select_by_value(value)
        time.sleep(2)

    # Define a function for entering date and performing search
    def enter_date_and_search(self,driver, id, date):
        datepicker_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id)))
        datepicker_input.clear()
        datepicker_input.send_keys(date.strftime('%d/%m/%Y'))
        time.sleep(2)
        search_button = driver.find_element(By.ID, "ctl00_cntPlcHldrContent_btnTpltUpdate_btnSearch")
        search_button.click()
        time.sleep(2)
    
    def update_message(self, message):
        # Update the message label text
        self.outputMsg.config(text=message)

    def is_internet_available(self):
        try:
            # Attempt to make a requet to google
            response = requests.get("http://www.google.com",timeout=5)
            response.raise_for_status()
            print("Internet connection is available.")
            return True
        except requests.RequestException as e:
            print("No internet connection. Error:", str(e))
            return False

    def handle_SocketError(self):
       try:
            # Check for internet connection
            if not self.is_internet_available():
                self.button_Disabled()
                print("No internet connection.")
                # Display a dialog box with the message
                messagebox.showinfo("Network Error Detected", "No internet connection. Please exit the program and configure your network.")

                return False
            return True
       except Exception as e:
                # Log other exceptions, if any
                print(f"Error in handle_SocketError: {str(e)}")
                return False

    def start_program(self):
        
        # Disable the Start and Stop buttons
        self.startBtn["state"] = tk.DISABLED
        self.endBtn["state"] = tk.DISABLED

        # Set the running flag to True
        self.running = True
        
        # Start the program in a separate thread
        self.program_thread = Thread(target=self.run_program)
        self.program_thread.start()

    def stop_program(self):

        # Set the running flag to False to stop the loop
        self.running = False
        print("The program stopped the checking process")
        self.update_message("The program stopped the checking process")
        self.outputMsg.after(2000, lambda: self.update_message("Ready"))
        # Additional cleanup tasks if needed
        self.startBtn["state"] = tk.NORMAL

    def run_program(self):

        # Enable the Stop button
        self.endBtn["state"] = tk.NORMAL
        print("The program started the checking process")
    
        # Check for socket error before proceeding
        if not self.handle_SocketError():
            self.startBtn["state"] = tk.NORMAL
            return
        
        # Initialize a flag to track if email has been sent for 4:30 am
        email_sent_430am = False
        # Initialize a flag to track if email has been sent for 5:45 am
        email_sent_545am = False
        # Initialize a flag to track if email has been sent for 6:30 am
        email_sent_630am = False
        # Initialize a flag to track if email has been sent for 7:00 am
        email_sent_700am = False

        # Keep running until the user presses the Stop button or the program stops
        while self.running:
            driver = webdriver.Chrome()
            current_time = datetime.datetime.now().time()
            try:
                # Login to BTX website page
                self.login(driver)

                # Step 2: Navigate to page
                self.navigate_to_page(driver, 'https://btx.kenanga.com.my/btxadmin/default.aspx', "//img[@src='/btxadmin/images/demo/icons/i_dayEndM_off.jpg']")

                # Step 3: Perform actions on page
                second_url = driver.current_url
                print("Second URL:", second_url)

                for xpath in ["//img[@src='/btxadmin/images/demo/icons/i_dayEndE_on.jpg']", "//img[@src='/btxadmin/images/demo/icons/i_dayEndE_off.jpg']"]:
                    try:
                        dayEndEnquiry_image = driver.find_element(By.XPATH, xpath)
                        dayEndEnquiry_image.click()
                        break
                    except NoSuchElementException:
                        continue

                third_url = driver.current_url
                print("Third URL:", third_url)

                self.select_dropdown_option(driver, "ctl00_cntPlcHldrContent_selEODEnquiry", "1,S")

                # Choose date 
                yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
                self.enter_date_and_search(driver, "ctl00_cntPlcHldrContent_txtDate", yesterday)

                # Step 4: Switch to new window and perform actions
                new_window = driver.window_handles[1]
                driver.switch_to.window(new_window)
                
                # The new window get maximize
                driver.maximize_window()

                fifth_url = driver.current_url
                print("Fifth URL:", fifth_url)

                process_dates = driver.find_elements(By.XPATH, "//table[@class='clsTable']/tbody/tr[2]/td[@id='tdBG']/span")
                for process in process_dates:
                    print(process.text)

                # driver.get(fifth_url)
                html_content_fifth_url = driver.page_source

                # Call the function in one.py and pass html_content_fifth_url
                one.process_html_content(html_content_fifth_url)
            finally:
                driver.quit()
            
        # Enable the Start button after stopping
        self.startBtn["state"] = tk.NORMAL
 
    def setup_gui(self):
        # Create a notebook (tabbed interface)
        self.tabControl = tb.Notebook(self.master)
        self.tabControl.pack(expand=True, fill='both')

        self.tab1 = tb.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Main')

        frame4 = tk.Frame(self.tab1, borderwidth=2)
        frame4.pack(side="top", padx=10, pady=30)
        self.outputMsg = tk.Label(frame4, text="")
        self.outputMsg.pack(padx=10)

        frame5 = tk.Frame(self.tab1, borderwidth=2)
        frame5.pack(side="top", padx=30)
        my_style = tb.Style()
        my_style.configure('success.TButton', font=("Helvetica", 18))
        my_style.configure('danger.TButton', font=("Helvetica", 18))

        self.startBtn = tb.Button(frame5, text="Start", 
            command=self.start_program,
            bootstyle="success",
            style="success.Tbutton",
            width=10)
        self.startBtn.pack(pady=40)

        frame6 = tk.Frame(self.tab1, borderwidth=2)
        frame6.pack(side="top", padx=10, pady=30)
        self.displayMsg = tk.Label(frame6, text="")
        self.displayMsg.pack(padx=10)

        self.endBtn = tb.Button(frame5, text="End", 
            command=self.stop_program,
            bootstyle="danger",
            style="danger.Tbutton",
            width=10)
        self.endBtn.pack(pady=0)

        self.footer_label = tk.Label(self.master, text="Danny Wong Jia Hong © 2024  ", bd=1, anchor=tk.W)
        self.footer_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.width_limit = 350
        self.height_limit = 400
        self.master.geometry(f"{self.width_limit}x{self.height_limit}")


    def __init__(self, master):
        self.master = master
        self.master.title("BTX Email Monitoring")
        self.setup_gui()
        self.master.bind("<Configure>", self.check_resize)
 

    def check_resize(self, event):
        current_width = self.master.winfo_width()
        current_height = self.master.winfo_height()

        # Check if the width exceeds the limit
        if current_width > self.width_limit:
            self.master.geometry(f"{self.width_limit}x{current_height}")

        # Check if the height exceeds the limit
        if current_height > self.height_limit:
            self.master.geometry(f"{current_width}x{self.height_limit}")


if __name__ == "__main__":
    root = tb.Window(themename="cosmo")
    app = BTX(root)
    root.mainloop()
