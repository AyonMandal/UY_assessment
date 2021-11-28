from appium import webdriver
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# SETTING UP THE DESIRED CAPABILITY

desired_caps = {'platformName': 'Android', 'platformVersion': '10', 'deviceName': 'Pixel',
                'app': '/path/to/UrbanYogi.apk', 'appPackage': 'com.capitalx.blissfully',
                'appActivity': 'ly.blissful.bliss.ui.ControllerActivity', 'noReset': True}

# TEST DATA
options = ['[1]', '[2]', '[3]', '[1]', '[2]']
test_ID = "XYZ"
email_ID = "XYZ@gmail.com"
invalid_email_id = "XYZgmail.com"
password_type = "ABCD123"

# Please note, I have used dummy selectors as my system was not able to handle AVD properly and it was crashing.
# And also I was not able to use my own phone as emulator due to Appium Inspector was showing session error.
# SELECTORS FOR FIRST PAGE
main_header = (By.ID, "heading")
sub_header = (By.ID, "sub-header")
start_journey_btn = (By.XPATH, "//button[contains(text(),'Start your journey')]")

# SELECTORS FOR LOADING PAGE
loader_header = (By.ID, "load_header")
loader_subheader = (By.ID, "load_subheader")

# SELECTORS FOR CONGRATULATIONS PAGE
congo_text_1 = (By.CSS_SELECTOR, "#some_id")
congo_text_2 = (By.CSS_SELECTOR, ".some_class_name")
do_it_btn = (By.XPATH, "//button[contains(text(),'Let's do it!')]")

# SELECTORS FOR QUESTION ANSWERS PAGE
back_arrow = (By.ID, "go-back")
top_bar = (By.ID, "top-bar")
selected_top_bar = (By.ID, "select-top-bar")
unselected_top_bar = (By.ID, "not-select-top-bar")
select_option = "//input[@type='radio']"
age_select = (By.XPATH, "//label[text()='20s']")
gender_select = (By.XPATH, "//label[text()='Male']")

# SELECTORS FOR LOADER AND WELL BEING SCORE
loader = (By.ID, "loading")
well_being_score_locator = (By.ID, "score")
next_btn = (By.ID, "continue")
well_being_text = (By.ID, "well-being-result")

# SELECTORS FO GOAL FOR THE WEEK
sleep_better = (By.ID, "sleep_better")
reduce_anx = (By.ID, "reduce_anxiety")
dev_grat = (By.ID, "develop-grat")
next_arrow = (By.ID, "next")

# SELECTORS FOR EMAIL, PASSWORD, CONTINUE BUTTON and START 7-DAY FREE TRIAL
email = (By.ID, "email")
password = (By.ID, "pwd")
userID = (By.ID, "username")
continue_btn = (By.ID, "continue")
Day_free_btn = (By.ID, "7-day-free")
cross_mark_btn = (By.ID, "cancel")
welcome = (By.ID, "welcome-message")
error_message = (By.ID, "error-span")

# TEST STARTS

# SETTING UP THE WEBDRIVER
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)

# 1) Wait until the landing page is loaded for maximum of 5secs
try:
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located(*main_header))
except NoSuchElementException:
    print('App did not rendered to landing page in 5 secs')

# 2) Once loaded, lets check the content of header and sub-header
header_text = driver.find_element(*main_header).text
sub_header_text = driver.find_element(*sub_header).text
assert header_text == "Feel more calm and sleep better"
assert sub_header_text == "Created by experts,Used by millions everyday!"

# 3) Click on start journey btn
driver.find_element(*start_journey_btn).click()

# 4) Verify the loading page has correct text
loader_header_text = driver.find_element(*loader_header).text
loader_subheader_text = driver.find_element(*loader_subheader).text
assert loader_header_text == "Take a deep breath!"
assert loader_subheader_text == "Loading..."

