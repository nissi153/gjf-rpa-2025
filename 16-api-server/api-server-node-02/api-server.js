const express = require('express');
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// JSON 파싱 미들웨어
app.use(express.json());

// Supabase 설정
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.error('Warning: Supabase configuration required!');
    console.error('1. Create .env file and add:');
    console.error('   SUPABASE_URL=your-actual-supabase-url');
    console.error('   SUPABASE_KEY=your-actual-supabase-anon-key');
    process.exit(1);
}

// Supabase 클라이언트 생성
const supabase = createClient(supabaseUrl, supabaseKey);

// 에러 응답 헬퍼 함수
const errorResponse = (message, statusCode = 400) => {
    return {
        status: statusCode,
        error: message
    };
};

const successResponse = (data, message = "Success") => {
    return {
        message: message,
        data: data
    };
};

// 1. 모든 학생 조회 (GET /students)
app.get('/students', async (req, res) => {
    try {
        const { data, error } = await supabase
            .from('students')
            .select('*')
            .order('id');
        
        if (error) {
            return res.status(500).json(errorResponse(`Failed to retrieve students: ${error.message}`, 500));
        }
        
        res.json(successResponse(data, "All students retrieved successfully"));
    } catch (error) {
        res.status(500).json(errorResponse(`Failed to retrieve students: ${error.message}`, 500));
    }
});

// 2. 특정 학생 조회 (GET /students/:id)
app.get('/students/:id', async (req, res) => {
    try {
        const studentId = parseInt(req.params.id);
        
        const { data, error } = await supabase
            .from('students')
            .select('*')
            .eq('id', studentId);
        
        if (error) {
            return res.status(500).json(errorResponse(`Failed to retrieve student: ${error.message}`, 500));
        }
        
        if (!data || data.length === 0) {
            return res.status(404).json(errorResponse(`Student with ID ${studentId} not found`, 404));
        }
        
        res.json(successResponse(data[0], "Student retrieved successfully"));
    } catch (error) {
        res.status(500).json(errorResponse(`Failed to retrieve student: ${error.message}`, 500));
    }
});

// 3. 새 학생 추가 (POST /students)
app.post('/students', async (req, res) => {
    try {
        const { name, age, grade } = req.body;
        
        // 필수 필드 검증
        if (!name || !age || !grade) {
            return res.status(400).json(errorResponse("Required fields missing: name, age, grade"));
        }
        
        const studentData = {
            name: name,
            age: parseInt(age),
            grade: parseInt(grade)
        };
        
        const { data, error } = await supabase
            .from('students')
            .insert(studentData)
            .select();
        
        if (error) {
            return res.status(500).json(errorResponse(`Failed to create student: ${error.message}`, 500));
        }
        
        res.status(201).json(successResponse(data[0], "Student created successfully"));
    } catch (error) {
        res.status(500).json(errorResponse(`Failed to create student: ${error.message}`, 500));
    }
});

// 4. 학생 정보 수정 (PUT /students/:id)
app.put('/students/:id', async (req, res) => {
    try {
        const studentId = parseInt(req.params.id);
        const { name, age, grade } = req.body;
        
        // 기존 학생 존재 확인
        const { data: existingStudent, error: checkError } = await supabase
            .from('students')
            .select('*')
            .eq('id', studentId);
        
        if (checkError) {
            return res.status(500).json(errorResponse(`Failed to check student: ${checkError.message}`, 500));
        }
        
        if (!existingStudent || existingStudent.length === 0) {
            return res.status(404).json(errorResponse(`Student with ID ${studentId} not found`, 404));
        }
        
        // 수정할 데이터 준비
        const updateData = {};
        if (name !== undefined) updateData.name = name;
        if (age !== undefined) updateData.age = parseInt(age);
        if (grade !== undefined) updateData.grade = parseInt(grade);
        
        if (Object.keys(updateData).length === 0) {
            return res.status(400).json(errorResponse("No data to update"));
        }
        
        const { data, error } = await supabase
            .from('students')
            .update(updateData)
            .eq('id', studentId)
            .select();
        
        if (error) {
            return res.status(500).json(errorResponse(`Failed to update student: ${error.message}`, 500));
        }
        
        res.json(successResponse(data[0], "Student updated successfully"));
    } catch (error) {
        res.status(500).json(errorResponse(`Failed to update student: ${error.message}`, 500));
    }
});

// 5. 학생 정보 삭제 (DELETE /students/:id)
app.delete('/students/:id', async (req, res) => {
    try {
        const studentId = parseInt(req.params.id);
        
        // 삭제 전 학생 존재 확인
        const { data: existingStudent, error: checkError } = await supabase
            .from('students')
            .select('name')
            .eq('id', studentId);
        
        if (checkError) {
            return res.status(500).json(errorResponse(`Failed to check student: ${checkError.message}`, 500));
        }
        
        if (!existingStudent || existingStudent.length === 0) {
            return res.status(404).json(errorResponse(`Student with ID ${studentId} not found`, 404));
        }
        
        const studentName = existingStudent[0].name;
        
        // 학생 정보 삭제
        const { data, error } = await supabase
            .from('students')
            .delete()
            .eq('id', studentId)
            .select();
        
        if (error) {
            return res.status(500).json(errorResponse(`Failed to delete student: ${error.message}`, 500));
        }
        
        res.json(successResponse({ id: studentId, name: studentName }, "Student deleted successfully"));
    } catch (error) {
        res.status(500).json(errorResponse(`Failed to delete student: ${error.message}`, 500));
    }
});

// 6. 이름으로 학생 검색 (GET /students/search?name=<name>)
app.get('/students/search', async (req, res) => {
    try {
        const { name } = req.query;
        
        if (!name) {
            return res.status(400).json(errorResponse("Please provide a name to search"));
        }
        
        const { data, error } = await supabase
            .from('students')
            .select('*')
            .ilike('name', `%${name}%`);
        
        if (error) {
            return res.status(500).json(errorResponse(`Failed to search students: ${error.message}`, 500));
        }
        
        res.json(successResponse(data, `Search for '${name}' completed`));
    } catch (error) {
        res.status(500).json(errorResponse(`Failed to search students: ${error.message}`, 500));
    }
});

// 헬스 체크 엔드포인트
app.get('/health', (req, res) => {
    res.json(successResponse({ status: "healthy" }, "API server is running normally"));
});

// 루트 엔드포인트
app.get('/', (req, res) => {
    res.json(successResponse({
        endpoints: {
            "GET /students": "Get all students",
            "GET /students/:id": "Get specific student",
            "POST /students": "Create new student",
            "PUT /students/:id": "Update student information",
            "DELETE /students/:id": "Delete student",
            "GET /students/search?name=<name>": "Search students by name",
            "GET /health": "Health check"
        }
    }, "Node.js Express REST API Server"));
});

// 서버 시작
app.listen(PORT, () => {
    console.log(`Starting Node.js Express REST API server on port ${PORT}...`);
    console.log("Available endpoints:");
    console.log("- GET    /students          : Get all students");
    console.log("- GET    /students/:id      : Get specific student");
    console.log("- POST   /students          : Create new student");
    console.log("- PUT    /students/:id      : Update student information");
    console.log("- DELETE /students/:id      : Delete student");
    console.log("- GET    /students/search   : Search students by name");
    console.log("- GET    /health            : Health check");
    console.log(`Server running at http://localhost:${PORT}`);
});
