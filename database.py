-- ============================================================
-- NATIONAL ROBOTICS COMPETITION DATABASE
-- PostgreSQL
-- PART 4 - DATABASE CREATION
-- PART 5 - INSERTING DATA
-- ============================================================

-- ============================================================
-- 1. CREATE DATABASE
-- ============================================================

CREATE DATABASE national_robotics_competition;

-- After creating the database, connect to it:
-- \c national_robotics_competition


-- ============================================================
-- 2. DROP TABLES IF THEY ALREADY EXIST
-- ============================================================

DROP TABLE IF EXISTS round_judge CASCADE;
DROP TABLE IF EXISTS competition_team CASCADE;
DROP TABLE IF EXISTS team_participant CASCADE;
DROP TABLE IF EXISTS award CASCADE;
DROP TABLE IF EXISTS score CASCADE;
DROP TABLE IF EXISTS robot CASCADE;
DROP TABLE IF EXISTS round CASCADE;
DROP TABLE IF EXISTS competition CASCADE;
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS judge CASCADE;
DROP TABLE IF EXISTS team CASCADE;
DROP TABLE IF EXISTS participant CASCADE;
DROP TABLE IF EXISTS school CASCADE;


-- ============================================================
-- 3. CREATE SCHOOL TABLE
-- ============================================================

CREATE TABLE school (
    school_id SERIAL PRIMARY KEY,
    school_name VARCHAR(150) NOT NULL UNIQUE,
    city VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    contact_email VARCHAR(100) UNIQUE
);


-- ============================================================
-- 4. CREATE PARTICIPANT TABLE
-- ============================================================

CREATE TABLE participant (
    participant_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10),
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    school_id INTEGER NOT NULL,

    CONSTRAINT fk_participant_school
        FOREIGN KEY (school_id)
        REFERENCES school(school_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_participant_gender
        CHECK (gender IN ('Male', 'Female')),

    CONSTRAINT chk_participant_birth
        CHECK (date_of_birth <= CURRENT_DATE)
);


-- ============================================================
-- 5. CREATE TEAM TABLE
-- ============================================================

CREATE TABLE team (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    school_id INTEGER NOT NULL,
    coach_name VARCHAR(100) NOT NULL,
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'Active',

    CONSTRAINT fk_team_school
        FOREIGN KEY (school_id)
        REFERENCES school(school_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_team_status
        CHECK (status IN ('Active', 'Inactive', 'Disqualified'))
);


-- ============================================================
-- 6. CREATE CATEGORY TABLE
-- ============================================================

CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    age_min INTEGER NOT NULL,
    age_max INTEGER NOT NULL,
    description TEXT,

    CONSTRAINT chk_category_age
        CHECK (
            age_min >= 6
            AND age_max <= 25
            AND age_min <= age_max
        )
);


-- ============================================================
-- 7. CREATE COMPETITION TABLE
-- ============================================================

