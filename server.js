const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static('homepage/templates/homepage'));

let teachers = [];

// Connect to the SQLite database and fetch teachers
let db = new sqlite3.Database('db.sqlite3', sqlite3.OPEN_READONLY, (err) => {
    if (err) {
        console.error(err.message);
    }
    console.log('Connected to the database.');

});

db.serialize(() => {
    db.all('SELECT * FROM accounts_customuser WHERE user_type = "teacher"', (err, rows) => {
        if (err){
            console.error(err.message);
        }
        for (let row of rows){
            teachers.push({
                id: row.id,
                chats: []
            });
        }

    });
});

db.close((err) => {
    if (err) {
        console.error(err.message);
    }
    console.log('Closed the database connection.');
})

io.on('connection', (socket) => {
    console.log('a user connected');

    // Broadcast the message to the teacher and student
    socket.on('chat message', (msg) => {
        // Assign the student to a teacher with the least chats when they send the first message
        if (!socket.teacher){
            const teacher = teachers.sort((a, b) => a.chats.length - b.chats.length)[0];
            teacher.chats.push(socket);
            socket.teacher = teacher;
        }

        io.to(socket.teacher.id).emit('chat message', msg);
        socket.emit('chat message', msg);
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

app.use(express.json());

app.post('/new_user', (req, res) => {
    const user = req.body;
    console.log(user);  // Log the user data to the console
    res.status(200).send('User data received');
});

server.listen(3000, () => {
    console.log('listening on *:3000');
});