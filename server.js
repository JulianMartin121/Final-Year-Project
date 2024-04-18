const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const mysql = require('mysql');
const cors = require('cors');
require('dotenv').config();

const app = express();
const server = http.createServer(app);

app.use(cors());

const io = socketIo(server, {
  cors: {
    origin: "*",  // Allow requests from any origin
    methods: ["GET", "POST"],  // Allow these HTTP methods
    allowedHeaders: ["my-custom-header"],  // Allow these custom headers
    credentials: true  // Allow cookies
  }
});

app.use(express.static('homepage/templates/homepage'));

let teachers = [];
let teacherAssignments = {};

// Connect to the SQLite database and fetch teachers
let db = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    multipleStatements: true
});

console.log("Connected to the database.");

db.query('SELECT * FROM accounts_customuser WHERE user_type = "teacher"', (err, results) => {
    if (err){
        console.error(err.message);
        return;
    }

    for (let row of results){
        teachers.push({
            id: row.Uni_ID,
            chats: []
        });
    }

    console.log(teachers);
    console.log('Number of teachers:', teachers.length);
});


io.on('connection', (socket) => {
    console.log('a user connected');
    // Assign the student to a teacher with the least chats when they send the first message
    if (!socket.teacher){
        console.log('Assigning teacher to student');
        const teacher = teachers.sort((a, b) => a.chats.length - b.chats.length)[0];
        teacher.chats.push(socket);
        socket.teacher = teacher;

        // Store the teacher assigned to the student
        teacherAssignments[socket.id] = teacher.id;
        console.log('Assigned teacher id:', teacher.id)
    }

    socket.on('open chat room', (studentID) => {
        if(teacherAssignments[studentID] == socket.teacher.id){
            db.query('SELECT * FROM chat_logs WHERE lectureNumber = ? ORDER BY timestamp DESC', [studentID], (err, results) => {
                if (err){
                    console.error(err.message);
                    return;
                }
                socket.emit('chat history', results);
            });
        }
    });

    // Broadcast the message to the teacher and student
    socket.on('chat message', (msg) => {
        console.log("Message received: ", msg.text);
        console.log("Chat message: ", msg);

        msg.receiver = socket.teacher.id;

        // Fetch the username from the database
        const queryUSER = 'SELECT username FROM accounts_customuser WHERE Uni_ID = ?';
        db.query(queryUSER, [msg.sender], (error, results) => {
            if (error){
                console.error(error.message);
                return;
            }

            msg.text = results[0].username + ': ' + msg.text;

            io.to(socket.teacher.id).emit('chat message', msg);
            socket.emit('chat message', msg);
        });

        // Insert the message into chat logs
        const query = 'INSERT INTO chat_logs (lectureNumber, message, timestamp) VALUES (?, ?, ?)';
        const params = [msg.lectureNumber, msg.text, new Date()];
        db.query(query, params, (err, results) => {
            if (err){
                console.error(err.message);
                return;
            }
            console.log('Message inserted into chat logs');
        });
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');

        // Remove the connection from the teacher's list of chats
        if (socket.teacher){
            const index = socket.teacher.chats.indexOf(socket);
            if (index > -1){
                socket.teacher.chats.splice(index, 1);
            
            }
        }
    });
});

// Create a new endpoint to get the teacher assigned to a student
app.get('/teacher_assignment', (req, res) => {
    const chatId = req.query.chatId;
    console.log(`Chat ID: ${chatId}`);
    const teacherId = teacherAssignments[chatId];
    console.log(`Teacher ID: ${teacherId}`);
    res.json({ teacherId });
});

app.use(express.json());

app.post('/new_user', (req, res) => {
    const user = req.body;
    console.log(user);  // Log the user data to the console
    res.status(200).send('User data received');
});

app.get('/chat_logs', (req, res) => {
    const lectureNumber = req.query.lectureNumber;
    console.log(`Lecture Number: ${lectureNumber}`);

    db.getConnection((err, connection) => {
        if (err){
            console.error(err.message);
            return;
        }

        connection.query('SELECT * FROM chat_logs WHERE lectureNumber = ? ORDER BY timestamp ASC', [lectureNumber], (err, results) => {
            connection.release();
            if (err){
                console.error(err.message);
                return;
            }

            res.json(results);
        });

    });
});

app.get('/students', (req, res) => {
    db.query('SELECT * FROM accounts_customuser WHERE user_type = "student"', (err, results) => {
        if (err){
            console.error(err.message);
            return;
        }

        res.json(results);
    });
});

app.get('/user_type', (req, res) => {
    const uniID = req.session.Uni_ID;
    console.log(`Uni ID: ${uniID}`);

    db.query('SELECT user_type FROM accounts_customuser WHERE Uni_ID = ?', [uniID], (err, results) => {
        if (err){
            console.error(err.message);
            return;
        }

        res.json(results[0].user_type);
    });
});


server.listen(3000, () => {
    console.log('listening on *:3000');
});