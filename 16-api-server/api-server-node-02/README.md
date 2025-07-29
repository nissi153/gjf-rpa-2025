# Node.js Express REST API Server

Supabase를 사용한 학생 관리 REST API 서버입니다.

## 기능

- **CRUD 작업**: 학생 정보 생성, 조회, 수정, 삭제
- **검색 기능**: 이름으로 학생 검색
- **에러 처리**: 상세한 에러 메시지와 상태 코드
- **환경 변수**: 보안을 위한 환경 변수 설정

## 설치 및 실행

### 1. 의존성 설치
```bash
npm install
```

### 2. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가하세요:

```env
# Supabase 설정
SUPABASE_URL=your-actual-supabase-url
SUPABASE_KEY=your-actual-supabase-anon-key

# 서버 포트 (선택사항)
PORT=5000
```

### 3. 서버 실행
```bash
# 개발 모드 (nodemon 사용)
npm run dev

# 프로덕션 모드
npm start
```

## API 엔드포인트

### 기본 엔드포인트
- `GET /` - API 서버 정보 및 사용 가능한 엔드포인트 목록
- `GET /health` - 서버 상태 확인

### 학생 관리 엔드포인트
- `GET /students` - 모든 학생 조회
- `GET /students/:id` - 특정 학생 조회
- `POST /students` - 새 학생 추가
- `PUT /students/:id` - 학생 정보 수정
- `DELETE /students/:id` - 학생 정보 삭제
- `GET /students/search?name=<name>` - 이름으로 학생 검색

## 사용 예시

### 학생 추가
```bash
curl -X POST http://localhost:5000/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "김철수",
    "age": 20,
    "grade": 3
  }'
```

### 모든 학생 조회
```bash
curl http://localhost:5000/students
```

### 특정 학생 조회
```bash
curl http://localhost:5000/students/1
```

### 학생 정보 수정
```bash
curl -X PUT http://localhost:5000/students/1 \
  -H "Content-Type: application/json" \
  -d '{
    "age": 21,
    "grade": 4
  }'
```

### 학생 삭제
```bash
curl -X DELETE http://localhost:5000/students/1
```

### 이름으로 검색
```bash
curl "http://localhost:5000/students/search?name=김"
```

## 응답 형식

### 성공 응답
```json
{
  "message": "Success message",
  "data": {
    // 응답 데이터
  }
}
```

### 에러 응답
```json
{
  "status": 400,
  "error": "Error message"
}
```

## Supabase 설정

1. [Supabase](https://supabase.com)에서 새 프로젝트 생성
2. SQL 편집기에서 다음 테이블 생성:

```sql
CREATE TABLE students (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  age INTEGER NOT NULL,
  grade INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

3. 프로젝트 설정에서 URL과 anon key를 복사하여 `.env` 파일에 설정

## 라이센스

ISC