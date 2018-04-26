--#1
/*
Provide a query showing Customers (just their full names, customer ID and country) 
who are not in the US.
*/
SELECT FirstName, LastName, CustomerId, Country FROM customers 
WHERE Country != 'United States';

--#2
/*
Provide a query only showing the Customers from Brazil.
*/
SELECT FirstName, LastName, CustomerId, Country FROM customers 
WHERE Country = 'Brazil';

--#3
/*
Provide a query showing the Invoices of customers who are from Brazil. 
The resultant table should show the customer's full name, Invoice ID, 
Date of the invoice and billing country.
*/
SELECT customers.FirstName, customers.LastName, invoices.invoiceid, invoices.invoiceDate, invoices.BillingCountry FROM invoices JOIN customers ON invoices.CustomerId = customers.CustomerId
WHERE customers.Country = 'Brazil';

--#4
/*
Provide a query showing only the Employees who are Sales Agents.
*/
SELECT FirstName, LastName FROM employees WHERE Title = 'Sales Support Agent';

--#5
/* Provide a query showing a unique list of billing countries from the Invoice table.
*/

SELECT DISTINCT BillingCountry FROM invoices;

--#6
/*
This is the same as #3...
*/

--#7
/*
Provide a query that shows the invoices associated with each sales agent. 
The resultant table should include the Sales Agent's full name.
*/

SELECT e.FirstName, e.LastName, i.InvoiceId FROM employees e JOIN customers c ON e.EmployeeID = c.SupportRepId JOIN invoices i ON c.CustomerID = i.CustomerID;