# 5) Waiting for 10 secs to load for Congratulations page(basically waiting for btn) is loaded
try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(*do_it_btn))
except NoSuchElementException:
    print('Congratulations page was not loaded in given timeout')

# 6) Verifying the text displayed in the page is as per expected
assert driver.find_element(*congo_text_1).text == "Congratulations! and some later text..."
assert driver.find_element(*congo_text_2).text == "Let's personalise the experience for you...."

# 7) Click on back button and verify user is re-directed to landing page of app
driver.find_element(*back_arrow).click()
try:
    driver.find_element(*start_journey_btn).click()
except NoSuchElementException:
    print('User was not re-directed to landing page')

# 8) Wait for Congratulations page and then we click on "Let's do it" button
try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(*do_it_btn))
except NoSuchElementException:
    print('Congratulations page was not loaded in given timeout')
driver.find_element(*do_it_btn).click()

# 9) Selecting random options for the MCQ's
# 9.a> taking the count of the top bar (blue color seperated bars).
# total count - 1 : is the number of MCQ's
# last page is for Age and Gender selection
pages = len(list(driver.find_elements(*top_bar)))
# iterating each page for selecting options
for page in range(0, pages - 1):
    # locator for a random option
    select_option = select_option + str(options[page])
    # verifying that the highlighted top bar is equal to page number
    assert page + 1 == len(list(driver.find_elements(*selected_top_bar)))
    # click the option selected
    driver.find_element(By.XPATH, select_option).click()

# 9.b> clicking on back button to come to first question
for page in range(0, pages - 1):
    driver.find_element(*back_arrow)

# 9.c> verify that the selection made persisted
for page in range(0, pages - 1):
    # locator for a random option
    select_option_1 = select_option + str(options[page])
    # verify that the same option remained selected
    assert driver.find_element(By.XPATH, select_option_1).is_selected()
    driver.find_element(By.XPATH, select_option_1).click()

# 10) Selecting age and sex
driver.find_element(*age_select).click()
driver.find_element(*gender_select).click()

# 11) Verifying loader is displayed and then comes the well-being score
assert driver.find_element(*loader).is_displayed()
try:
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located(*next_btn))
except NoSuchElementException:
    print('App did not rendered to landing page in 5 secs')

well_being_score = driver.find_element(*well_being_score_locator).text

if 0 < int(well_being_score) <= 35:
    expected_text = 'bad'
elif 30 < int(well_being_score) <= 75:
    expected_text = 'average'
else:
    expected_text = 'good'
assert expected_text in driver.find_element(*well_being_text).text
driver.find_element(*next_btn).click()

# 11) Select a goal and go for next
driver.find_element(*sleep_better).click()
driver.find_element(*next_arrow).click()

# 12) Populate mail, pwd and select continue. Wait for the 7-day trail btn appears
# cancel the page and verify the username is displayed in "Good Morning" message
# 12.a> Only FirstName is populated and users try to sign in, error is displayed
driver.find_element(*userID).send_keys(test_ID)
driver.find_element(*continue_btn).click()
assert driver.find_element(*error_message).is_displayed()

# 12.b> Invalid Email is populated and validated
driver.find_element(*email).send_keys(invalid_email_id)
driver.find_element(*continue_btn).click()
assert driver.find_element(*error_message).is_displayed()

# 12.c> Only First Name and Email is populated
driver.find_element(*email).send_keys(email_ID)
driver.find_element(*continue_btn).click()
assert driver.find_element(*error_message).is_displayed()

# 12.d > Valid data is populated in every field
driver.find_element(*password).send_keys(password_type)
driver.find_element(*continue_btn).click()
# waiting for the 7-day trail button to appear
try:
    wait = WebDriverWait(driver, 8)
    wait.until(EC.visibility_of_element_located(*Day_free_btn))
except NoSuchElementException:
    print("Timeout reached!")
driver.find_element(*Day_free_btn).click()
assert test_ID in driver.find_element(*welcome).text
