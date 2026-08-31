# python_fullstack_1
ctrl+j
git add .
git commit -m "html"
git push



gmeet code - wdyiijnhat



https://github.com/SriramMurugesan/python_fullstack_1

# html->hyper text markup language
structure of the web page
# css->cascading style sheet
giving design and cosmetics to your web page
# js->javascript
bring the functionality to your web page
# python-> backend
creates api and backend logics will be created here
# SQL 

DB- postgresql, mariadb, mysql,oracle

https://www.sqltutorial.org/playground/



https://www.kaggle.com/learn/python

# constraints 
1. Primary key -- Roll no(unique value and should not be null)

2. Foreign key -- relationship between tables(primary key of another table)

3. Not null

4. Unique

5. Check

6. Default 

 # DDL - Data Definition Language-> structure of table
create, alter, drop, truncate
# DML - Data Manipulation Language-> data manipulation  
insert, update, delete
# DCL - Data Control Language-> security permissions
revoke, grant
# TCL - Transaction Control Language-> transaction
commit, rollback
# DQL - Data Query Language-> query
select

# DDL - commands(practice)
--create table student(student_id int primary key, name varchar(50), email varchar(50), branch varchar(10));

--create table branch (branch_id int primary key, branch_name varchar(50));

--alter table branch rename to departments

--alter table students rename column branch to branch_id;

--alter table students column branch_id type int;

--alter table students add constraint constraint_name foreign key(branch_id) references departments(branch_id);

drop table students;

truncate table students;

# DML - commands(practice)
--insert into departments(branch_id, branch_name) values(1, 'Computer Science');

--insert into students(student_id, name, email, branch_id) values(1, 'John', 'john@example.com', 1);

update students set name = 'John' where student_id = 1;

delete from students where student_id = 1;

# questions fro employee database
-- select * from employees where salary >20000;
-- select * from employees where department_id=10;
-- select first_name , last_name from employees where salary <10000;
select * from employees where manager_id is not null ; 
-- return employees who have salry greater than 20000
-- return whose department id is 10
-- return first name and last name of employees whose salary less than 10000
-- return employees whose manager_id is null
# and or not
select * from employees where salary >50000 and department_id=10;
-- return employees who have salary greater than 50000 and department id is 10
select * from employees where salary >50000 or department_id=10;
-- return employees who have salary greater than 50000 or department id is 10
select * from employees where salary >50000 and department_id not in (10,20,30);
-- return employees who have salary greater than 50000 and not in 10 dept 
# in not in
select * from employees where department_id in (10,20,30);
select * from employees where department_id not in (10,20,30);
-- return emplyoees whose dept id are 10,20,30
-- return emplyoees whose dept id are not in 10,20,30
# pattern matching
select * from employees where first_name like 'A%';
select * from employees where first_name like '%A';
select * from employees where first_name like '%A%';
-- return employees whose name starts with A
-- return employees whose name ends with A
-- return employees whose name contains A

# sort and ordering
select * from employees order by salary asc;
select * from employees order by salary desc;
-- return employees sorted by salary in ascending order
-- return employees sorted by salary in descending order
# count , sum, avg, min, max
select count(*) from employees;
select count(*) from employees group by department_id;
select count(*) from employees group by department_id order by count(*) desc;
-- return count of employees
-- return count of employees in each department
-- return count of employees in each department and order by count in descending order
# Group by and having
select count(*) from employees group by department_id having count(*) > 1;
-- return count of employees in each department and order by count in descending order
select * from employees where department_id in (select department_id from employees group by department_id having count(*) > 1);
-- return count of employees in each department and order by count in descending order and salary greater than 50000

## Joins 
# inner join
select * from employees join departments on employees.department_id = departments.department_id;
select * from employees join departments on employees.department_id = departments.department_id where salary >50000;
-- return employees with their department names
-- return employees with their department names and salary greater than 50000


create env: python3 -m venv env
activate env: . env/bin/activate
deactivate env: deactivate