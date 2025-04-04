CREATE TABLE Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT (255),
    birth_date DATE,
    course INTEGER(10),
    specialty TEXT (255),
    phone_number VARCHAR (15),
    faculty TEXT (155),
    gender TEXT (20), 
    group_name VARCHAR (15),
    FOREIGN KEY (faculty) REFERENCES Faculty(name),
    FOREIGN KEY (group_name) REFERENCES `Group`(group_number)
  );
