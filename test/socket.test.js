const request = require('supertest');
const { app, server, io, closeDbConnection } = require('../server');
const ioClient = require('socket.io-client');
require('dotenv').config();

const socketUrl = `http://localhost:${process.env.PORT || 3000}`;

describe('Express and Socket.IO Server', () => {
  let clientSocket;

  beforeAll((done) => {
    server.listen(process.env.PORT || 3000, () => {
      done();
    });
  });

  afterAll((done) => {
    if (clientSocket) {
      clientSocket.close();
    }
    server.close(() => {
      closeDbConnection().then(() => done()).catch(done);
    });
  });

  beforeEach((done) => {
    clientSocket = ioClient(socketUrl, {
      transports: ['websocket'],
      'force new connection': true,
    });
    clientSocket.on('connect', done);
  });

  afterEach((done) => {
    if (clientSocket.connected) {
      clientSocket.disconnect();
    }
    done();
  });

  test('should allow CORS for any origin', async () => {
    const response = await request(app).get('/');
    expect(response.headers['access-control-allow-origin']).toBe('*');
  });

  test('should handle User Login event', (done) => {
    clientSocket.emit('User Login', '123');
    done();
  });

  test('should join and leave a room', (done) => {
    const roomName = 'testRoom';

    clientSocket.emit('join room', roomName);

    clientSocket.on('joined room', (room) => {
      expect(room).toBe(roomName);

      clientSocket.emit('leave room', roomName);

      clientSocket.on('left room', (leftRoom) => {
        expect(leftRoom).toBe(roomName);
        done();
      });
    });
  });

  test('should handle chat ended event', (done) => {
    const data = { studentId: 'student1', teacherId: 'teacher1', lectureNumber: 1 };
    const roomName = `room-${data.studentId}-${data.teacherId}-${data.lectureNumber}`;

    clientSocket.emit('chat ended', data);

    clientSocket.on('left room', (leftRoom) => {
      expect(leftRoom).toBe(roomName);
      done();
    });
  });
});
