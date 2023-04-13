# Rocket-News
Rocket-News is a web application built using Django and PostgreSQL that allows users to create, modify, and remove news articles. The application provides a dashboard where users can view all the news articles created in the system. Bootstrap has been used in the frontend to make the application responsive and visually appealing.

With Rocket-News, users can easily create news articles and publish them to the website. They can also modify or remove existing articles. The dashboard provides an overview of all the articles in the system, allowing users to quickly find and manage their content.

# Installation
- Clone the repository using the following command <br>
   git clone https://github.com/SaikumarPole/Rocket-News.git <br>
- Create a virtual environment and activate it <br>
  python -m venv env <br>
  source env/bin/activate <br>
- Install the dependencies <br>
  pip install -r requirements.txt <br>
- Run the migrations<br>
  python manage.py migrate News --database=default <br>
- Start the development server <br>
  python manage.py runserver <br>
# Lisense
  This project is licensed under the MIT License 
