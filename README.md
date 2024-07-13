# Python_Messaging_System with Celery and RabbitMQ

This is a Flask-based messaging system that uses Celery and RabbitMQ for background task processing. The system provides endpoints for sending emails and logging requests.

## Features

- Send emails asynchronously using Celery and RabbitMQ.
- Log requests to a log file.
- View log file contents via an endpoint.

## Requirements

- Python 3.6+
- Flask
- Celery
- RabbitMQ
- smtplib (standard library)
- email.mime (standard library)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/aeeshah/Python_Messaging_System.git
    cd your-repo-name
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install flask celery
    ```

4. **Ensure RabbitMQ is installed and running:**

    ```sh
    sudo apt-get install rabbitmq-server
    sudo systemctl start rabbitmq-server
    sudo systemctl enable rabbitmq-server
    ```

5. **Create the log file and set the necessary permissions:**

    ```sh
    sudo touch /var/log/messaging_system.log
    sudo chmod 666 /var/log/messaging_system.log
    ```

## Configuration

- Update the `SENDER_EMAIL` and `SENDER_PASSWORD` variables in `app.py` with your SMTP server credentials.

## Running the Application

1. **Start the Celery worker:**

    ```sh
    celery -A app.celery worker --loglevel=info
    ```

2. **Run the Flask application:**

    ```sh
    flask run --port=8000
    ```

3. **Access the application:**

    The application will be running on `http://localhost:8000`.

## Endpoints

- **Send Email:**

    ```
    GET /?sendmail=recipient@example.com
    ```

    Queue an email to be sent to the specified recipient.

- **Log Request:**

    ```
    GET /?talktome
    ```

    Log the current time to the log file.

- **View Logs:**

    ```
    GET /logs
    ```

    Retrieve the contents of the log file.

## Exposing Your Application with ngrok

To make your local Flask application accessible over the internet, you can use ngrok.

1. **Install ngrok:**

    Download ngrok from [ngrok.com](https://ngrok.com/) and follow the installation instructions.

2. **Expose your application:**

    Open a new terminal window and run:

    ```sh
    ngrok http 8000
    ```

This will generate a public URL that tunnels to your local server running on port 8000. You'll see an output like this:
Use the generated `https://<ngrok_subdomain>.ngrok.io` URL to access your Flask application over the internet.

  
## Troubleshooting

- Ensure RabbitMQ is running: `sudo systemctl status rabbitmq-server`
- Check the log file for errors: `/var/log/messaging_system.log`
- Verify the SMTP server settings and credentials.
