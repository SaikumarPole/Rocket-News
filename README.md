# Rocket-News
Rocket-News is a web application built using Django and PostgreSQL that allows users to create, modify, and remove news articles. The application provides a dashboard where users can view all the news articles created in the system. Bootstrap has been used in the frontend to make the application responsive and visually appealing.

With Rocket-News, users can easily create news articles and publish them to the website. They can also modify or remove existing articles. The dashboard provides an overview of all the articles in the system, allowing users to quickly find and manage their content.

# Installation
- Clone the repository using the following command <br> 
```
   git clone https://github.com/SaikumarPole/Rocket-News.git
```
 Create a virtual environment and activate it 

```
- python -m venv env 
  source env/bin/activate
```
- Install the dependencies 

```
  pip install -r requirements.txt 
```
- Run the migrations
```
  python manage.py migrate News --database=default 
```
- Start the development server 
```
  python manage.py runserver 
```
# Lisense
  This project is licensed under the MIT License 
