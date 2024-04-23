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

    let userUniID;

    socket.on('User Login', (Uni_ID) => {
        userUniID = Uni_ID;
        console.log('User Uni ID:', userUniID);

        // Fetch the user type from the database
        db.query('SELECT user_type FROM accounts_customuser WHERE Uni_ID = ?', [userUniID], (err, results) => {
            if (err){
                console.error(err.message);
                return;
            }

            const userType = results[0].user_type;

            if(userType === 'student'){
                db.query('SELECT teacher_id FROM teacher_assignments WHERE student_id = ?', [userUniID], (err, results) => {
                    if (err){
                        console.error(err.message);
                        return;
                    }

                    if(results.length > 0){
                        console.log('Student already assigned to teacher')
                        const teacherId = results[0].teacher_id;
                        const teacher = teachers.find(teacher => teacher.id === teacherId);
                        teacher.chats.push(socket);
                        socket.teacher = teacher;
                    }else{
                        console.log('Assigning teacher to student');
                        const teacher = teachers.sort((a, b) => a.chats.length - b.chats.length)[0];
                        teacher.chats.push(socket);
                        socket.teacher = teacher;

                        db.query('INSERT INTO teacher_assignments (teacher_id, student_id) VALUES (?, ?)', [teacher.id, userUniID], (err, results) => {
                            if (err){
                                console.error(err.message);
                                return;
                            }
                            console.log('Teacher assigned to student');
                        });
                    }
                });
            }
        });
    });


    // Fetch the chat history between the teacher and student
    socket.on('open chat room', (studentID) => {
        console.log('Opening chat room before if statement')
        console.log('Student ID: ', studentID);
        db.query('SELECT teacher_id FROM teacher_assignments WHERE student_id = ?', [studentID], (err, results) => {
            if (err){
                console.error('Error Message in chat room: ', err.message);
                return;
            }
            if(results[0].teacher_id == socket.teacher.id){
                console.log('if statement');
                console.log('Student ID: ', studentID);
                console.log('Teacher ID: ', socket.teacher.id);
                db.query('SELECT * FROM homepage_message WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?) ORDER BY timestamp DESC', [studentID, socket.teacher.id, socket.teacher.id, studentID], (err, results) => {
                    if (err){
                        console.error(err.message);
                        return;
                    }
                    socket.emit('chat history', results);
                });
            }
        });
    });

    // Broadcast the message to the teacher and student
    socket.on('chat message', (msg) => {
        console.log("Message received: ", msg.text);
        console.log("Chat message: ", msg);

        msg.receiver = socket.teacher.id;

        // Fetch the username from the database
        const queryUSER = 'SELECT id, username FROM accounts_customuser WHERE Uni_ID = ?';
        db.query(queryUSER, [msg.sender], (error, results) => {
            if (error){
                console.error(error.message);
                return;
            }

            msg.text = results[0].username + ': ' + msg.text;
            msg.sender = results[0].id;
            console.log(msg.sender);

            console.log('Username successful');

            io.to(socket.teacher.id).emit('chat message', msg);
            socket.emit('chat message', msg);
        });

        const queryReceiver = 'SELECT id FROM accounts_customuser WHERE Uni_ID = ?';
        db.query(queryReceiver, [msg.receiver], (error, results) => {
            if (error){
                console.error(error.message);
                return;
            }
            msg.receiver = results[0].id;

            console.log(msg.receiver);
            console.log(msg.sender);

            console.log('Inserting message into homepage_message table');
            const query = 'INSERT into homepage_message (content, timestamp, receiver_id, sender_id, lecture_number) VALUES (?, CURRENT_TIMESTAMP, ?, ?, ?)';
            const params = [msg.text, msg.receiver, msg.sender, parseInt(msg.lectureNumber)];
    
            db.query(query, params, (error, results) => {
                if (error){
                    console.error('Error message here: ', error.message);
                    return;
                }
                console.log('Message inserted into homepage_message table');
            });
        });

        // Insert the message into homepage_message table
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
    const uniId = req.query.Uni_ID;
    console.log(`Uni ID: ${uniId}`);
    db.query('SELECT teacher_id FROM teacher_assignments WHERE student_id = ?', [uniId], (err, results) => {
        if (err){
            console.error(err.message);
            return;
        }
        const teacherId = results[0].teacher_id;
        console.log(`Teacher ID: ${teacherId}`);
        res.json({ teacherId });
    });
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

        connection.query('SELECT * FROM homepage_message WHERE lecture_number = ? ORDER BY timestamp ASC', [lectureNumber], (err, results) => {
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

app.get('/students_assigned_to_teacher', (req, res) => {
    const teacherId = req.query.teacherId;
    db.query('SELECT student_id FROM teacher_assignments WHERE teacher_id = ?', [teacherId], (err, results) => {
        if (err){
            console.error(err.message);
            return;
        }
        let studentsAssignedToTeacher = [];
        for (let row of results){
            db.query('SELECT * FROM accounts_customuser WHERE Uni_ID = ?', [row.student_id], (err, results) => {
                if (err){
                    console.error(err.message);
                    return;
                }
                studentsAssignedToTeacher.push(results[0]);
            });
        }
        res.json(studentsAssignedToTeacher);
    });
});



server.listen(3000, () => {
    console.log('listening on *:3000');
});