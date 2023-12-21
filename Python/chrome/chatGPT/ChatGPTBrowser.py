import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from chrome import GetExistingChromeSession

driver = GetExistingChromeSession.GetDriver("https://chat.openai.com/c/accf6fb5-9110-43b3-80a2-073a24b37aec")
time.sleep(5)


def inputRequest(request):
    # Define the chat input field and chat response element locators
    input_locator = (By.ID, "prompt-textarea")
    # Send a message to the chatbot
    input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(input_locator))
    modified_text = request.replace('\n', '')
    input_field.send_keys(modified_text)
    print("Sent keys to chatgpt about to submit")
    submit_locator = (By.XPATH, "//*[@id='__next']//*//form//button")
    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(submit_locator))
    submit_button.click()


def getResponse():
    # response
    response_locator = (By.XPATH, "//div[@data-message-author-role='assistant']")
    # Locate all elements that match the response locator
    response_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(response_locator))

    got_response = False
    # Get the last element from the list (the most recent response)
    time.sleep(5)
    while not got_response:
        if response_elements:
            last_response_element = response_elements[-1]
            chatbot_response = last_response_element.text
            if len(chatbot_response) > 0:
                got_response = True
                print("Last Chatbot Response:", chatbot_response)
                return chatbot_response

        else:
            print("No chatbot responses found")
            time.sleep(10)


def closeBrowser():
    driver.close()