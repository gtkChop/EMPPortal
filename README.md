## Employee Management Portal
###### State: Development

The objective of this application is to manage all employees easily as possible. 
Moreover, this application will also contains, project management, Task Management, Workflow processes for HR and Projects.


#### Planned High Level Functionalities -

* HR Management (extension - 1)
    * All employees details
    * Apply leaves
    * Fill daily time sheets
    * Workflow process for HR
    * To do list
    
* Project Management (extension - 2)
    * Departments
    * All projects details
    * Team members information
    * Work flow process for projects

* Employee Task Management (extension - 3)
    * Fill task done every day
    * Task Dashboard for employee
    

* Sprint Board for each project (extension - 4)
    * Sprint tracker
    * Sprint Dashboard
    
* Admin dashboards (extension - 5):
    * Department, Employees and Project summary

* Project Manager Dashboards (extension - 6):
    * Employees Tasks and Current Sprint dashboard
    
#### Current Progress:
Working on Extension 1

#### How To Run the Application? (Guide):

###### Prerequisite:
    * Install Docker
    * Install Docker Compose
    

* Clone this Repository
* Run command ```Make initial-build``` - (Check Makefile) - use this for the first time, otherwise use ``` Make build ``` command.
* Run command ```Make superuser``` - (Check Makefile)
    * Date entered should be ISO format (yyyy-mm-dd)
    * Country should be country code e.g. in (India), ie (Ireland)
    * username should be all in small letters
* Once superuser is created generate your api key and note down your api key
    * Run command ```Make bash``` - (Check Makefile)
    * Run command ```python ./app/manage.py generate_api_key <supersuser email id>```
    
* Load a sample data (For development):
    * Open file load_data.py (In Emapp folder) and add you API key.
    * Run command ``` Make build```
    * Run command ``` Make initial-data```
    * Visit your http://localhost:8800/login
 
* For UI/css changes:
    * make changes in folder webpack/src/css or webpack/src/js
    * changes will be reflected automatically inside the container.
    
* To check the logs: Run command ``` Make logs ```


Hints For Dev:

* Create your own branch for each feature.
* If it looks good merge to branch dev.
* To merge to master - Raise a pull requests.

 



