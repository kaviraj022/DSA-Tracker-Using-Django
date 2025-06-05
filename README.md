‼️Switch to code or raw text for better alignment‼️
Required Packages: Pymysql, Django
Languages: HTML, CSS, JS, Python
Database: MySQL
Hashing algorithm for passwords: Default Django hashing algorithm(PBKDF2 algorithm with a SHA256 hash)
Tables Structure:

mysql> use dsa_tracker;

mysql> SHOW TABLES;
+-----------------------+
| Tables_in_dsa_tracker |
+-----------------------+
| problems              |
| usernotes             |
| userprogress          |
| users                 |
+-----------------------+

mysql> DESCRIBE Users;
+---------------+----------------------+------+-----+---------+----------------+
| Field         | Type                 | Null | Key | Default | Extra          |
+---------------+----------------------+------+-----+---------+----------------+
| id            | int                  | NO   | PRI | NULL    | auto_increment |
| username      | varchar(100)         | NO   | UNI | NULL    |                |
| email         | varchar(100)         | NO   | UNI | NULL    |                |
| password_hash | varchar(255)         | NO   |     | NULL    |                |
| role          | enum('admin','user') | NO   |     | user    |                |
+---------------+----------------------+------+-----+---------+----------------+

mysql> DESCRIBE Problems;
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int          | NO   | PRI | NULL    | auto_increment |
| topic         | varchar(100) | NO   |     | NULL    |                |
| difficulty    | varchar(50)  | NO   |     | NULL    |                |
| name          | varchar(255) | NO   | UNI | NULL    |                |
| youtube_link  | varchar(255) | YES  |     | NULL    |                |
| practice_link | varchar(255) | YES  |     | NULL    |                |
+---------------+--------------+------+-----+---------+----------------+

mysql> DESCRIBE UserNotes;
+------------+------+------+-----+---------+----------------+
| Field      | Type | Null | Key | Default | Extra          |
+------------+------+------+-----+---------+----------------+
| id         | int  | NO   | PRI | NULL    | auto_increment |
| user_id    | int  | NO   | MUL | NULL    |                |
| problem_id | int  | NO   | MUL | NULL    |                |
| note       | text | YES  |     | NULL    |                |
+------------+------+------+-----+---------+----------------+

mysql> DESCRIBE UserProgress;
+--------------+------------+------+-----+---------+----------------+
| Field        | Type       | Null | Key | Default | Extra          |
+--------------+------------+------+-----+---------+----------------+
| id           | int        | NO   | PRI | NULL    | auto_increment |
| user_id      | int        | NO   | MUL | NULL    |                |
| problem_id   | int        | NO   | MUL | NULL    |                |
| is_completed | tinyint(1) | NO   |     | 0       |                |
+--------------+------------+------+-----+---------+----------------+
Custom Decorators for admin and user dashboard navigation
Admins: Superadmin(can create admins as well as delete any users and modify the problems ,
        Admin(can delete users and modify the problems cant delete other admins or Superadmin)
