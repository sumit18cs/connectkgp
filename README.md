# Connect KGP
## Connect KGP is a web-based application to provide Educational resources to the college community.

![**Slideshow**](/Slideshow.gif)

# Overview
 - Developed a web-based application using Flask framework to provide educational resources to the college community.
 - Designed Graphical User Interface for a signup, login, homepage, chat window, and discussion forum.
 - Created SQLAlchemy database and tables to store user personal details, their skills, messages, and their posts.
 - Implemented followers-based search and skill-based trending on the home page.
 - Hosted the web application at Heroku (Cloud-based Application Platform) (Link: https://kgpconnect.herokuapp.com)

# Features 
 - **Search and Personalized dashboard:** It provides a platform to write about all the technical skills that you have and if anybody wants to learn new skills they simply search that skill and get to know about all the resources and material needed for learning that skill.  
 - **Doubts and Disussion:** Users can post their doubts in the doubt/discussion area and all users can have a discussion on that topic using the comments section given on doubt page and come up with a simplified solution. The discussion area is mainly focused to share the different ideas of the users on any topic so that the whole college community can understand that topic in the best possible way. 
 - **Job and Internship:** It will allow users to post internship/part-time job opportunities. This feature is basically for the alums. It provides the alums to hire for an intern or a part-time job among the students of his/her college. Similar to doubt/discussion, here also there is a comment section where different users can share their views.
 - **Collaboration:** This feature can be used by any users who want to share their project idea(or need a group of people on any particular domain) and get to know whether some fellow students are interested in collaborating and work together on that project idea. Similar to doubt/discussion, here also there is a comment section where different users can share their views.
 - **End to end messages:** There is an option to send any private message to any user if you need any help from that user but you are only allowed to send a message if both the sender and the recipient user are selected 'YES' to receive messages from another user.

# Softwares and Libraries Used:
 - Python 
 - Flask  
 - HTML5 
 - CSS3 
 - SQLAlchemy 
 - Javascript
 - Bootstrap
 - Bcrypt
 - Flask-mail

# Steps to Run it locally:
I am using Ubuntu 16.04 LTS and python version needed for this software is minimum 3.61. Open Terminal and install python virtual environment using the below mentioned code:python3 -m venv newwhere, ‘new’ is the virtual environment name.2. Go to above created virtual environment directory and start virtual environment:  cd newsource bin/activate3.  Now their is a folder name “kgp” in the submitted ZIP file. Copy paste this folder into the “new”folder which is created earlier.4. Go inside this foldercd kgp5. Now write the below code in terminal and make sure your internet is working properly otherwise their is an error. Reuirements.txt contain all the dependencies required for this software.pip install -r requirements.txt6. Everything is done now start applicaionpython app.pyNow, there is a link in the terminal just open link in the browser.(ie, local host link)
- Ubuntu 16.04 LTS (Make sure you have Python 3.6 or higher installed on your system to run the application)
1.  First download the zipped folder and then unzip it
2.  Install python virtual environment using the below mentioned code: `python3 -m venv new`, new is the virtual environment name
3.  Go to above created virtual environment directory and start virtual environment:  `cd new`  `source bin/activate`
4.  Navigate to the folder where you have unzipped it and enter that directory
5.  Now type the following to install all the dependencies:
   `pip install -r requirements.txt` 
6.  Now finally run:
   `python application.py`


## Prerequisites
Make sure you have Python 3.6 or higher installed on your system to run the application. 
- (Window)
Also install venv library to install the dependencies in a virtual environment using the command:
pip install venv

## Steps:

1. First download the zipped folder Code.zip and then unzip it. 
2. Open a Command Prompt/Terminal and navigate to the folder where you have unzipped it and enter that directory.
3. Create a virtual environment using the following commands:
   `virtualenv  t4sne`
4. Then to activate the environment type:
   For windows:
   `t4sne\Scrips\activate`

   For Mac/Linux:
   `source t4sne/bin/activate`
   Now type the following to install all the dependencies:
   `pip install -r requirements.txt` 
   Wait for it to install everything.
5. Next type:
   `pipwin install pyaudio`
6. Now finally run:
   `python application.py`

Finally, open any browser and type in localhost:5000 or 127.0.0.1:500
