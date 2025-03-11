SELECT first_name, last_name FROM employees; --список всех сотрудников--
SELECT dept_name FROM departments; --имена департаментов--
SELECT first_name, last_name FROM employees WHERE hire_date > '2020-01-01';--сотрудники нанятые после 2020--
SELECT AVG(salary) AS average_salary FROM salaries;--средняя зп всех сотрудников--
SELECT first_name, last_name, gender FROM employees; --список сотрудников с указанием пола--
SELECT first_name, last_name, birth_date FROM employees WHERE birth_date > '1990-01-01'; --сотрудники родивщиеся после 1990--
SELECT MAX(salary) AS max_salary FROM salaries; --максимальная зп среди сотрудников--
