from libraries import *

class BTX:
    
    def login(driver):
        # Make selenium to automate the login process (username,password,login button)
        username_input = driver.find_element(By.ID, 'ctl00_cntPlcHldrContent_txtUsrID')
        password_input = driver.find_element(By.ID, 'ctl00_cntPlcHldrContent_txtUsrPwd')
        submit_button = driver.find_element(By.ID,'ctl00_cntPlcHldrContent_ibSignIn')

        username_input.send_keys('ITHQOPR')
        password_input.send_keys('Kibb8888')
        submit_button.click()

    # Define a function for navigating to a specific page
    def navigate_to_page(driver, url, xpath):
        driver.get(url)
        time.sleep(2)
        driver.maximize_window()
        time.sleep(2)
        element = driver.find_element(By.XPATH, xpath)
        element.click()
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
                login(driver)

                # Step 2: Navigate to page
                navigate_to_page(driver, 'https://btx.kenanga.com.my/btxadmin/default.aspx', "//img[@src='/btxadmin/images/demo/icons/i_dayEndM_off.jpg']")
                
                # Check if it's 4:30 AM
                if current_time.hour == 10 and current_time.minute == 30:
                    # Check if email has already been sent
                    if not email_sent_430am:
                        subprocess.run(["python", "one.py"])
                        messagebox.showinfo("Processing Ended", "Processing for 10:30 AM has ended.")
                        # Set email_sent flag to True to prevent sending multiple emails
                        email_sent_430am = True
                else:
                    # Reset email_sent_430am if the time is not 4:30 AM
                    email_sent_430am = False
                
                # Check if it's 5:45 AM
                if current_time.hour == 11 and current_time.minute == 10:
                    # Check if email for 5:45 AM has already been sent
                    if not email_sent_545am:
                        subprocess.run(["python", "two.py"])
                        messagebox.showinfo("Processing Ended", "Processing for 11:10 AM has ended.")
                        email_sent_545am = True
                else:
                    # Reset email_sent_545am if the time is not 5:45 AM
                    email_sent_545am = False

                # Check if it's 6:30 AM
                if current_time.hour == 12 and current_time.minute == 10:
                    # Check if email for 6:30 AM has already been sent
                    if not email_sent_630am:
                        subprocess.run(["python", "three.py"])
                        messagebox.showinfo("Processing Ended", "Processing for 12:10 PM has ended.")
                        email_sent_630am = True
                else:
                    # Reset email_sent_545am if the time is not 5:45 AM
                    email_sent_630am = False

                # Check if it's 7:00 AM
                if current_time.hour == 13 and current_time.minute == 1:
                    # Check if email for 7:00 AM has already been sent
                    if not email_sent_700am:
                        subprocess.run(["python", "four.py"])
                        messagebox.showinfo("Processing Ended", "Processing for 1:01 PM has ended.")
                        email_sent_700am = True
                else:
                    # Reset email_sent_700am if the time is not 7:00 AM
                    email_sent_700am = False

                print('waiting...')
                self.update_message('Waiting...')
                # If neither of the conditions are met, wait for 5 seconds
                time.sleep(5)
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