CREATE TABLE competition (
    competition_id SERIAL PRIMARY KEY,
    competition_name VARCHAR(150) NOT NULL UNIQUE,
    competition_date DATE NOT NULL,
    location VARCHAR(150) NOT NULL,
    category_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Planned',

    CONSTRAINT fk_competition_category
        FOREIGN KEY (category_id)
        REFERENCES category(category_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_competition_status
        CHECK (
            status IN ('Planned', 'Active', 'Completed', 'Cancelled')
        )
);


-- ============================================================
-- 8. CREATE ROUND TABLE
-- ============================================================

CREATE TABLE round (
    round_id SERIAL PRIMARY KEY,
    competition_id INTEGER NOT NULL,
    round_name VARCHAR(100) NOT NULL,
    round_number INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,

    CONSTRAINT fk_round_competition
        FOREIGN KEY (competition_id)
        REFERENCES competition(competition_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_round_number
        CHECK (round_number > 0),

    CONSTRAINT chk_round_time
        CHECK (end_time > start_time),

    CONSTRAINT uq_round_number
        UNIQUE (competition_id, round_number)
);


-- ============================================================
-- 9. CREATE ROBOT TABLE
-- ============================================================

CREATE TABLE robot (
    robot_id SERIAL PRIMARY KEY,
    team_id INTEGER NOT NULL,
    robot_name VARCHAR(100) NOT NULL UNIQUE,
    model VARCHAR(100) NOT NULL,
    build_year INTEGER NOT NULL,
    technical_description TEXT,

    CONSTRAINT fk_robot_team
        FOREIGN KEY (team_id)
        REFERENCES team(team_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_robot_year
        CHECK (build_year BETWEEN 2015 AND 2030)
);


-- ============================================================
-- 10. CREATE JUDGE TABLE
-- ============================================================

CREATE TABLE judge (
    judge_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20)
);


-- ============================================================
-- 11. CREATE SCORE TABLE
-- ============================================================

CREATE TABLE score (
    score_id SERIAL PRIMARY KEY,
    team_id INTEGER NOT NULL,
    round_id INTEGER NOT NULL,
    judge_id INTEGER NOT NULL,
    technical_score NUMERIC(5,2) NOT NULL,
    creativity_score NUMERIC(5,2) NOT NULL,
    performance_score NUMERIC(5,2) NOT NULL,
    total_score NUMERIC(6,2) GENERATED ALWAYS AS
        (
            technical_score
            + creativity_score
            + performance_score
        ) STORED,
    comments TEXT,

    CONSTRAINT fk_score_team
        FOREIGN KEY (team_id)
        REFERENCES team(team_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_score_round
        FOREIGN KEY (round_id)
        REFERENCES round(round_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_score_judge
        FOREIGN KEY (judge_id)
        REFERENCES judge(judge_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_technical_score
        CHECK (technical_score BETWEEN 0 AND 40),

    CONSTRAINT chk_creativity_score
        CHECK (creativity_score BETWEEN 0 AND 30),

    CONSTRAINT chk_performance_score
        CHECK (performance_score BETWEEN 0 AND 30),

    CONSTRAINT uq_team_round_judge
        UNIQUE (team_id, round_id, judge_id)
);


-- ============================================================
-- 12. CREATE AWARD TABLE
-- ============================================================

CREATE TABLE award (
    award_id SERIAL PRIMARY KEY,
    competition_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    award_name VARCHAR(100) NOT NULL,
    award_place INTEGER NOT NULL,
    award_date DATE NOT NULL,

    CONSTRAINT fk_award_competition
        FOREIGN KEY (competition_id)
        REFERENCES competition(competition_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_award_team
        FOREIGN KEY (team_id)
        REFERENCES team(team_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_award_place
        CHECK (award_place BETWEEN 1 AND 10),

    CONSTRAINT uq_competition_place
        UNIQUE (competition_id, award_place)
);


-- ============================================================
-- 13. CREATE TEAM_PARTICIPANT TABLE
-- ============================================================

CREATE TABLE team_participant (
    team_id INTEGER NOT NULL,
    participant_id INTEGER NOT NULL,
    role VARCHAR(50) NOT NULL,
    joined_date DATE NOT NULL DEFAULT CURRENT_DATE,

    PRIMARY KEY (team_id, participant_id),

    CONSTRAINT fk_tp_team
        FOREIGN KEY (team_id)
        REFERENCES team(team_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_tp_participant
        FOREIGN KEY (participant_id)
        REFERENCES participant(participant_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_member_role
        CHECK (
            role IN (
                'Team Leader',
                'Programmer',
                'Engineer',
                'Designer',
                'Researcher'
            )
        )
);


-- ============================================================
-- 14. CREATE COMPETITION_TEAM TABLE
-- ============================================================

CREATE TABLE competition_team (
    competition_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE,
    registration_status VARCHAR(20) NOT NULL DEFAULT 'Registered',

    PRIMARY KEY (competition_id, team_id),

    CONSTRAINT fk_ct_competition
        FOREIGN KEY (competition_id)
        REFERENCES competition(competition_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_ct_team
        FOREIGN KEY (team_id)
        REFERENCES team(team_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_registration_status
        CHECK (
            registration_status IN (
                'Registered',
                'Confirmed',
                'Withdrawn'
            )
        )
);


-- ============================================================
-- 15. CREATE ROUND_JUDGE TABLE
-- ============================================================

CREATE TABLE round_judge (
    round_id INTEGER NOT NULL,
    judge_id INTEGER NOT NULL,
    assigned_role VARCHAR(50) NOT NULL,

    PRIMARY KEY (round_id, judge_id),

    CONSTRAINT fk_rj_round
        FOREIGN KEY (round_id)
        REFERENCES round(round_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_rj_judge
        FOREIGN KEY (judge_id)
        REFERENCES judge(judge_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_judge_role
        CHECK (
            assigned_role IN (
                'Head Judge',
                'Technical Judge',
                'Performance Judge',
                'Safety Judge'
            )
        )
);


-- ============================================================
-- PART 5
-- INSERT REALISTIC DATA
-- ============================================================


-- ============================================================
-- 16. INSERT SCHOOLS
-- ============================================================

INSERT INTO school
(school_name, city, region, address, contact_email)
VALUES
('Nazarbayev Intellectual School of Atyrau', 'Atyrau', 'Atyrau Region',
 '45 Abay Avenue', 'nis.atyrau@example.kz'),

('Atyrau Regional Specialized Boarding School', 'Atyrau', 'Atyrau Region',
 '12 Satpayev Street', 'arsbschool@example.kz'),

('Bilim Innovation Lyceum Atyrau', 'Atyrau', 'Atyrau Region',
 '78 Azattyk Street', 'bilim.atyrau@example.kz'),

('Nazarbayev Intellectual School of Astana', 'Astana', 'Astana',
 '10 Kabanbay Batyr Avenue', 'nis.astana@example.kz'),

('Nazarbayev Intellectual School of Almaty', 'Almaty', 'Almaty',
 '85 Zheltoksan Street', 'nis.almaty@example.kz'),

('Kazakh-Turkish Lyceum Shymkent', 'Shymkent', 'Turkistan Region',
 '23 Tauke Khan Avenue', 'ktl.shymkent@example.kz'),

('Physics and Mathematics School Karaganda', 'Karaganda', 'Karaganda Region',
 '31 Bukhar Zhyrau Avenue', 'pms.karaganda@example.kz'),

('IT Lyceum Aktobe', 'Aktobe', 'Aktobe Region',
 '18 Abulkhair Khan Avenue', 'it.aktobe@example.kz'),

('Robotics School Kostanay', 'Kostanay', 'Kostanay Region',
 '55 Altynsarin Street', 'robotics.kostanay@example.kz'),

('Technical Lyceum Pavlodar', 'Pavlodar', 'Pavlodar Region',
 '40 Nazarbayev Avenue', 'tech.pavlodar@example.kz');


-- ============================================================
-- 17. INSERT PARTICIPANTS
-- ============================================================

INSERT INTO participant
(first_name, last_name, date_of_birth, gender, email, phone, school_id)
VALUES
('Aruzhan', 'Sarsenova', '2008-03-15', 'Female',
 'aruzhan.sarsenova@example.kz', '+77011234501', 1),

('Dias', 'Nurgaliyev', '2007-07-21', 'Male',
 'dias.nurgaliyev@example.kz', '+77011234502', 1),

('Madina', 'Akhmetova', '2009-01-18', 'Female',
 'madina.akhmetova@example.kz', '+77011234503', 2),

('Alikhan', 'Bekov', '2008-11-05', 'Male',
 'alikhan.bekov@example.kz', '+77011234504', 2),

('Amina', 'Tulegenova', '2007-09-12', 'Female',
 'amina.tulegenova@example.kz', '+77011234505', 3),

('Erlan', 'Iskakov', '2008-05-27', 'Male',
 'erlan.iskakov@example.kz', '+77011234506', 3),

('Dana', 'Kairatova', '2009-02-11', 'Female',
 'dana.kairatova@example.kz', '+77011234507', 4),

('Miras', 'Suleimenov', '2007-12-09', 'Male',
 'miras.suleimenov@example.kz', '+77011234508', 4),

('Ayaulym', 'Serikova', '2008-06-19', 'Female',
 'ayaulym.serikova@example.kz', '+77011234509', 5),

('Timur', 'Ospanov', '2007-04-23', 'Male',
 'timur.ospanov@example.kz', '+77011234510', 5),

('Zarina', 'Kassenova', '2009-08-30', 'Female',
 'zarina.kassenova@example.kz', '+77011234511', 6),

('Arman', 'Zhaksybek', '2008-10-17', 'Male',
 'arman.zhaksybek@example.kz', '+77011234512', 6),

('Aigerim', 'Mukhanova', '2007-02-26', 'Female',
 'aigerim.mukhanova@example.kz', '+77011234513', 7),

('Nursultan', 'Abdullin', '2008-01-14', 'Male',
 'nursultan.abdullin@example.kz', '+77011234514', 7),

('Kamila', 'Yessimova', '2009-05-08', 'Female',
 'kamila.yessimova@example.kz', '+77011234515', 8),

('Rustam', 'Kenzhebayev', '2007-06-16', 'Male',
 'rustam.kenzhebayev@example.kz', '+77011234516', 8),

('Inkar', 'Baimuratova', '2008-09-04', 'Female',
 'inkar.baimuratova@example.kz', '+77011234517', 9),

('Sanzhar', 'Kaliyev', '2007-03-29', 'Male',
 'sanzhar.kaliyev@example.kz', '+77011234518', 9),

('Aruzhan', 'Temirbek', '2008-12-02', 'Female',
 'aruzhan.temirbek@example.kz', '+77011234519', 10),

('Adil', 'Rakhimov', '2007-10-25', 'Male',
 'adil.rakhimov@example.kz', '+77011234520', 10);


-- ============================================================
-- 18. INSERT TEAMS
-- ============================================================

INSERT INTO team
(team_name, school_id, coach_name, registration_date, status)
VALUES
('Atyrau RoboStars', 1, 'Marat Kadyrov', '2026-01-15', 'Active'),
('Caspian Coders', 2, 'Aigerim Beketova', '2026-01-18', 'Active'),
('Tech Titans', 3, 'Serik Omarov', '2026-01-20', 'Active'),
('Astana Robotics', 4, 'Kanat Zhumabayev', '2026-01-22', 'Active'),
('Almaty Mechanics', 5, 'Dana Kassenova', '2026-01-25', 'Active'),
('Shymkent RoboLab', 6, 'Murat Saparov', '2026-01-27', 'Active'),
('Karaganda Engineers', 7, 'Askar Tursynov', '2026-02-01', 'Active'),
('Aktobe Innovators', 8, 'Zhanar Ibrayeva', '2026-02-04', 'Active'),
('Kostanay RoboForce', 9, 'Baurzhan Seidakhmet', '2026-02-07', 'Active'),
('Pavlodar Circuit', 10, 'Aliya Nurzhanova', '2026-02-10', 'Active');


-- ============================================================
-- 19. INSERT CATEGORIES
-- ============================================================

INSERT INTO category
(category_name, age_min, age_max, description)
VALUES
('Line Following Robot', 12, 18,
 'Autonomous robot that follows a marked track.'),

('Robot Sumo', 12, 18,
 'Robots compete by pushing an opponent outside the arena.'),

('Rescue Robot', 13, 19,
 'Robots perform autonomous rescue and obstacle tasks.'),

('Robot Football', 12, 18,
 'Autonomous robots compete in a football match.'),

('Innovation Project', 14, 20,
 'Robotics project demonstrating an innovative technical solution.');


-- ============================================================
-- 20. INSERT COMPETITIONS
-- ============================================================

INSERT INTO competition
(competition_name, competition_date, location, category_id, status)
VALUES
('National Robotics Championship 2026 - Line Following',
 '2026-03-15', 'Astana Robotics Arena', 1, 'Completed'),

('National Robotics Championship 2026 - Sumo',
 '2026-03-16', 'Astana Robotics Arena', 2, 'Completed'),

('National Robotics Championship 2026 - Rescue',
 '2026-03-17', 'Astana Robotics Arena', 3, 'Completed'),

('National Robotics Championship 2026 - Football',
 '2026-03-18', 'Astana Robotics Arena', 4, 'Completed'),

('National Robotics Championship 2026 - Innovation',
 '2026-03-19', 'Astana Robotics Arena', 5, 'Completed');


-- ============================================================
-- 21. INSERT ROUNDS
-- ============================================================

INSERT INTO round
(competition_id, round_name, round_number, start_time, end_time)
VALUES
(1, 'Qualification', 1, '2026-03-15 09:00:00', '2026-03-15 11:00:00'),
(1, 'Semi Final', 2, '2026-03-15 12:00:00', '2026-03-15 14:00:00'),
(1, 'Final', 3, '2026-03-15 15:00:00', '2026-03-15 17:00:00'),

(2, 'Qualification', 1, '2026-03-16 09:00:00', '2026-03-16 11:00:00'),
(2, 'Semi Final', 2, '2026-03-16 12:00:00', '2026-03-16 14:00:00'),
(2, 'Final', 3, '2026-03-16 15:00:00', '2026-03-16 17:00:00'),

(3, 'Qualification', 1, '2026-03-17 09:00:00', '2026-03-17 11:00:00'),
(3, 'Semi Final', 2, '2026-03-17 12:00:00', '2026-03-17 14:00:00'),
(3, 'Final', 3, '2026-03-17 15:00:00', '2026-03-17 17:00:00'),

(4, 'Qualification', 1, '2026-03-18 09:00:00', '2026-03-18 11:00:00'),
(4, 'Semi Final', 2, '2026-03-18 12:00:00', '2026-03-18 14:00:00'),
(4, 'Final', 3, '2026-03-18 15:00:00', '2026-03-18 17:00:00'),

(5, 'Presentation', 1, '2026-03-19 09:00:00', '2026-03-19 11:00:00'),
(5, 'Evaluation', 2, '2026-03-19 12:00:00', '2026-03-19 14:00:00'),
(5, 'Final', 3, '2026-03-19 15:00:00', '2026-03-19 17:00:00');


-- ============================================================
-- 22. INSERT ROBOTS
-- ============================================================

INSERT INTO robot
(team_id, robot_name, model, build_year, technical_description)
VALUES
(1, 'Caspian Runner', 'Arduino Autonomous V2', 2026,
 'High-speed line following robot with infrared sensors.'),

(2, 'Steppe Sumo', 'RoboCore Sumo X', 2026,
 'Compact autonomous sumo robot with high torque motors.'),

(3, 'Tech Rescue One', 'RescueBot R3', 2026,
 'Rescue robot equipped with distance and thermal sensors.'),

(4, 'Astana Striker', 'FootballBot Pro', 2026,
 'Autonomous football robot with ball detection sensors.'),

(5, 'Almaty Explorer', 'AI Rover M2', 2025,
 'Mobile robot using computer vision for navigation.'),

(6, 'Shymkent Force', 'RoboSumo X2', 2026,
 'Heavy-duty sumo robot with reinforced chassis.'),

(7, 'Karaganda Scout', 'RescueBot R4', 2026,
 'Autonomous rescue platform with obstacle detection.'),

(8, 'Aktobe Racer', 'LineBot Turbo', 2026,
 'Fast line-following robot with PID control.'),

(9, 'Kostanay Defender', 'SumoMaster 5', 2025,
 'Competition sumo robot with high traction wheels.'),

(10, 'Pavlodar Genius', 'AI Robotics Platform', 2026,
 'Experimental robot using machine learning algorithms.');


-- ============================================================
-- 23. INSERT JUDGES
-- ============================================================

INSERT INTO judge
(first_name, last_name, specialization, email, phone)
VALUES
('Yerlan', 'Sadykov', 'Robotics Engineering',
 'yerlan.sadykov@robotics.kz', '+77015550001'),

('Ainur', 'Kassenova', 'Artificial Intelligence',
 'ainur.kassenova@robotics.kz', '+77015550002'),

('Marat', 'Orazbayev', 'Embedded Systems',
 'marat.orazbayev@robotics.kz', '+77015550003'),

('Gulnaz', 'Tulegenova', 'Mechanical Engineering',
 'gulnaz.tulegenova@robotics.kz', '+77015550004'),

('Dias', 'Bekmurat', 'Computer Vision',
 'dias.bekmurat@robotics.kz', '+77015550005'),

('Laura', 'Ismailova', 'Robotics Education',
 'laura.ismailova@robotics.kz', '+77015550006'),

('Ruslan', 'Akhmetov', 'Automation',
 'ruslan.akhmetov@robotics.kz', '+77015550007'),

('Madina', 'Saparova', 'Mechatronics',
 'madina.saparova@robotics.kz', '+77015550008'),

('Kanat', 'Nurlanov', 'Control Systems',
 'kanat.nurlanov@robotics.kz', '+77015550009'),

('Aruzhan', 'Muratova', 'Robotics Research',
 'aruzhan.muratova@robotics.kz', '+77015550010');


-- ============================================================
-- 24. TEAM PARTICIPANTS
-- ============================================================

INSERT INTO team_participant
(team_id, participant_id, role, joined_date)
VALUES
(1, 1, 'Team Leader', '2026-01-16'),
(1, 2, 'Programmer', '2026-01-16'),

(2, 3, 'Team Leader', '2026-01-19'),
(2, 4, 'Engineer', '2026-01-19'),

(3, 5, 'Team Leader', '2026-01-21'),
(3, 6, 'Programmer', '2026-01-21'),

(4, 7, 'Team Leader', '2026-01-23'),
(4, 8, 'Engineer', '2026-01-23'),

(5, 9, 'Team Leader', '2026-01-26'),
(5, 10, 'Researcher', '2026-01-26'),

(6, 11, 'Team Leader', '2026-01-28'),
(6, 12, 'Engineer', '2026-01-28'),

(7, 13, 'Team Leader', '2026-02-02'),
(7, 14, 'Programmer', '2026-02-02'),

(8, 15, 'Team Leader', '2026-02-05'),
(8, 16, 'Designer', '2026-02-05'),

(9, 17, 'Team Leader', '2026-02-08'),
(9, 18, 'Engineer', '2026-02-08'),

(10, 19, 'Team Leader', '2026-02-11'),
(10, 20, 'Researcher', '2026-02-11');


-- ============================================================
-- 25. COMPETITION TEAM REGISTRATION
-- ============================================================

INSERT INTO competition_team
(competition_id, team_id, registration_date, registration_status)
VALUES

(1, 1, '2026-02-15', 'Confirmed'),
(1, 4, '2026-02-16', 'Confirmed'),
(1, 8, '2026-02-17', 'Confirmed'),
(1, 10, '2026-02-18', 'Confirmed'),

(2, 2, '2026-02-15', 'Confirmed'),
(2, 6, '2026-02-16', 'Confirmed'),
(2, 9, '2026-02-17', 'Confirmed'),
(2, 1, '2026-02-18', 'Confirmed'),

(3, 3, '2026-02-15', 'Confirmed'),
(3, 7, '2026-02-16', 'Confirmed'),
(3, 5, '2026-02-17', 'Confirmed'),
(3, 10, '2026-02-18', 'Confirmed'),

(4, 4, '2026-02-15', 'Confirmed'),
(4, 5, '2026-02-16', 'Confirmed'),
(4, 8, '2026-02-17', 'Confirmed'),
(4, 2, '2026-02-18', 'Confirmed'),

(5, 5, '2026-02-15', 'Confirmed'),
(5, 3, '2026-02-16', 'Confirmed'),
(5, 7, '2026-02-17', 'Confirmed'),
(5, 10, '2026-02-18', 'Confirmed');


-- ============================================================
-- 26. ROUND JUDGES
-- ============================================================

INSERT INTO round_judge
(round_id, judge_id, assigned_role)
VALUES

(1, 1, 'Head Judge'),
(1, 3, 'Technical Judge'),
(1, 5, 'Performance Judge'),

(2, 1, 'Head Judge'),
(2, 3, 'Technical Judge'),
(2, 5, 'Performance Judge'),

(3, 1, 'Head Judge'),
(3, 3, 'Technical Judge'),
(3, 5, 'Performance Judge'),

(4, 2, 'Head Judge'),
(4, 4, 'Technical Judge'),
(4, 6, 'Performance Judge'),

(5, 2, 'Head Judge'),
(5, 4, 'Technical Judge'),
(5, 6, 'Performance Judge'),

(6, 2, 'Head Judge'),
(6, 4, 'Technical Judge'),
(6, 6, 'Performance Judge'),

(7, 7, 'Head Judge'),
(7, 8, 'Technical Judge'),
(7, 9, 'Performance Judge'),

(8, 7, 'Head Judge'),
(8, 8, 'Technical Judge'),
(8, 9, 'Performance Judge'),

(9, 7, 'Head Judge'),
(9, 8, 'Technical Judge'),
(9, 9, 'Performance Judge'),

(10, 1, 'Head Judge'),
(10, 6, 'Technical Judge'),
(10, 10, 'Performance Judge'),

(11, 1, 'Head Judge'),
(11, 6, 'Technical Judge'),
(11, 10, 'Performance Judge'),

(12, 1, 'Head Judge'),
(12, 6, 'Technical Judge'),
(12, 10, 'Performance Judge'),

(13, 2, 'Head Judge'),
(13, 5, 'Technical Judge'),
(13, 10, 'Performance Judge'),

(14, 2, 'Head Judge'),
(14, 5, 'Technical Judge'),
(14, 10, 'Performance Judge'),

(15, 2, 'Head Judge'),
(15, 5, 'Technical Judge'),
(15, 10, 'Performance Judge');


-- ============================================================
-- 27. SCORES
-- ============================================================

INSERT INTO score
(team_id, round_id, judge_id, technical_score, creativity_score,
 performance_score, comments)
VALUES

-- Competition 1
(1, 1, 1, 35, 25, 28, 'Excellent speed and stable control.'),
(4, 1, 3, 33, 24, 27, 'Good technical performance.'),
(8, 1, 5, 31, 26, 25, 'Creative design and reliable movement.'),

(1, 2, 1, 37, 26, 29, 'Strong semi-final performance.'),
(4, 2, 3, 35, 25, 27, 'Minor navigation errors.'),
(8, 2, 5, 34, 27, 26, 'Good autonomous control.'),

(1, 3, 1, 39, 28, 30, 'Outstanding final performance.'),
(4, 3, 3, 36, 26, 28, 'Very consistent performance.'),
(8, 3, 5, 35, 27, 27, 'Strong final result.'),

-- Competition 2
(2, 4, 2, 34, 24, 29, 'Strong pushing performance.'),
(6, 4, 4, 36, 25, 28, 'Powerful motor system.'),
(9, 4, 6, 32, 23, 27, 'Good tactical approach.'),

(2, 5, 2, 36, 26, 29, 'Excellent arena control.'),
(6, 5, 4, 38, 24, 29, 'Very strong mechanical design.'),
(9, 5, 6, 34, 25, 28, 'Good strategy.'),

(2, 6, 2, 38, 27, 30, 'Excellent final match.'),
(6, 6, 4, 39, 26, 30, 'Outstanding mechanical performance.'),
(9, 6, 6, 35, 25, 28, 'Strong and controlled performance.'),

-- Competition 3
(3, 7, 7, 36, 27, 28, 'Excellent obstacle detection.'),
(7, 7, 8, 34, 26, 27, 'Good rescue strategy.'),
(5, 7, 9, 35, 25, 26, 'Reliable autonomous movement.'),

(3, 8, 7, 38, 28, 29, 'Excellent sensor integration.'),
(7, 8, 8, 36, 27, 28, 'Strong technical solution.'),
(5, 8, 9, 37, 26, 27, 'Very good performance.'),

(3, 9, 7, 39, 29, 30, 'Excellent rescue performance.'),
(7, 9, 8, 37, 28, 29, 'Very strong final result.'),
(5, 9, 9, 38, 27, 28, 'Excellent autonomous navigation.'),

-- Competition 4
(4, 10, 1, 34, 28, 27, 'Good football control.'),
(5, 10, 6, 36, 27, 28, 'Strong ball detection.'),
(8, 10, 10, 32, 26, 26, 'Good attacking strategy.'),

(4, 11, 1, 37, 29, 28, 'Excellent team coordination.'),
(5, 11, 6, 38, 28, 29, 'Very effective control system.'),
(8, 11, 10, 35, 27, 27, 'Good autonomous movement.'),

(4, 12, 1, 39, 29, 30, 'Outstanding final performance.'),
(5, 12, 6, 38, 30, 29, 'Excellent football strategy.'),
(8, 12, 10, 36, 28, 28, 'Strong final match.'),

-- Competition 5
(5, 13, 2, 35, 29, 27, 'Interesting innovation concept.'),
(3, 13, 5, 37, 28, 28, 'Strong technical presentation.'),
(7, 13, 10, 34, 30, 27, 'Creative and practical solution.'),

(5, 14, 2, 38, 29, 29, 'Excellent prototype quality.'),
(3, 14, 5, 39, 28, 28, 'Strong engineering implementation.'),
(7, 14, 10, 36, 30, 28, 'Highly creative project.'),

(5, 15, 2, 39, 30, 30, 'Outstanding innovation project.'),
(3, 15, 5, 40, 29, 29, 'Excellent technical solution.'),
(7, 15, 10, 38, 30, 29, 'Very impressive project.');


-- ============================================================
-- 28. AWARDS
-- ============================================================

INSERT INTO award
(competition_id, team_id, award_name, award_place, award_date)
VALUES

(1, 1, 'Gold Medal', 1, '2026-03-15'),
(1, 4, 'Silver Medal', 2, '2026-03-15'),
(1, 8, 'Bronze Medal', 3, '2026-03-15'),

(2, 6, 'Gold Medal', 1, '2026-03-16'),
(2, 2, 'Silver Medal', 2, '2026-03-16'),
(2, 9, 'Bronze Medal', 3, '2026-03-16'),

(3, 3, 'Gold Medal', 1, '2026-03-17'),
(3, 7, 'Silver Medal', 2, '2026-03-17'),
(3, 5, 'Bronze Medal', 3, '2026-03-17'),

(4, 4, 'Gold Medal', 1, '2026-03-18'),
(4, 5, 'Silver Medal', 2, '2026-03-18'),
(4, 8, 'Bronze Medal', 3, '2026-03-18'),

(5, 5, 'Gold Medal', 1, '2026-03-19'),
(5, 3, 'Silver Medal', 2, '2026-03-19'),
(5, 7, 'Bronze Medal', 3, '2026-03-19');


-- ============================================================
-- 29. CHECK DATA
-- ============================================================

SELECT 'Schools' AS table_name, COUNT(*) AS record_count
FROM school

UNION ALL

SELECT 'Participants', COUNT(*)
FROM participant

UNION ALL

SELECT 'Teams', COUNT(*)
FROM team

UNION ALL

SELECT 'Categories', COUNT(*)
FROM category

UNION ALL

SELECT 'Competitions', COUNT(*)
FROM competition

UNION ALL

SELECT 'Rounds', COUNT(*)
FROM round

UNION ALL

SELECT 'Robots', COUNT(*)
FROM robot

UNION ALL

SELECT 'Judges', COUNT(*)
FROM judge

UNION ALL

SELECT 'Scores', COUNT(*)
FROM score

UNION ALL

SELECT 'Awards', COUNT(*)
FROM award

UNION ALL

SELECT 'Team Participants', COUNT(*)
FROM team_participant

UNION ALL

SELECT 'Competition Teams', COUNT(*)
FROM competition_team

UNION ALL

SELECT 'Round Judges', COUNT(*)
FROM round_judge;