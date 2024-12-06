# QuickCRUD

QuickCRUD is a command-line interface (CLI) tool designed to automatically generate FastAPI APIs from a provided SQL schema. By using this tool, developers can quickly generate CRUD (Create, Read, Update, Delete) operations for each table in the database schema, saving valuable time when setting up backend APIs.

## Features

- Automatically generates FastAPI CRUD operations for SQL schema tables.
- Supports PostgreSQL, MySQL, and SQLite databases.
- Generates API routes for basic operations: GET, POST, PUT, DELETE.
- Creates a ready-to-use Docker Compose setup with two containers: one for the FastAPI application and another for the database.

## Current Status

As of now, **QuickCRUD** is in its **early stages**. 

## Installation

To install **QuickCRUD**:


```
pip install quickcrud
```

## Usage

To generate FastAPI APIs from your SQL schema, simply run the following command:

```
quickcrud --schema path/to/your/schema.sql --db-type postgres
```

Replace `postgres` with `mysql` or `sqlite` depending on your database type.

## Development

To contribute to QuickCRUD, clone the repository and install the dependencies:

```
git clone https://github.com/wendersoon/QuickCRUD
cd QuickCRUD
poetry install
```

You can run tests, format the code with Black, and check for linting issues using the pre-configured tools.
