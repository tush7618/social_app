# Social Networking Application

A Django Rest Framework (DRF) based social networking application with functionalities for user authentication, friend requests, and user search. 

## Features

- User Signup and Login
- Search Users by Email or Name
- Send, Accept, and Reject Friend Requests
- List Friends and Pending Friend Requests

## Technologies Used

- Python
- Django
- Django Rest Framework
- PostgreSQL

## Installation

1. **Clone the Repository**

    ```bash
    https://github.com/tush7618/social_app.git
    cd social_app
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply Migrations**

    ```bash
    python manage.py migrate
    ```
5. **Run the Development Server**

    ```bash
    python manage.py runserver 8000
    ```

## API Endpoints

### User Signup

- **Endpoint**: `/api/v1/signup/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "email": "user@example.com",
        "password": "yourpassword",
	"first_name": "user",
    	"last_name": "name"
    }
    ```
- **Response**: `201 Created` on success, `400 Bad Request` on error.

### User Login

- **Endpoint**: `/api/v1/login/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "email": "user@example.com",
        "password": "yourpassword"
    }
    ```
- **Response**: `200 OK` with token on success, `401 Unauthorized` on error.

### Search Users

- **Endpoint**: `/api/v1/search/`
- **Method**: `GET`
- **Query Parameters**: `search=keyword`
- **Request Header**: `Authorization: Token <your_token_here>`
- **Response**: `200 OK` with a list of users.

### Send Friend Request

- **Endpoint**: `/api/v1/friend-requests/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "receiver_email":"user@example.com"
    }
    ```
- **Request Header**: `Authorization: <your_token_here>`
- **Response**: `201 Created` on success, `400 Bad Request` on error.

### Accept Friend Request

- **Endpoint**: `/api/v1/friend-request-response/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "friend_request_id": 12,
    	"response":"accept"
    }
    ```
- **Request Header**: `Authorization: <your_token_here>`
- **Response**: `200 OK` on success, `400 Bad Request` on error.

### Reject Friend Request

- **Endpoint**: `/api/v1/friend-request-response/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "friend_request_id": 12,
    	"response":"reject"
    }
    ```
- **Request Header**: `Authorization: <your_token_here>`
- **Response**: `200 OK` on success, `400 Bad Request` on error.

### List Friends

- **Endpoint**: `/api/v1/friends/`
- **Method**: `GET`
- **Request Header**: `Authorization: <your_token_here>`
- **Response**: `200 OK` with a list of friends.

### List Pending Friend Requests

- **Endpoint**: `/api/v1/pending-requests/`
- **Method**: `GET`
- **Request Header**: `Authorization: <your_token_here>`
- **Response**: `200 OK` with a list of pending requests.

## Troubleshooting

- Ensure that the token is included in the `Authorization` header as `<your_token_here>`.
- Check the DRF logs for detailed error messages if something is not working.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Django and Django Rest Framework for providing powerful tools to build RESTful APIs.
- Postman for API testing and debugging.

Feel free to adjust the README according to your project's specifics and add any additional information that might be relevant.
