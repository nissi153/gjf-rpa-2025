# Node.js Express API 서버

간단한 REST API 서버입니다. 사용자 정보를 관리할 수 있는 CRUD 기능을 제공합니다.

## 설치 및 실행

### 1. 의존성 설치
```bash
npm install
```

### 2. 서버 실행
```bash
# 일반 실행
npm start

# 개발 모드 (자동 재시작)
npm run dev
```

서버는 기본적으로 포트 3000에서 실행됩니다.

## API 엔드포인트

### 기본 정보
- **GET /** - API 정보 및 사용 가능한 엔드포인트 목록

### 사용자 관리
- **GET /api/users** - 모든 사용자 조회
- **GET /api/users/:id** - 특정 사용자 조회
- **POST /api/users** - 새 사용자 추가
- **PUT /api/users/:id** - 사용자 정보 수정
- **DELETE /api/users/:id** - 사용자 삭제

## 사용 예시

### 모든 사용자 조회
```bash
curl http://localhost:3000/api/users
```

### 특정 사용자 조회
```bash
curl http://localhost:3000/api/users/1
```

### 새 사용자 추가
```bash
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "홍길동",
    "email": "hong@example.com",
    "age": 35
  }'
```

### 사용자 정보 수정
```bash
curl -X PUT http://localhost:3000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "김철수",
    "age": 26
  }'
```

### 사용자 삭제
```bash
curl -X DELETE http://localhost:3000/api/users/1
```

## 응답 형식

### 성공 응답
```json
{
  "id": 1,
  "name": "김철수",
  "email": "kim@example.com",
  "age": 25
}
```

### 에러 응답
```json
{
  "error": "사용자를 찾을 수 없습니다."
}
```

## 환경 변수

- `PORT` - 서버 포트 (기본값: 3000)

## 기술 스택

- Node.js
- Express.js
- CORS 미들웨어