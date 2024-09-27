## RegisterUni

## Project Description
RegisterUni is our course registration app is specifically designed to simplify and speed up the enrollment process for everyone involved—students, teachers, and advisors. This tool allows students to easily browse course listings, enables teachers to access student feedback for any courses, and assists advisors in editing degree audits for all of their students. By addressing common issues such as enrollment limits, scheduling conflicts, and course setup, RegisterUni utilizes real-time data and advanced scheduling algorithms to ensure a smooth academic journey for students and efficient course management for faculty.


This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`.

## List of members
Kim-Cuong Tran Dang,
Sarthak Pokharel,
Maxwell Schnock,
Jacob Chamoun,
Karina Khaledi

## Meeting Recording
[Watch the recorded meeting here!] (https://youtu.be/osVJMIvhUOI?si=enmHJ9aS8APqcYRa)


## License
This project is licensed under the MIT License





