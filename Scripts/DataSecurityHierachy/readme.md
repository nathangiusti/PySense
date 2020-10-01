This script creates a hierarchy style data security structure. 

Use Case:
- We have two companies, Acme and Xyz. Each company has an East and West division. Each division is also broken into sections 1 and 2. 
- We want to be able to assign people such that an administrator for Acme could see all of Acme, while a worker in Xyz East Div 1, would only be able to see the data for Xyz East Div 1. 

Solution Overview:
- Data Security in Sisense will only allow the intersection of all data security rules being applied. 
- This means if we grant permissions for one column and no permissions for another column, the user will see no data. 
- Since it only takes the intersection of the security rules, so long as they are restricted on one column of our security table, 

Security_Table.csv: 
- There are 4 columns, one for each tier of our hierachy and a key column. 
- This is essentially a csv representation of your hierarchy.

Fact.csv:
- This is a fact table for testing our hierarchy. 
- It has one entry for every row in our fact table. 

Security Groups.csv:
- This CSV is the source file that will be read into our script to create the data security. 
- It contains three columns: the name of the group, what level to assign permissions at, and what value to assign. 

Example:
- Acme Admins,1,Acme

This assigns a group called Acme Admins to see all data in the Acme organization.

- Xyz East 1,3, Xyz East 1

This assigns a group called Xyz East 1 to only see the data for Xyz East 1. 

DataSecurityHierarchy.py
- See the comments in the python script for detailed information

Data Security Screen Shot.png
- A screenshot of the finished applied data security
