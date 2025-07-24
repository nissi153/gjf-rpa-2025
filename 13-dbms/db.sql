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

-- 연습문제
-- 1. grade가 3학년인 학생만 출력하시오.
SELECT * FROM student
WHERE grade = '3학년';
-- 2. id가 1인 학생만 출력하시오.
SELECT * FROM student
WHERE id = 1;
-- 3. 이름안에 '수'가 들어간 학생(들)을 출력하시오. LIKE절
-- % : 길이와 내용이 상관없이  _(under score) : 길이가 1이고 내용이 상관없음.
SELECT * FROM student
WHERE name like '%수%';
SELECT * FROM student
WHERE name like '__수'; -- '이철수'
-- 4. age(나이)가 20이상 30이하 사이에 들어간 학생들을 출력하시오. BETWEEN절
SELECT * FROM student
WHERE age BETWEEN 20 AND 30;
SELECT * FROM student
WHERE age >= 20 and age <= 30;

-- IN() 함수 : ~가 포함된 경우 TRUE
-- 이름이 '홍길동' 또는 '이철수'인 경우
SELECT * FROM student
WHERE name IN('홍길동', '이철수');
SELECT * FROM student
where name = '홍길동' or name = '이철수';

-- 정렬(sort)
-- 나이순으로 오름차순 정렬
SELECT * FROM student
ORDER by age ASC;

-- 나이순으로 내림차순 정렬
SELECT * FROM student
ORDER by age DESC;

-- 학년순, 나이순으로 오름차순 정렬
SELECT * FROM student
ORDER by grade ASC, age ASC;

-- 상위 N개만 보기(LIMIT절)
-- 상위 2개만 보기
SELECT * FROM student
LIMIT 2;

-- 최근에 등록된 학생 2명만 보기
SELECT * FROM student
ORDER by created_at DESC
LIMIT 2;


INSERT INTO student (name, age, grade) 
VALUES ('이순신', 40, '4학년');

INSERT INTO student (name, age, grade) 
VALUES ('강감찬', 25, '3학년');

INSERT INTO student (name, age, grade) 
VALUES ('임꺽정', 28, '1학년');


-- 연습문제
-- 1. 25세 이상인 학생들의 이름과 학년을 나이가 많은 순으로 조회하시오.
SELECT name, grade, age 
FROM student
WHERE age >= 25
ORDER by age DESC;
-- 2. ‘3학년’ 학생 중에서 최근에 등록된 학생 1명의 전체 정보를 조회하시오.
SELECT *
FROM student
WHERE grade = '3학년'
ORDER by created_at DESC
LIMIT 1;
-- 3. 학생 이름에 ‘길’ 또는 '정'이 포함된 학생들의 이름과 나이를 조회하시오.
SELECT name, age
FROM student
WHERE name like '%길%' or name like '%정%';


SELECT * FROM student;








