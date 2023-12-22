from chrome import GetExistingChromeSession
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#your existing bard session
driver = GetExistingChromeSession.GetDriver("https://bard.google.com/chat/b0358e2be759b2fe")
time.sleep(5)


def inputRequest(request):
    # Define the chat input field and chat response element locators
    input_locator = (By.XPATH, "//*/rich-textarea/div[1]")
    # Send a message to the chatbot
    input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(input_locator))
    modified_text = request.replace('\n', '  ')
    print("About to send keys ")
    input_field.send_keys(modified_text)
    #print(" Here modified text : " , modified_text)
    #print("Sent keys to chatgpt about to submit")
    submit_locator = (By.XPATH, "//*/input-area/div/div[2]/button/span[3]")
    print("Locating submit button ")
    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(submit_locator))
    submit_button.click()
    time.sleep(8)


def getResponse():
    # response
    response_locator = (By.XPATH, "//div/message-content")
    # Locate all elements that match the response locator
    response_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(response_locator))

    got_response = False
    # Get the last element from the list (the most recent response)
    #time.sleep(2)
    while not got_response:
        if response_elements:
            last_response_element = response_elements[-1]
            chatbot_response = last_response_element.text
            if len(chatbot_response) > 0:
                got_response = True
                #print("Last Chatbot Response:", chatbot_response)
                return chatbot_response

        else:
            print("No chatbot responses found")
            time.sleep(10)


def closeBrowser():
    driver.close()