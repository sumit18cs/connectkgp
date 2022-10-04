# Connect KGP
## Connect KGP is a one-stop platform where students get all the information they need, right from academics to placements. It’s designed to cater to every career path and skill and can be helpful for people looking for the right resources. It essentially is a social media platform. Only the media here is all things academics.

![**Slideshow**](/Slideshow.gif)

# Overview
 - Developed a web-based application using Flask framework to provide educational resources to the college community.
 - Designed Graphical User Interface for a signup, login, homepage, chat window, and discussion forum.
 - Created SQLAlchemy database and tables to store user personal details, their skills, messages, and their posts.
 - Implemented followers-based search and skill-based trending on the home page.
 - Hosted the web application at Heroku (Cloud-based Application Platform) (Link: https://kgpconnect.herokuapp.com)

# Features 
 - **Search and Personalized dashboard:** It provides a platform to write about all the required technical skills that you have and if anybody wants to learn new skills they simply search that skill and get to know about all the resources and material needed for learning that skill. Get curated resources on any skill that you want to learn.
 -  **CDC Diaries:** A compendium of interview experience and tips that make it easier for students to prepare before an interview.
 - **Doubts and Disussion:** Users can post their doubts in the doubt/discussion area and all users can have a discussion on that topic using the comments section given on doubt page and come up with a simplified solution. The discussion area is mainly focused to share the different ideas of the users on any topic so that the whole college community can understand that topic in the best possible way. 
 - **Job and Internship:** It will allow users to post internship/part-time job opportunities. This feature is basically for the alums. It provides the alums to hire for an intern or a part-time job among the students of his/her college. Similar to doubt/discussion, here also there is a comment section where different users can share their views.
 - **Collaboration:** This feature can be used by any users who want to share their project idea(or need a group of people on any particular domain) and get to know whether some fellow students are interested in collaborating and work together on that project idea. Similar to doubt/discussion, here also there is a comment section where different users can share their views.
 - **End to end messages:** There is an option to send any private message to any user if you need any help from that user but you are only allowed to send a message if both the sender and the recipient user are selected 'YES' to receive messages from another user.

# Softwares and Libraries Used
 - Python 
 - Flask  
 - HTML5 
 - CSS3 
 - SQLAlchemy 
 - Javascript
 - Bootstrap
 - Bcrypt
 - Flask-mail

# Steps to Run it locally

## Prerequisites
Make sure you have Python 3.6 or higher installed on your system to run the application. 

## Steps:

- **Ubuntu 16.04 LTS**
1.  First download the zipped folder and then unzip it
2.  Install python virtual environment using the below mentioned code: `python3 -m venv new`, new is the virtual environment name
3.  Go to above created virtual environment directory and start virtual environment:  `cd new`  `source bin/activate`
4.  Navigate to the folder where you have unzipped it and enter that directory
5.  Now type the following to install all the dependencies: `pip install -r requirements.txt` 
6.  Now finally run: `python application.py`

- **Windows 10**
1.  Install venv library to install the dependencies in a virtual environment using the command:   `pip install venv`
2.  Download the zipped folder and then unzip it
3.  Open a Command Prompt and navigate to the folder where you have unzipped it and enter that directory
4.  Create a virtual environment using the following commands:   `virtualenv  kgp`
5.  Activate the environment:   `kgp\Scrips\activate`
6.  Now type the following to install all the dependencies:  `pip install -r requirements.txt` 
7.  Now finally run:  `python application.py`


**Finally, open any browser and type in localhost:5000 or 127.0.0.1:500**
