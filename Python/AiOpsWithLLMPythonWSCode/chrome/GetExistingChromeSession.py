from selenium import webdriver


#debug port needs to be enabled to 9222 in chrome shortcut and an instance of that browser needs to be open  to connect to existign session
def GetDriver(url):
    # Chrome short cut modified  - "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
    # Set up Chrome options with the Debugger Address
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('debuggerAddress', 'localhost:9222')  # Use the IP and port where Chrome is listening

    print("starting chrome webdriver")

    # Initialize the WebDriver with the Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    print("got driver")

    # Now you can interact with the existing Chrome session
    driver.get(url)  # Interact with the existing session as needed

    print("Got url returning driver")
    return driver
