-- 코멘트(주석)
-- 대문자 : SQL 예약어
-- 소문자 : 사용자 변수

-- SQLite용 SQL 기초문법

-- 테이블 생성
CREATE TABLE student (
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

-- 데이터(레코드, 행) 추가
-- id : 자동증가, created_at : 기본값
INSERT INTO student (name, age, grade) 
VALUES ('홍길동', 30, '1학년');


-- 전체 검색
-- * : 모든 컬럼을 출력하라
SELECT * FROM student;