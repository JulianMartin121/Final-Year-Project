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

// Fetch all teachers from the database
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


    socket.on('User Login', (Uni_ID) => {
        console.log('User ID:', Uni_ID);
    });

    // Join a specific room
    socket.on('join room', (roomName) => {
        if (!roomName) {
            console.error("Attempted to join a room without a room name");
            return;
        }
        socket.join(roomName);
        console.log(`Joined room: ${roomName}`);
    });
    

    socket.on('leave room', (roomName) => {
        socket.leave(roomName);
        console.log(`Left room: ${roomName}`);
    });

    // Broadcast the message to the teacher and student
    socket.on('chat message', (msg) => {
        console.log("Received message data:", msg);
        if (!msg.content || !msg.senderId || !msg.roomId) {
            console.log("Received incomplete message data, ignoring.");
            return;
        }

        console.log("Message received:", msg.content);
        console.log("Chat message details:", msg);

        const roomParts = msg.roomId.split('-');
        let receiverId = roomParts[2];

        const roomName = msg.roomId;

        const queryUser = 'SELECT id, username FROM accounts_customuser WHERE Uni_ID = ?';
        db.query(queryUser, [msg.senderId], (error, results) => {
            if (error) {
                console.error('Error fetching sender information:', error.message);
                return;
            }
            const senderId = results[0].id;
            const senderUsername = results[0].username;
            msg.content = `${senderUsername}: ${msg.content}`;

            const queryReceiver = 'SELECT id FROM accounts_customuser WHERE Uni_ID = ?';
            db.query(queryReceiver, [receiverId], (error, results) => {
                if (error) {
                    console.error('Error fetching receiver information:', error.message);
                    return;
                }

                receiverId = results[0].id;

                io.to(roomName).emit('chat message', msg);

                const insertQuery = 'INSERT INTO homepage_message (content, timestamp, receiver_id, sender_id, lecture_number) VALUES (?, CURRENT_TIMESTAMP, ?, ?, ?)';
                const params = [msg.content, receiverId, senderId, parseInt(roomParts[3])];
                db.query(insertQuery, params, (error) => {
                    if (error) {
                        console.error('Error inserting message:', error.message);
                        return;
                    }
                    console.log('Message successfully inserted into homepage_message table');
                });
            });
        });
    });
    

    socket.on('disconnect', () => {
        console.log('user disconnected');
        teachers.forEach(teacher => {
            const index = teacher.chats.indexOf(socket);
            if (index > -1) {
                teacher.chats.splice(index, 1);
            }
        });
    });
});

function assignNewTeacherToStudent(studentId) {
    const teacher = teachers.sort((a, b) => a.chats.length - b.chats.length)[0];
    teacher.chats.push(studentId);
    return teacher.id;
}

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
    console.log('Fetching chat logs');
    const room = req.query.room;
    let [prefix, studentId, teacherId, lectureNumber] = room.split('-');
    console.log(studentId, teacherId, lectureNumber);

    const queryStudent = 'SELECT id, username FROM accounts_customuser WHERE Uni_ID = ?';
        db.query(queryStudent, [studentId], (error, results) => {
            if (error) {
                console.error('Error fetching sender information:', error.message);
                return;
            }
            const studentId = results[0].id;
            console.log("Student ID in chat logs: ", studentId)

            const queryTeacher = 'SELECT id FROM accounts_customuser WHERE Uni_ID = ?';
            db.query(queryTeacher, [teacherId], (error, results) => {
                if (error) {
                    console.error('Error fetching receiver information:', error.message);
                    return;
                }

                teacherId = results[0].id;
                console.log("Teacher ID in chat logs: ", teacherId)

                db.query('SELECT * FROM homepage_message WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?) AND lecture_number = ? ORDER BY timestamp ASC',
                    [studentId, teacherId, teacherId, studentId, lectureNumber], (err, results) => {
                    if (err) {
                        console.error('Query error:', err.message);
                        return;
                    }

                    console.log('Sending results');

                    console.log("Results: ", results);
                
                    res.json(results);
                    });
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

app.get('/teacher_id', (req, res) => {
    const studentId = req.query.studentId;

    db.getConnection((err, connection) => {
        if (err){
            console.error(err.message);
            return;
        }

        connection.query('SELECT teacher_id FROM teacher_assignments WHERE student_id = ?', [studentId], (err, results) => {
            connection.release();
            if (err){
                console.error(err.message);
                return;
            }

            res.json(results[0].teacher_id);
        });
    });
});

app.get('/student_id', (req, res) => {
    const teacherId = req.query.teacherId;

    db.getConnection((err, connection) => {
        if (err){
            console.error(err.message);
            return;
        }

        connection.query('SELECT student_id FROM teacher_assignments WHERE teacher_id = ?', [teacherId], (err, results) => {
            connection.release();
            if (err){
                console.error(err.message);
                return;
            }

            res.json(results[0].student_id);
        });
    });
});

app.get('/assigned_students', (req, res) => {
    const teacherId = req.query.teacherId;
    db.query('SELECT student_id FROM teacher_assignments WHERE teacher_id = ?', [teacherId], (err, results) => {
        if (err){
            console.error(err.message);
            return;
        }
        let assignedStudents = [];
        for (let row of results){
            db.query('SELECT * FROM accounts_customuser WHERE Uni_ID = ?', [row.student_id], (err, results) => {
                if (err){
                    console.error(err.message);
                    return;
                }
                assignedStudents.push(results[0]);
            });
        }
        res.json(assignedStudents);
    });
});

app.get('/student_info', (req, res) => {
    const studentId = req.query.studentId;
    db.query('SELECT Uni_ID, username FROM accounts_customuser WHERE Uni_ID = ?', [studentId], (err, results) => {
        if (err) {
            console.log('Error fetching student info:', err);
            res.status(500).send('Server error');
        } else {
            res.json(results[0]);
        }
    });
});

// Initiate chat between a student and an assigned or newly assigned teacher
app.get('/initiate_chat', (req, res) => {
    const studentId = req.query.studentId;
    const lectureNumber = req.query.lectureNumber;

    if (!studentId || !lectureNumber) {
        return res.status(400).json({ error: 'Missing required parameters' });
    }

    // Check for existing teacher assignment
    db.query('SELECT teacher_id FROM teacher_assignments WHERE student_id = ?', [studentId], (err, results) => {
        if (err) {
            console.error('Error checking for assigned teacher:', err.message);
            return res.status(500).send('Database error');
        }

        let teacherId;

        if (results.length > 0) {
            // Student already has an assigned teacher
            teacherId = results[0].teacher_id;
        } else {
            // Assign a new teacher if no assignment found
            if (teachers.length === 0) {
                return res.status(500).send('No available teachers');
            }

            teacherId = assignNewTeacherToStudent(studentId);

            // Store the new teacher-student assignment
            db.query('INSERT INTO teacher_assignments (teacher_id, student_id) VALUES (?, ?)', [teacherId, studentId], (err) => {
                if (err) {
                    console.error('Error assigning new teacher:', err.message);
                    return res.status(500).send('Failed to assign teacher');
                }
                // Emit an event to notify that a new student is assigned
                io.emit('new_student_assigned', { teacherId, studentId });
            });
        }

        // Create the room name using student, teacher, and lecture number
        const roomName = `room-${studentId}-${teacherId}-${lectureNumber}`;
        res.json({ teacherId, roomName });
    });
});




server.listen(3000, () => {
    console.log('listening on *:3000');
});