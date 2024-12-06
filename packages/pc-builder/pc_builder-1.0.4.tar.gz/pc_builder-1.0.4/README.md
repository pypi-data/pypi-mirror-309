# PC Builder

## Overview

The **PC Builder** is an application designed to help users plan and
configure their ideal personal computer setup.
It allows users to select components based on their needs,
budget, and preferences, providing recommendations and compatibility checks.

## Team Members

- **Domantas Petkevičius** - Back-End Developer, Team Leader
- **Dagnis Matulis** - Back-End Developer
- **Juozas Krukauskas** - Front-End Developer
- **Simona Vytytė** - Front-End Developer

## Project Description

The PC Builder application provides an intuitive interface for users to:

- Browse and select various computer components (CPU, GPU, RAM, etc.)
- Add and remove parts from their personal build and display the current configurations.
- Get compatibility checks for selected components.
- View estimated costs based on selected parts.

## Technologies Used

- **Programming Language:** _python_
- **Frameworks:** _click_ for CLI interface
- **Testing:** _pytest_ and _unittest_ for unit and integration testing
- **Build Tools:** _tox_ for testing automation and building, _PyInstaller_ for creating executable files

## Infrastructure Management

The project uses Git for version control and GitHub for repository hosting. Continuous integration and testing are set up using **tox**, which automates the testing and build processes.

## Installing the PC Builder Package

- You can easily install the PC Builder package via pip from PyPI (if available):
  ```bash
  pip install pc-builder
  ```
- Once installed, you can use the pcbuilder command in your terminal to run the application:
  ```bash
  pcbuilder
  ```

## Building and Running the Application from source

This guide provides instructions for users to set up the PC Builder project, run tests, and build the application from source.

### Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Python 3.7 or later**: Download and install Python from [python.org](https://www.python.org/downloads/).
- **pip**: This usually comes pre-installed with Python. You can check if you have pip installed by running:
  ```bash
  pip --version
  ```

### Building and Running the Application Locally

- Clone the repository https://github.com/mif-it-se-2024/group-project-pc-builders
- Navigate to the Project Directory
  ```bash
  cd pc_builder
  ```
- Create a Virtual Environment (Optional but Recommended)

  Windows:

  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

  Linux:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- Install Project Dependencies

  ```bash
  pip install -r requirements.txt
  ```

- Run tests and build the application

  ```bash
  tox
  ```

- Launch the application
  ```bash
  cd dist
  ```
  ```bash
  pcbuilder.exe ( Windows ) or ./pcbuilder ( Linux )
  ```
