# E-Learning API

The goal of this project is to facilitate the creation and consumption of learning materials. By streamlining the process, I aim to empower educators and learners alike. Ultimately, this project seeks to bridge gaps in learning opportunities and promote continuous education.


## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- This API allows two kind of users **Content Creators** and **Learners**
- **Content Creators** can create and manage Programs, Courses, Modules, Medias and Quizzes.
- **Content Creators** can also decide who they want to allow access to thier content by accpeting or rejecting applications to thier courses or programs.
- **Content Creators** can set deadlines for Courses and programs.
- **Learners** can apply to Courses and Programs. If accepted can view the details of the Modules.
- Enrolled **Learners** can access Quizzes and submit answers and get results for their work.
- Highlight any unique aspects or functionalities.
- **Learners** can apply to a single course that might be part of a program.
- **Learners** who apply to a program that contains many courses will be automatically enrolled in all the courses if accepted.
- **Learners** make progress in a course by compeleting Modules and the Quizzes they contain within the deadlines specified (if it applies).
- **Learners** make progress in a program by compeleting Courses they contain within the deadlines specified (if it applies).
- **Learners** can take quizes multiple times. The best score will be recoreded.
- **Learners** enrolled in multiple programs can make progress in all the Programs when completing Courses that are part of multiple programs.

## Technologies

- **Programming Language**: Python
- **Framework**: Django
- **REST Framework**: Django REST Framework
- **Authentication**: SimpleJWT (for token authentication)
- **Database**: MySQL
- **Deployment**: PythonAnywhere
- **API Testing**: Postman

## Installation

### Prerequisites

- Python 3.10
- Django 5.1 or later
- Django Filter 24.3
- Django Rest Framework 3.15.2
- Django Rest Framework simpleJWT 5.3.1
- mysqlclient 2.2.4
- pillow 10.4.0
- pyJWT 2.9.0
- sqlparse 0.5.1
- typing_extensions 4.12.2



### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/abenezer-s/e_learning_api.git
   cd yourproject

2. Create a virtual environment:

```bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:

```bash

pip install -r requirements.txt
```
4. Set up the database:

```bash

python manage.py migrate
```
5. Create a superuser (optional):

```bash

python manage.py createsuperuser
```
## Usage

### Instructions on how to run the project:

Start the development server:

```bash
python manage.py runserver
```

    Open your web browser and go to http://127.0.0.1:8000/.

Important endpoints

| Endpoint          | Method | Description                          |
|-------------------|--------|--------------------------------------|
| `/api/users/`     | GET    | Retrieve a list of all users.       |
| `/api/program/`  | GET     | Retrieve a list of all programs.       |
| `/api/course/`   | GET     | Retrieve a list of all courses.       |
| `/api/module/`   | GET     | Retrieve a list of all modules.       |
| `/api/quiz/`     | GET     | Retrieve a list of all quizzes.       |

The comprehensive list of endpoints can be found [here](https://docs.google.com/document/d/1IhmwAIoYWrmaBvRMIEl_o1ELL-5gma1MJoyTCvvac4w/edit?usp=sharing)  

## Running Tests

This project includes a suite of tests for the API that can be run using [Postman](https://www.postman.com/). These tests help verify that the API endpoints are functioning correctly.

### Prerequisites

- Ensure you have [Postman](https://www.postman.com/downloads/) installed.
- Import the collection file provided with this project (see below).

### Postman Collection

This project includes a Postman collection for testing the API. You can access the collection using the link below:

[View Postman Collection](https://www.postman.com/avionics-meteorologist-79642757/workspace/e-learning-api-workspace/collection/38735947-0ba70c38-9bf2-4cc1-86f7-59266cd7e389?action=share&creator=38735947)

### How to Use

1. Click on the link above to open the collection in Postman.
2. Import the collection into your Postman workspace.
3. Ensure you set any necessary environment variables.
4. Run the requests as needed.

### Note

Please ensure that you include all necessary parameters when making requests. Missing parameters can lead to unexpected errors or incomplete responses.




## Contributing

Guidelines for contributing to the project.

    Fork the repository.
    

Create your feature branch:

``` bash
git checkout -b feature/YourFeature
```
Commit your changes:

``` bash
git commit -m "Add your message"
```
Push to the branch:

```bash 
git push origin feature/YourFeature
```
    

## License


## Acknowledgments

This project uses [Django](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/) which provided a solid foundation for building the API.