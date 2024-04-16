-- drop database UniversityRegistrationDB;

CREATE DATABASE if not exists UniversityRegistrationDB;
USE UniversityRegistrationDB;

CREATE TABLE if not exists Department (
    DepartmentKey int PRIMARY KEY,
    Name VARCHAR(255),
    Chair VARCHAR(255)
);

CREATE TABLE if not exists Registar (
   RegistarID INT PRIMARY KEY,
   PhoneNum TEXT,
   Email VARCHAR(255),
   FirstName VARCHAR(255),
   LastName VARCHAR(255),
   AccessLevel VARCHAR(255)
);

CREATE TABLE if not exists Teacher (
    TeacherId INT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Email VARCHAR(255),
    DepartmentKey int,
    CONSTRAINT fk1 FOREIGN KEY (DepartmentKey)
        REFERENCES Department(DepartmentKey)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE if not exists Course (
    CourseID INT PRIMARY KEY,
    Name VARCHAR(255),
    Credit_Hours INT,
    Description TEXT,
    Pre_req INT,
    Teacher_ID INT,
    DepartmentKey int,
    CONSTRAINT fk2 FOREIGN KEY (DepartmentKey) REFERENCES Department(DepartmentKey)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk3 FOREIGN KEY (Teacher_ID)
        REFERENCES Teacher(TeacherID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk4 FOREIGN KEY (Pre_req)
        REFERENCES Course(CourseID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

create table if not exists Students(
    studentID int primary key,
    firstName varchar(255),
    lastName varchar(255),
    major text
);

create table if not exists Plan(
    planID int,
    studentID int,
    planName varchar(255),
    primary key(planID, studentID),
    foreign key (studentID) references Students(studentID)
);

create table if not exists StudentAcademicRecord(
    recordID int,
    studentID int,
    standing varchar(255),
    creditHours int,
    RegistrationTimeTicket datetime,
    primary key (recordID, studentID),
    foreign key (studentID) references Students(studentID)
);

create table if not exists Feedback(
    feedbackID int,
    studentID int,
    comments text,
    rating int,
    courseID int,
    primary key (feedbackID, studentID),
    foreign key (courseID) references Course(courseID)
);

CREATE TABLE if not exists Advisor (
    Advisor_ID INT NOT NULL,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    DepartmentKey VARCHAR(255),
    Colleagues int,
    PRIMARY KEY (Advisor_ID),
    FOREIGN KEY (Colleagues) REFERENCES Advisor(Advisor_ID) ON UPDATE cascade ON DELETE restrict,
    foreign key (colleagues) references Advisor(Advisor_ID) on update cascade on delete restrict
);

create table if not exists DegreeAudit(
    auditID int primary key,
    startTerm varchar(255),
    gradTerm varchar(255),
    status varchar(255),
    advisorID int,
    foreign key (advisorID) references Advisor(advisor_ID)
);

CREATE TABLE if not exists RegistarCourseBridge (
    CourseID INT,
    RegistarID INT,
    primary key(courseiD, registarID),
    CONSTRAINT fk5 FOREIGN KEY (CourseID)
        REFERENCES Course(CourseID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk6 FOREIGN KEY (RegistarID)
        REFERENCES Registar(RegistarID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE if not exists RegistarDepBridge (
    DepartmentKey INT,
    RegistarID INT,
    primary key(departmentKey, registarID),
    CONSTRAINT fk7 FOREIGN KEY (DepartmentKey)
        REFERENCES Department(DepartmentKey)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk8 FOREIGN KEY (RegistarID)
        REFERENCES Registar(RegistarID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
CREATE TABLE if not exists StudentDepartment(
    studentId INTEGER,
    departmentKey INTEGER,
    FOREIGN KEY (studentId) REFERENCES Students(studentID),
    FOREIGN KEY (departmentKey) REFERENCES Department(departmentKey),
    PRIMARY KEY (studentId, departmentKey)
);

CREATE TABLE if not exists Academic_Policies (
    PolicyID INT NOT NULL,
    CourseID INT NOT NULL,
    Title VARCHAR(255),
    Description TEXT,
    EffectiveDate Date,
    PRIMARY KEY(PolicyID),
    FOREIGN KEY(CourseID) REFERENCES Course(CourseID) ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE if not exists Enrollment_Status  (
    StatID INT NOT NULL,
    Total_Enrollment INT,
    Maximum_Capacity INT,
    Waitlist_Total INT,
    CourseID INT NOT NULL,
    PRIMARY KEY (StatID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID) ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE if not exists RecordAccess(
    recordId INTEGER,
    advisorId INTEGER,
    FOREIGN KEY (recordId) REFERENCES StudentAcademicRecord(recordId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (advisorId) REFERENCES Advisor(advisor_Id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    PRIMARY KEY (recordId, advisorId)
);

Create table if not exists StudentsCourse(
    courseID int,
    studentID int,
    primary key(courseID, studentID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID) ON UPDATE cascade ON DELETE restrict,
    FOREIGN KEY (studentID) REFERENCES Students(studentID) ON UPDATE cascade ON DELETE restrict
)
