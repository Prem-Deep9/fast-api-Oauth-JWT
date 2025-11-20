# ToDoApp

## Running the Application

Follow these steps to set up and run the application:

### Step 1: Install Prerequisites
1. Install **Docker** from [Docker's official website](https://www.docker.com/products/docker-desktop).
2. Install **pgAdmin** from [pgAdmin's official website](https://www.pgadmin.org/download/).

### Step 2: Start the PostgreSQL Database
1. Run Docker Desktop and PGAdmin on your system.
2. Navigate to the project directory containing the `docker-compose.yml` file.
3. Run the following command to start the PostgreSQL container: docker-compose up -d

### Step 3: Add the Database to pgAdmin
1. Add a new server in pgAdmin:
    Right-click on Servers in the left-hand panel and select Create > Server....
2. In the General tab:
    Name: Enter a name for the server (e.g., ToDoAppDB).
3. In the Connection tab:
    Host name/address: localhost (or 127.0.0.1).
    Port: 5432.
    Username: AppSuperUser.
    Password: s3cret.
    Click Save.
You can comeback and see all the tables and data in here.

### Step 4: Add the DATABASE_URL Environment Variable
Create a .env file if doesnt exist and in the .env file Set the DATABASE_URL environment variable.
A sample connection string for the ToDoAppDB database would look like this:
DATABASE_URL=postgresql://AppSuperUser:s3cret@localhost:5432/ToDoAppDB

Install Python on your machine
   - Download and install from [python.org](https://python.org)
   - Version is mentioned in `.python-version` file
   - Ensure Python is added to your system PATH

Install uv globally
   - Run `pip install uv`
   - Run `uv --version` to check if uv is installed
   - Run `uv venv` to create a virtual environment and activate it

For new projects, you can use `uv init` to create a new project with uv.
uv add to install new libraries and add new dependencies to the pyproject.toml file.

Install dependencies
   - Run `uv sync` to install all dependencies

Run `uv run fastapi run main.py` to run the app in prod
Run `uv run fastapi dev main.py` to run the app in dev