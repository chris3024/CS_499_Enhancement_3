# CS-499: Enhancement 3
[![🐍  Python-tests](https://github.com/chris3024/CS_499_Enhancement_3/actions/workflows/pyton-tests.yml/badge.svg)](https://github.com/chris3024/CS_499_Enhancement_3/actions/workflows/pyton-tests.yml)
![pylint](https://img.shields.io/badge/PyLint-9.94-yellow?logo=python&logoColor=white)
[![CodeQL Advanced](https://github.com/chris3024/CS_499_Enhancement_3/actions/workflows/codeql.yml/badge.svg)](https://github.com/chris3024/CS_499_Enhancement_3/actions/workflows/codeql.yml)
___

This repository holds the enhanced codebase for Category Three: Databases. The original code originates from work created in IT-145: Foundation in Application Development. This was first expanded upon in Enhancement One, which added the GUI framework and data persistence
in the form of JSON files. In this enhancement, the JSON file I/O is replaced with the use of a database, specifically MongoDB. Also, this code was further enhanced with the implementation of user authentication, role-based access control, and advanced security features, such as password hashing. 

| Main Window (Login Button)                                                           | Login Window                                                                |
|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| <img src="screenshots/Screenshot 2025-06-08 173208.png" alt="Main Menu" width="546"> | <img src="screenshots/Screenshot 2025-06-08 173215.png" alt="Login Screen"> |

| Main Window (Admin)                                                                   | Main Window (User)                                                                   |
|---------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| <img src="screenshots/Screenshot 2025-06-08 173232.png" alt="Admin Main" width="546"> | <img src="screenshots/Screenshot 2025-06-08 173252.png" alt="User Main" width="546"> |

| CRUD Methods                                                                             | CRUD Methods (Continued)                                                                 |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| <img src="screenshots/Screenshot 2025-06-03 101434.png" alt="Create/Update" width="546"> | <img src="screenshots/Screenshot 2025-06-03 101446.png" alt="Update/Delete" width="546"> |

___

## Prerequisites
* <a href="https://python.org">Python</a>
* <a href="https://mongodb.com">MongoDB</a>

___

#### Setup Instructions

1. Clone Repository
    ```bash
    git clone https://github.com/chris3024/CS_499_Enhancement_3.git
    cd CS_499_Enhancement_3
    ```
    Manual Download:
    * Click the green Code button
    * Select Download Zip
    * Extract to a directory of your choice

2. Setup and Activate the virtual environment
 
    Linus/macOS
    ```bash
    python3 -m venv venv
    ```
    Windows (Command Prompt)
    ```cmd
    python -m venv venv
    ```
    Windows (Powershell)
    ```powershell
    python -m venv venv
    venv\Scripts\Activate.ps1
    ```
    
3. Install requirements for the project
    ```bash
    pip install -r requirements.txt
    ```
4. Run the application
    ```bash
    python main.py
    ```