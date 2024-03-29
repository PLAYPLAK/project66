-- Create the `classup` database if it doesn't exist
CREATE DATABASE IF NOT EXISTS classup;

-- Switch to the `classup` database
USE classup;

-- Table structure for table `admin`
CREATE TABLE IF NOT EXISTS admin (
  adminID VARCHAR(255) PRIMARY KEY,
  name TEXT
);

-- Table structure for table `user`
CREATE TABLE IF NOT EXISTS user (
  FullNameTH TEXT NOT NULL,
  FullNameENG TEXT NOT NULL,
  UserID VARCHAR(255) PRIMARY KEY,
  Phone TEXT,
  Email TEXT
);

-- Table structure for table `guild`
CREATE TABLE IF NOT EXISTS guild (
  GuildID VARCHAR(255) PRIMARY KEY,
  Alert_Msg TEXT,
  FadminID VARCHAR(255) NOT NULL,
  RoleID TEXT,
  FOREIGN KEY (FadminID) REFERENCES admin (adminID)
);

-- Table structure for table `function_ch`
CREATE TABLE IF NOT EXISTS function_ch (
  FuncID INTEGER PRIMARY KEY AUTO_INCREMENT,
  FuncName TEXT NOT NULL,
  CH_ReplyFuncID TEXT,
  FGuildID VARCHAR(255) NOT NULL,
  FOREIGN KEY (FGuildID) REFERENCES guild (GuildID)
);

-- Table structure for table `member`
CREATE TABLE IF NOT EXISTS member (
  UserID VARCHAR(255),
  GuildID VARCHAR(255),
  profilename TEXT NOT NULL,
  StudentID TEXT NOT NULL,
  PRIMARY KEY (UserID, GuildID),
  FOREIGN KEY (UserID) REFERENCES user (UserID),
  FOREIGN KEY (GuildID) REFERENCES guild (GuildID)
);

-- Table structure for table `response_msg`
CREATE TABLE IF NOT EXISTS response_msg (
  resID INTEGER PRIMARY KEY AUTO_INCREMENT,
  Word TEXT,
  ResMsg TEXT,
  GuildID VARCHAR(255),
  type_ans TEXT,
  FOREIGN KEY (GuildID) REFERENCES guild (GuildID)
);

-- Table structure for table `study_plan`
CREATE TABLE IF NOT EXISTS study_plan (
  planID INTEGER PRIMARY KEY AUTO_INCREMENT,
  dayName TEXT NOT NULL,
  time TEXT NOT NULL,
  subjectName TEXT NOT NULL,
  UserID VARCHAR(255) NOT NULL,
  day_ID TEXT NOT NULL,
  FOREIGN KEY (UserID) REFERENCES user (UserID)
);


