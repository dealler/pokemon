# Pokémon Battle Simulator

## Introduction
This Pokémon Battle Simulator allows users to simulate battles between different Pokémon. The simulator uses a SQLite database to record battle outcomes and event details, and fetches Pokémon data from the PokeAPI.

## Prerequisites
Before running the simulator, ensure you have Docker installed on your machine. Docker will be used to build and run the application in an isolated environment.

## Setup and Installation
1. **Clone the Repository**  
   If the code is hosted on a version control system like GitHub, provide cloning instructions. Otherwise, ensure all files are placed in a single directory.

   ```bash
   git clone https://github.com/dealler/pokemon.git
   cd pokemon


2. **Usage**
   To use Docker Compose, you'll need to have Docker Compose installed. Then, you can start your application and Redis with the following command:

   ```bash
   docker-compose up
This command builds your application's Docker image, pulls the Redis image if it's not already present, and starts both containers. Your application will be able to connect to the Redis server at redis:6379.   

## Usage
   Once the application is running inside the Docker container, follow the on-screen prompts to simulate Pokémon battles. You will be asked to enter the names of the Pokémon that will battle each other. The simulator will then proceed with the battle, displaying each move and its outcome.

## Features
Battle simulation between two Pokémon.
Fetches real Pokémon data from the PokeAPI.
Records battle outcomes and event details in a SQLite database.
## Testing
To run the test suite for the application:

Ensure you have Python installed with the necessary packages (unittest, requests).

Run the test files using Python's unittest framework.

    
    python -m unittest test_poke_db.py
    python -m unittest test_pokemon.py




## Contact
[created by Ilan Kraisler](https://www.linkedin.com/in/ilan-kraisler-29815734/)
