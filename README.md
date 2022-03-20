# NTU Course Scraper

Script that scrapes courses for subjects I'm interested in from Nanyang Technological University's "Content of Courses" webpage using Selenium, so I don't have to click through all of them. You can edit the `KEYWORDS` list to include substrings (in all caps) of study programmes you're interested in.

Writes information to a file `ntu-courses.txt` by default when finished. You may need to run this script a few times in case the course data doesn't render in time and Selenium errors out.
