--#6
/*
List the Company name and the number of calls for those companies with more than 18 calls. 
*/
SELECT Company_name, COUNT(*) AS cc FROM Issue JOIN Caller ON Issue.Caller_id = Caller.Caller_id JOIN Customer ON Caller.Company_ref = Customer.Company_ref
GROUP BY Company_name
HAVING COUNT(*) > 18

--#7
/*
Find the callers who have never made a call. 
Show first name and last name
*/
SELECT First_name, Last_name FROM Caller LEFT JOIN Issue ON Caller.Caller_id = Issue.Caller_id
WHERE Call_date IS NULL

--#8
/* 
For each customer show: Company name, contact name, 
number of calls where the number of calls is fewer than 5
*/
SELECT Customer.Company_name, first_name, last_name, nc FROM Customer JOIN Caller ON Customer.Contact_id = Caller.Caller_id JOIN (SELECT Company_name, COUNT(Call_ref) AS nc FROM Issue JOIN Caller ON Issue.Caller_id = Caller.Caller_id JOIN Customer ON Caller.Company_ref = Customer.Company_ref
GROUP BY Customer.Company_name, Caller.Company_ref
HAVING COUNT(Call_ref) < 5) a ON Customer.Company_name = a.Company_name
ORDER BY nc DESC

--#9
/*
For each shift show the number of staff assigned. 
Beware that some roles may be NULL and that the same person might have been assigned to multiple roles 
(The roles are 'Manager', 'Operator', 'Engineer1', 'Engineer2'). 
*/
SELECT Shift_date, Shift_type, 
CASE
WHEN Manager IS NULL THEN 0
ELSE 1
END +
CASE
WHEN Operator IS NULL THEN 0
WHEN Operator = Manager THEN 0
ELSE 1
END +
CASE
WHEN Engineer1 IS NULL THEN 0
WHEN Engineer1 = Manager THEN 0
WHEN Engineer1 = Operator THEN 0
ELSE 1
END +
CASE
WHEN Engineer2 IS NULL THEN 0
WHEN Engineer2 = Manager THEN 0
WHEN Engineer2 = Operator THEN 0
WHEN Engineer2 = Engineer1 THEN 0
ELSE 1
END AS cw
FROM Shift

--#10
/*
Caller 'Harry' claims that the operator who took his most recent call was abusive and insulting. 
Find out who took the call (full name) and when.
*/
SELECT Staff.first_name, Staff.last_name, Issue.Call_date FROM Issue JOIN Staff ON Issue.Taken_by = Staff.Staff_code
WHERE Issue.Call_date = (SELECT MAX(Issue.Call_date) FROM Issue JOIN Caller ON Issue.Caller_id = Caller.Caller_id
WHERE first_name = 'Harry')





