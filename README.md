My Final Year Project for University of Surrey. At the current moment, I am developing a skeleton  web-page that is meant to replicate Surreylearn. 

The project is focused on "Exploring the use of a real time chat interface in Surreylearn"

In response to the reliance of third-party communication applications such as Outlook and Microsoft Teams at the University of Surrey, this project proposes the integration of a real-time chat interface within SurreyLearn. There is support of a basic messaging and emailing system which is overlooked by many who use SurreyLearn and thus my project will explore how the implementation of the chat interface could be integrated into SurreyLearn, it is expected to enhance the educational experience at SurreyLearn by improving accessibility, responsiveness and engagement in the online learning environment.

# Requirements
[Node.js]
[Django]
[MySQL]

# If coming from GitHub
git clone https://github.com/JulianMartin121/Final-Year-Project.git

# Install Node.js packages
Make sure your directory is set to FYPApp at the first level (ie. Final Year Project\FYPApp)

in console do:
```sh
npm install
```

# Install python packages
Make sure you are in the FYPApp directory at first level
```sh
pip install -r requirements.txt
```

# Set up MySQL database
Create an MySQL database for the project. In the submission, there will be a MySQL dump with the data and tables named 'fypdatabase.sql'

I personally used MySQL workbench to create a connection for the server side.

IMPORTANT: If you are using MySQL Workbench, create your own server as mentioned, go to Server which is found in the tabs (where file, edit, view etc. is) and press Data Import.
You should select "Import from Self-Contained File" and select the 'fypdatabase.sql'

You will need to adjust .env file to fit your MySQL database. Both Django settings.py and Node server.js should already contain the necessary functions to get the .env names

If you don't have a .env file (if you cloned from git for example) make one at the FYPApp first level.

Things you will need to change in the .env file to whatever you are using
```env
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

# Run Migrations
To set up the tables:
```sh
py manage.py migrate
```

You may also need to run this command below beforehand
```sh
py manage.py makemigrations
``` 



## Running the project

Open two consoles that is at the FYPApp level

# Start the Express/Node.js server
In the first console
```sh
node server.js
```

This command starts up the Express/Node.js server

# Start the Django Web Server
In the second console
```sh
py manage.py runserver
```

This command should start the Django web server.