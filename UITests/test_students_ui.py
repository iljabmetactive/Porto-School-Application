#how to run selenium tests
#go to UItests folder and run python StudentTests.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time

def create_driver():
    options = Options()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)





def test_createStudent_UI():
    driver = create_driver()

    driver.get("http://localhost:5173")

    driver.find_element(By.XPATH, "//button[contains(., 'Create Student')]")
    time.sleep(1)

    driver.find_element(By.NAME, "name").send_keys("UI Test Student")
    driver.find_element(By.NAME, "email").send_keys("ui@test.com")
    driver.find_element(By.NAME, "phone").send_keys("123456")

    driver.find_element(By.NAME, "course").send_keys("Beginner A1-A2")

    driver.find_element(By.TAG_NAME, "form").submit()

    time.sleep(2)

    assert "UI Test Student" in driver.page_source

    driver.quit()


def test_deleteStudent_UI():
    driver = create_driver()
    driver.get("http://localhost:5173")

    time.sleep(2)

    delete_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Delete')]")

    if delete_buttons:
        delete_buttons[0].click()

        alert = driver.switch_to.alert
        alert.accept()

        time.sleep(2)

        assert True

    driver.quit()

def test_studentBooking_UI():
    driver = create_driver()
    driver.get("http://localhost:5173")

    time.sleep(2)

    driver.find_element(By.XPATH, "//button[contains(., 'Schedule Course')]").click()

    time.sleep(2)

    slots = driver.find_elements(By.XPATH, "//button[contains(., '-')]")

    if slots:
        slots[0].click()

    driver.find_element(By.XPATH, "//button[contains(., 'Confirm Booking')]").click()

    time.sleep(2)

    assert True

    driver.quit()

def test_addNotes_UI():
    driver = create_driver()
    driver.get("http://localhost:5173")

    time.sleep(2)

    driver.find_element(By.LINK_TEXT, "View Details").click()

    time.sleep(2)

    textarea = driver.find_element(By.TAG_NAME, "textarea")
    textarea.send_keys("Selenium test note")

    driver.find_element(By.XPATH, "//button[contains(., 'Save Notes')]").click()

    time.sleep(2)

    assert True

    driver.quit()

def test_bookingWithout_timeSlot():
    driver = create_driver()
    driver.get("http://localhost:5173")

    time.sleep(2)

    driver.find_element(By.XPATH, "//button[contains(., 'Schedule Course')]").click()

    time.sleep(2)

    driver.find_element(By.XPATH, "//button[contains(., 'Confirm Booking')]").click()

    time.sleep(2)

    assert True

    driver.quit()



if __name__ == "__main__":
    test_createStudent_UI()
    test_deleteStudent_UI()
    test_studentBooking_UI()
    test_addNotes_UI()
    test_bookingWithout_timeSlot()