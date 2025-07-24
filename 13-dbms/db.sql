-- 코멘트(주석)
-- 대문자 : SQL 예약어
-- 소문자 : 사용자 변수

-- SQLite용 SQL 기초문법

-- 테이블 생성
CREATE TABLE IF NOT EXISTS student (
    -- PRIMARY KEY : 기본키(Key)
    -- AUTOINCREMENT : 1씩 자동증가
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- DB인덱스(학번,주민번호 아님)
    -- NOT NULL : Empty를 허용하지 않음. insert시 NULL이면 오류발생!
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL,
    -- profile_img TEXT, -- 'myprofile_202507241929.png'
    -- TIMESTAMP : 날짜시간(1970.0.0.0.0 정수값), DATE : 날짜시간
    -- DEFAULT : 생략시 기본값
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 테이블 삭제(주의 !!!)
-- DROP TABLE student;


-- 데이터(레코드, 행) 추가
-- id : 자동증가, created_at : 기본값
INSERT INTO student (name, age, grade) 
VALUES ('홍길동', 30, '1학년');

INSERT INTO student (name, age, grade) 
VALUES ('김영희', 25, '2학년');

INSERT INTO student (name, age, grade, created_at) 
VALUES ('이철수', 22, '3학년', '2025-07-25');

-- 데이터 수정 (name이 홍길동인 사람의 grade를 '4학년'으로 수정하라.)
UPDATE student 
SET grade = '4학년', age = 35
WHERE name = '홍길동';


-- 데이터 삭제
-- DELETE FROM student; -- 전체 레코드 삭제됨 !!!
DELETE FROM student
WHERE name = '김영희';


-- 전체 검색
-- * : 모든 컬럼을 출력하라
SELECT * FROM student;

-- SQL 검색 기능
-- 특정 컬럼만 검색하기
SELECT name, grade
FROM student;

-- 조건 조회(WHERE)
SELECT * FROM student
WHERE age >= 27;






