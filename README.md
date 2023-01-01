# StupidityDB Server

This is the server for the StupidityDB project. It is a simple HTTP server that serves data from a
PostGreSQL database.

## Installation

Python 3.10+ is required to run the server You can get it [here](https://www.python.org/downloads/).

You will also need to install the dependencies. You can do this by running the following command:

```bash
pip install -U poetry
poetry install --only main
```

## Pre Run

Before running the server, you will need to edit the a `config.example.json5` file in
the `stupidity_db_server` directory (Also rename it to `config.json5`.).

You also need to run every SQL script in the `schemas` directory (By order) in the database you want to use.

## Running

To run the server, you can use the following command:

```bash
poetry run server
```
