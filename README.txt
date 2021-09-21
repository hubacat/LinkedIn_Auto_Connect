--------------------------------------------------------------------
GOAL:
--------------------------------------------------------------------
This program takes a list of students from a specified university,
and sends them a Connection request with a personalized message.


--------------------------------------------------------------------
HOW TO USE:
--------------------------------------------------------------------
i) Download this repo.

1) Download the chromium webdriver and establish a PATH to it (It can 
	be found in this repo in selenium_drivers.)git .

2) Create/Extract your classmates' names into a .xlsx (or compatible format) file.
For the program to work as intended, the name must include at least a first and a last name.
Middle names are considered as last names and a a maximum of 4 words per name can be used.

Ex.: "Marius Baboushka Jacob" is a name with 3 words.

Ex.: Using a webscraping tool like octoparse (free, GUI, and easy to use), create a
	a task to extract all your classmates' names from your School's portal (Moodle).
	
3) Transfer (must be unformated paste) your classmates' names into the data.xlsx 
file under 'NAMES', and add the word 'done' at the end of the list.

4) In bot.py, modify lines 27-30 with your respective information. The USERNAME, 
PASSWORD, and SCHOOL_NAME variables must be entered for the program to work as intended.

5) Run the bot.py program.
-The program will sign into your LinkedIn profile, so you'll be notified to complete your potential two-step authentification, and then press ENTER into the console.

6) Finally, I suggest using the monitor.txt file to verify which connections where successful and unsuccessful. 
*Unsuccessful connections can be due to two things, either your classmate doesn't have a LinkedIn profile, or the program didn't found him.
*Successful connection can be a false-positive, a connection was made but with the wrong profile (estimation of this occuring: XXX% from a 400 student sample)
