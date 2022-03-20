''' Scrapes some NTU courses to find interesting ones! '''

import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.firefox import GeckoDriverManager

# Define some scraping constants
URL = 'https://wis.ntu.edu.sg/webexe/owa/aus_subj_cont.main'
SEMESTER_TERM = '2021_2'

DROPDOWN_WAIT = 2.5
EXIT_WAIT = 4
KEYWORDS = ['COMPUTER SCIENCE', 'DATA SCIENCE', 'MATH']

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.get(URL)

semester_select = Select(driver.find_element(by=By.NAME, value='acadsem'))

# select academic term by value 
semester_select.select_by_value(SEMESTER_TERM)

# select subject/year by value
subject_select = Select(driver.find_element(by=By.NAME, value='r_course_yr'))

all_subjects = [option.text for option in subject_select.options]
relevant_subjects = [subject for subject in all_subjects if any(kw in subject.upper() for kw in KEYWORDS)]

class CourseInfo:
    ''' Course WebElement parsed into its fields. '''
    def __init__(self, course_web_element):
        course_data = course_web_element.find_elements(by=By.TAG_NAME, value='tr')
        heading_data = course_data[0].find_elements(by=By.TAG_NAME, value='td')
        self.code = heading_data[0].text
        self.title = heading_data[1].text
        self.credits = heading_data[2].text
        self.description = course_data[-1].text
        self.subjects = set()

courses_of_interest = dict()

for i, subject in enumerate(relevant_subjects):
    print(f'Scraping {subject}... {i + 1}/{len(relevant_subjects)}')
    subject_select.select_by_visible_text(subject)
    
    # click button to render course catalog for this subject
    load_courses = driver.find_element(by=By.XPATH, value='//input[@value="Load Content of Course(s)"]')
    load_courses.click()
    catalog = driver.find_element(by=By.XPATH, value='//iframe[@name="subjects"]')
    
    # switch the webdriver object to the iframe.
    driver.switch_to.frame(catalog)

    # add the course data in
    time.sleep(DROPDOWN_WAIT)
    courses = map(CourseInfo, driver.find_elements(by=By.TAG_NAME, value='table'))
    for course in courses:
        if course.code not in courses_of_interest:
            courses_of_interest[course.code] = course
        courses_of_interest[course.code].subjects.add(subject)
    
    # remember to switch back
    driver.switch_to.default_content()

time.sleep(EXIT_WAIT)
driver.quit()

# Write the data to a TXT
course_file = open('ntu-courses.txt', 'w')

for code in sorted(courses_of_interest.keys()):
    course = courses_of_interest[code]
    course_file.write(f'===== {course.code} {course.title} {course.credits} =====\n')
    course_file.write(course.description + '\n')
    course_file.write('In programmes: ' + ', '.join(course.subjects) + '\n\n')

print('Done!')
course_file.close()