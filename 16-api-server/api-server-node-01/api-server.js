const express = require('express');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3000;

// 미들웨어 설정
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 샘플 데이터
let users = [
    { id: 1, name: '김철수', email: 'kim@example.com', age: 25 },
    { id: 2, name: '이영희', email: 'lee@example.com', age: 30 },
    { id: 3, name: '박민수', email: 'park@example.com', age: 28 }
];

// 기본 라우트
app.get('/', (req, res) => {
    res.json({ 
        message: 'Node.js Express API 서버가 실행 중입니다!',
        endpoints: {
            'GET /api/users': '모든 사용자 조회',
            'GET /api/users/:id': '특정 사용자 조회',
            'POST /api/users': '새 사용자 추가',
            'PUT /api/users/:id': '사용자 정보 수정',
            'DELETE /api/users/:id': '사용자 삭제'
        }
    });
});

// 모든 사용자 조회
app.get('/api/users', (req, res) => {
    res.json(users);
});

// 특정 사용자 조회
app.get('/api/users/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const user = users.find(u => u.id === id);
    
    if (!user) {
        return res.status(404).json({ error: '사용자를 찾을 수 없습니다.' });
    }
    
    res.json(user);
});

// 새 사용자 추가
app.post('/api/users', (req, res) => {
    const { name, email, age } = req.body;
    
    if (!name || !email || !age) {
        return res.status(400).json({ error: '이름, 이메일, 나이를 모두 입력해주세요.' });
    }
    
    const newId = users.length > 0 ? Math.max(...users.map(u => u.id)) + 1 : 1;
    const newUser = { id: newId, name, email, age: parseInt(age) };
    
    users.push(newUser);
    res.status(201).json(newUser);
});

// 사용자 정보 수정
app.put('/api/users/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const { name, email, age } = req.body;
    
    const userIndex = users.findIndex(u => u.id === id);
    
    if (userIndex === -1) {
        return res.status(404).json({ error: '사용자를 찾을 수 없습니다.' });
    }
    
    users[userIndex] = {
        ...users[userIndex],
        name: name || users[userIndex].name,
        email: email || users[userIndex].email,
        age: age ? parseInt(age) : users[userIndex].age
    };
    
    res.json(users[userIndex]);
});

// 사용자 삭제
app.delete('/api/users/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const userIndex = users.findIndex(u => u.id === id);
    
    if (userIndex === -1) {
        return res.status(404).json({ error: '사용자를 찾을 수 없습니다.' });
    }
    
    const deletedUser = users.splice(userIndex, 1)[0];
    res.json({ message: '사용자가 삭제되었습니다.', deletedUser });
});

// 에러 핸들링 미들웨어
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: '서버 내부 오류가 발생했습니다.' });
});

// 404 핸들러
app.use((req, res) => {
    res.status(404).json({ error: '요청한 엔드포인트를 찾을 수 없습니다.' });
});

// 서버 시작
app.listen(PORT, () => {
    console.log(`서버가 포트 ${PORT}에서 실행 중입니다.`);
    console.log(`http://localhost:${PORT}`);
    console.log(`API 문서: http://localhost:${PORT}/`);
});

module.exports = app;