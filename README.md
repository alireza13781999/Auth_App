
# Django Phone Number Registration and Login System

This is a Django-based application that implements user registration and login functionality using phone numbers. The application includes features like:
- User registration with phone number verification code.
- Login system with phone number/password.
- IP blocking for multiple failed login attempts or incorrect verification code entries.


## Requirements
- Dependencies listed in `requirements.txt`

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/alireza13781999/Auth_App.git
cd Auth_App
```


### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Apply Migrations

```bash
python manage.py migrate
```


### Step 4: Start the Development Server

```bash
python manage.py runserver
```

You can access the application at `http://127.0.0.1:8000/`.

## API Endpoints

### 1. **Send Code**

- **URL**: `/user/send-code/`
- **Method**: `POST`
- **Payload**:
    ```json
    {
        "phone_number": "1234567890"
    }
    ```

- **Response**: 
    ```json
    {
        "message": "Verification code sent.",
        "code": "123456"
    }
    ```

### 2. **Verify Code**

- **URL**: `/user/verify-code/`
- **Method**: `POST`
- **Payload**:
    ```json
    {
        "phone_number": "1234567890",
        "code": "123456"
    }
    ```

- **Response**:
    ```json
    {
        "message": "Phone number verified successfully"
    }
    ```

### 3. **Register**

- **URL**: `/user/register/`
- **Method**: `POST`
- **Payload**:
    ```json
    {
        "first_name": "Alireza",
        "Last_name": "Nemati",
        "email": "alireza.nemati@me.com",
        "password": "securepassword"
    }
    ```

- **Response**:
    ```json
    {
        "message": "Registration complete and logged in successfully"
    }
    ```

### 4. **Login**

- **URL**: `/user/login/`
- **Method**: `POST`
- **Payload**:
    ```json
    {
        "phone_number": "1234567890",
        "password": "securepassword"
    }
    ```

- **Response**:
    ```json
    {
        "message": "Login successful"
    }
    ```

## Testing with Postman
[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/7293653-66a4dfc7-5871-4492-b829-8fd64c9af1ec?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D7293653-66a4dfc7-5871-4492-b829-8fd64c9af1ec%26entityType%3Dcollection%26workspaceId%3Dc4d57c25-8af2-473a-a76f-4968935f743c)
