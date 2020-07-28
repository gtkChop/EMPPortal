import requests
import json

url_create = "http://127.0.0.1:8000/etmapp/api/create_employee"
url_delete = "http://127.0.0.1:8000/etmapp/api/delete_employee"
headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': 'application/json',
    "API-KEY": "OZn5Q5No.7uSJpq7EeN2gUZrgS72Zfz0IrnLuxugT"
}

data = [
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Kenny",
        "middle_name": "l",
        "last_name": "John",
        "work_email": "kenny_john@gmail.com",
        "nationality_code": "in",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
               "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
               "REST APIs, web-based applications and AI technologies like chatbots.",
        "contact_ph": "0899518706",
        "graduation_level": "",
        "employee_id": "ETM-1234PX",
        "joining_date": "2018-10-01",
        "position": "Senior Software Developer",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "work_ph": "",
        "skills": ["management"],
        "experience": "4",
        "role": "member",
        "social_linkedin": "https://www.linkedin.com/in/swaroop-shubhakrishna/"
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "John",
        "last_name": "Steve",
        "work_email": "john_steve@gmail.com",
        "nationality_code": "in",
        "employee_id": "ETM-1235PX",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "joining_date": "2018-10-01",
        "position": "Senior Software Developer",
        "contact_ph": "0899518706",
        "role": "hr",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
                       "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
                       "REST APIs, web-based applications and AI technologies like chatbots.",
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Emily",
        "last_name": "Kevin",
        "work_email": "emily@gmail.com",
        "nationality_code": "in",
        "employee_id": "ETM-1236PX",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "joining_date": "2018-10-01",
        "position": "Human Resource",
        "contact_ph": "0899518706",
        "role": "hr",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
                       "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
                       "REST APIs, web-based applications and AI technologies like chatbots.",
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Vikram",
        "middle_name": "l",
        "last_name": "Singh",
        "work_email": "vikram@gmail.com",
        "nationality_code": "in",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
               "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
               "REST APIs, web-based applications and AI technologies like chatbots.",
        "contact_ph": "0899518706",
        "graduation_level": "",
        "employee_id": "ETM-1237PX",
        "joining_date": "2018-10-01",
        "position": "Director",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "work_ph": "",
        "skills": ["Management"],
        "experience": "4",
        "role": "admin",
        "social_linkedin": "https://www.linkedin.com/in/swaroop-shubhakrishna/"
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Neha",
        "middle_name": "m",
        "last_name": "choudry",
        "work_email": "neha@gmail.com",
        "nationality_code": "ie",
        "contact_ph": "0899518706",
        "graduation_level": "",
        "employee_id": "DLX-EMP5",
        "joining_date": "2018-10-01",
        "position": "Manager",
        "bio": "Hey, bio",
        "work_country_code": "ie",
        "work_address": "Galway Eyre Suqare",
        "work_ph": "",
        "skills": ["management", 'python'],
        "experience": "4",
        "role": "member"
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Paul",
        "last_name": "Romera",
        "work_email": "paulromera_kenny_john@gmail.com",
        "nationality_code": "in",
        "employee_id": "ETM-1239PX",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "joining_date": "2018-10-01",
        "position": "Team Lead",
        "contact_ph": "0899518706",
        "role": "member",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
                       "and open data applications.",
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Yoie",
        "middle_name": "l",
        "last_name": "Mi",
        "work_email": "yoie_mi_@gmail.com",
        "nationality_code": "jp",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
               "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
               "REST APIs, web-based applications and AI technologies like chatbots.",
        "contact_ph": "0899518706",
        "graduation_level": "",
        "employee_id": "ETM-12312PX",
        "joining_date": "2018-10-01",
        "position": "Junior Software Developer",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "work_ph": "",
        "skills": ["python", "java"],
        "experience": "4",
        "role": "member",
        "social_linkedin": "https://www.linkedin.com/in/swaroop-shubhakrishna/"
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Ajay",
        "middle_name": "l",
        "last_name": "Dev",
        "work_email": "ajay@gmail.com",
        "nationality_code": "in",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
               "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
               "REST APIs, web-based applications and AI technologies like chatbots.",
        "contact_ph": "0899518706",
        "graduation_level": "",
        "employee_id": "ETM-12322PX",
        "joining_date": "2018-10-01",
        "position": "Senior Software Developer",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "work_ph": "",
        "skills": ["management", "java", "ETL"],
        "experience": "4",
        "role": "member",
        "social_linkedin": "https://www.linkedin.com/in/swaroop-shubhakrishna/"
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Tommy",
        "middle_name": "j",
        "last_name": "Tommy",
        "work_email": "tom@gmail.com",
        "nationality_code": "in",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
               "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
               "REST APIs, web-based applications and AI technologies like chatbots.",
        "contact_ph": "0899518706",
        "graduation_level": "",
        "employee_id": "ETM-1233PX",
        "joining_date": "2018-10-01",
        "position": "Senior Software Developer",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "work_ph": "",
        "skills": ["management", "R", "Machine Learning", "Natural Language Processing"],
        "experience": "4",
        "role": "member",
        "social_linkedin": "https://www.linkedin.com/in/swaroop-shubhakrishna/"
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Niket",
        "middle_name": "j",
        "last_name": "l",
        "work_email": "niket@gmail.com",
        "nationality_code": "ie",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
               "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
               "REST APIs, web-based applications and AI technologies like chatbots.",
        "contact_ph": "0899518706",
        "graduation_level": "",
        "employee_id": "ETM-1243PX",
        "joining_date": "2018-10-01",
        "position": "Senior Software Developer",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "work_ph": "",
        "skills": ["management", "R", "Machine Learning", "Natural Language Processing"],
        "experience": "4",
        "role": "member",
        "social_linkedin": "https://www.linkedin.com/in/swaroop-shubhakrishna/"
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Naveen",
        "middle_name": "j",
        "last_name": "J",
        "work_email": "naveen@gmail.com",
        "nationality_code": "in",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
               "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
               "REST APIs, web-based applications and AI technologies like chatbots.",
        "contact_ph": "0899518706",
        "graduation_level": "",
        "employee_id": "ETM-1245PX",
        "joining_date": "2018-10-01",
        "position": "Senior Software Developer",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "work_ph": "",
        "skills": ["management", "R", "Machine Learning", "Natural Language Processing"],
        "experience": "4",
        "role": "member",
        "social_linkedin": "https://www.linkedin.com/in/swaroop-shubhakrishna/"
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Jerrard",
        "middle_name": "j",
        "last_name": "romio",
        "work_email": "jerrard@gmail.com",
        "nationality_code": "in",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
               "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
               "REST APIs, web-based applications and AI technologies like chatbots.",
        "contact_ph": "0899518706",
        "graduation_level": "",
        "employee_id": "ETM-12436PX",
        "joining_date": "2018-10-01",
        "position": "Senior Software Developer",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "work_ph": "",
        "skills": ["management", "R", "Machine Learning", "Natural Language Processing"],
        "experience": "4",
        "role": "member",
        "social_linkedin": "https://www.linkedin.com/in/swaroop-shubhakrishna/"
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "laura",
        "middle_name": "l",
        "last_name": "Dev",
        "work_email": "laura@gmail.com",
        "nationality_code": "in",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
               "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
               "REST APIs, web-based applications and AI technologies like chatbots.",
        "contact_ph": "0899518706",
        "graduation_level": "",
        "employee_id": "ETM-1278PX",
        "joining_date": "2018-10-01",
        "position": "Senior Software Developer",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "work_ph": "",
        "skills": ["management", "java", "ETL"],
        "experience": "4",
        "role": "member",
        "social_linkedin": "https://www.linkedin.com/in/swaroop-shubhakrishna/"
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Jonny",
        "middle_name": "l",
        "last_name": "jonny",
        "work_email": "jonny@gmail.com",
        "nationality_code": "in",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
               "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
               "REST APIs, web-based applications and AI technologies like chatbots.",
        "contact_ph": "0899518706",
        "graduation_level": "",
        "employee_id": "ETM-11322PX",
        "joining_date": "2018-10-01",
        "position": "Senior Software Developer",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "work_ph": "",
        "skills": ["management", "java", "ETL"],
        "experience": "4",
        "role": "member",
        "social_linkedin": "https://www.linkedin.com/in/swaroop-shubhakrishna/"
    },
    {
        "date_of_birth": "1992-07-09",
        "first_name": "Gareth",
        "middle_name": "l",
        "last_name": "Junior",
        "work_email": "gareth@gmail.com",
        "nationality_code": "in",
        "bio": "An experienced software developer and researcher with a passion for developing AI tools and linked "
               "and open data applications. Proven ability in developing Open Source Management System (CKAN), "
               "REST APIs, web-based applications and AI technologies like chatbots.",
        "contact_ph": "0899518706",
        "graduation_level": "",
        "employee_id": "ETM-1279PX",
        "joining_date": "2018-10-01",
        "position": "Senior Software Developer",
        "work_country_code": "ie",
        "work_address": "Dublin",
        "work_ph": "",
        "skills": ["management", "java", "ETL"],
        "experience": "4",
        "role": "member",
        "social_linkedin": "https://www.linkedin.com/in/swaroop-shubhakrishna/"
    },
]


def create_employees():

    for item in data:
        resp = requests.post(
            url_create,
            headers=headers,
            data=json.dumps(item)
        )
        print(resp.json())
        print(resp.status_code)
    print("Done")


def delete_all_data():
    for item in data:
        resp = requests.post(
            url_delete,
            headers=headers,
            data=json.dumps({
                "id": item.get('employee_id')
            })
        )
        print(resp.json())
        print(resp.status_code)
    print("Done Deleting")


if __name__ == "__main__":
    create_employees()
    #delete_all_data()
