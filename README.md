# Research Time
Exploring research trends over time. 
## Overview
### Purpose
Research Time is a web-based dashboard that allows users to explore research trends over time. It is targeted towards current researchers or any curious about the history of the Academic World. By understanding historical data, users should be able to glean insight into current trends. 
### Demo 
A demo of Research Time in action is available here on [Media Space Illinois](https://mediaspace.illinois.edu/media/t/1_2aw0g7j1).

## Installation 
### Required software
```
Python		3.10.4
Neo4j		5.3.0
Neo4j-APOC	5.3.0
MongoDB		6.0.4
MySQL		8.0.31
```
### Python
Install Python dependencies by running 
```pip install -r requirements.txt``` 
in this directory, using the virtual environment configuration of your choice. 

### Database configuration
Databases should be configured as defined in the [MP1 Instructions Document](https://docs.google.com/document/d/1SbwBda-Jqmkos8OoftbusvvRgP0j2-Y1VSQhzVSZneE/view). All databases should contain the latest version of the AcademicWorld dataset. Ensure that APOC is installed on the neo4j database.

### MongoDB
In the terminal, launch the MongoDB server by running `mongod --config router.conf`

### Neo4j
Ensure that APOC is installed on the neo4j database. Copy the cypher code from `neo4j/enhance_db.cypher` into the neo4j browser. Run the code, ensuring that it returns without errors. 

### MySQL
Using MySQL Workbench MySQL Command Line Client, connect to the MySQL database configured above  and run the script `sql/setup.sql`.

## Usage
### Launching the Dashboard
Ensure Neo4j, Mongo, and MySQL databases are running.

From this directory, use Python to run the file `launch_dashboard.py`. Connect your web browser to the URL provided in the terminal output, by default `http://localhost:8050/`.

### Interacting with the Dashboard
View the data presented by the six widgets. Many widgets allow additional user interaction. See the table below for instructions for interacting with each widget. 

## Design
Research Time has a simple architecture. A python front-end serves HTML, and sends queries to three databases which run in separate processes. 

For now, the application has been designed to run locally. For simplicity, no APIs were added to isolate databases from the front-end.

### Implementation
Research Time is a [Dash](https://pypi.org/project/dash/) dashboard which serves data from the three databases discussed above. Dash is a python module, it uses [Flask](https://pypi.org/project/Flask/) as its web server and [plotly](https://pypi.org/project/plotly/) for visualization. In addition, we used several helper modules for interfacing with databases. 

### Widget Breakdown

| Widget 	| Objectives 	| Usage 	| DB 	| Technique 	| User Input?| Update DB?|
|--------	|------------	|-------	|-------|---------------	|-------|-------|
|Keyword Popularity over Time|Allow the user to explore how the popularity of keywords has changed over time. |Enter a Keyword, and a Start and End year. Click Search.|MongoDB|view|X||
|University Interests over Time|Allow the user to explore how the research interests of universities have changed over time.|Enter a Keyword, a University, and a Start and End year. Click Search.|MongoDB|index|X||
|Publication Count over Time|Allow the user to view faculty trends, see how their publication numbers have varied with time.|Enter a Researcher and a Start and End year. Click Search.|MongoDB||X||
|Clustered Keywords|Allow the users to view previously clustered keywords for analysis.|View the 25 largest available clusters in the table. Define a new cluster by entering keywords as a comma separated list, and clicking Create. Existing clusters can be expanded by clustering any of their keywords.|Neo4j||X|X|
|Keyword Similarity|Given a keyword, allow the user to see other similar keywords or clusters in terms of common publications. Can be used to inform keyword clustering.|Enter a Keyword and click Search. View the top ten most similar keywords or clusters in terms of common unique publications. Clusters are only counted once even if they share multiple keywords.|Neo4j||X||
|Keyword Audit|Allow the user to rate keywords. Recently rated keywords are displayed.|View the top 10 most recently rated keywords in the table. To rate a new keyword, enter it and a rating. Click Rate. The rating must be an integer between 0 and 5.|MySQL|constraint (check)|X|X|

### Extra-Credit Capabilities 
The Clustered Keywords and Keyword Similarity widgets provide a unique ability to improve data quality. The Keyword Similarity widget allows the user to find keywords that capture the same concept. For example, there is little semantic difference between 'algorithm' and 'algorithms'. The similar keywords can then be clustered. This allows improved data quality by treating these two keywords as one cluster. 

Clustering is implemented in Neo4j as separate `CLUSTER` nodes. This means that the specific keyword choices of the original authors are always preserved. This allows flexibility in working with the original keywords, or the user-enhanced clustered keywords. 


## Contributions 
Michael Miller: Clustered Keywords, Keyword Similarity, Keyword Audit widgets. Written documentation. Estimated time: 20 hours
Michael Minoue: Keyword Popularity over Time, University Interests over Time, Publication Count over Time widgets. Video documentation. Estimated time: 20 hours
