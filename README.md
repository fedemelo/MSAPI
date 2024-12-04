<h1 align="center">Melanoma Segmentation API</h1>

<p align="center">
   <a href="https://sonarcloud.io/summary/new_code?id=fedemelo_MSAPI"><img src="https://sonarcloud.io/api/project_badges/measure?project=fedemelo_MSAPI&metric=alert_status" alt="Quality Gate Status"></a>
   <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
   <a href="https://pycqa.github.io/isort/"><img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="Imports: isort"></a>
</p>

---

Melanoma Segmentation API (MSAPI) is a FastAPI-based REST API that communicates with segmentation and classification models for melanoma detection in dermoscopic images.

It is designed to be consumed by the [Melanoma Segmentation Web Application (MSWA)](https://github.com/fedemelo/MSWA).

## Quick Reference

The official documentation for the API was built automatically by Swagger and is available at http://localhost:8000 once the server is running.

However, the following table provides a quick reference for the most important endpoints available.

| **Request Type** | **Endpoint Path**        | **Description**                                                                                              |
| ---------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------ |
| POST             | `v1.0/doctors`           | Registers a new user with fields: name, email, and password. Ensures email is unique.                        |
| POST             | `v1.0/doctors/login`     | Authenticates a user using email and password with the OAuth 2.0 protocol.                                   |
| GET/PUT          | `v1.0/doctors/<email>`   | Retrieves (GET) or updates (PUT) doctor profile information.                                                 |
| GET              | `v1.0/patients/<cedula>` | Retrieves the patient information, including all images uploaded for a patient and their segmentation masks. |
| POST             | `v1.0/patients`          | Registers a new patient with fields: name, cédula, and doctor email. Ensures cédula is unique.               |
| POST             | `v1.0/images`            | Allows uploading a named image to a patient with their cédula.                                               |
| POST             | `v1.0/images/process`    | [PENDING] Processes the uploaded image and returns the segmentation mask by communicating with the model.    |

## Local Setup

The project must be run using [Python 3.11.3](https://www.python.org/downloads/release/python-3113/).

1. Clone the repository and navigate to the project directory:

   ```shell
   git clone https://github.com/fedemelo/MSAPI
   cd msapi
   ```

### Dependencies

2. Create a virtual environment

   ```shell
   python3.11 -m venv venv
   ```

3. Activate the virtual environment

   Unix:

   ```shell
   source venv/bin/activate
   ```

   Windows:

   ```batch
   venv\Scripts\activate.bat
   ```

4. Install dependencies

   ```shell
   pip install -r requirements.txt
   ```

> [!WARNING]
> **Windows users**
>
> Note that the `uvloop` package is not compatible with Windows. If it is present in the `requirements.txt` file, it must be manually removed before installing the dependencies. Removing it will not affect API functionality.


5. Install pre-commit hooks

   ```shell
   pre-commit install
   ```

   This will ensure that the code is formatted, linted, and tested before each commit. See [Code Quality](#code-quality) for more information.

### Database

6. Create the database or restore a backup

   Either create a new database or restore a backup:
   - To create new database, run the following command:
      ```shell
      psql -U postgres -c "CREATE DATABASE melanoma_segmentation_db"
      ```
      Then, run the application. The application will create the necessary tables.

   - To restore a backup, run the corresponding script.

      Unix:

      ```shell
      sh db/restore-db-backup.sh
      ```

      Windows:

      ```batch
      db\restore-db-backup.bat
      ```
   
 > [!NOTE] 
 > There's also a script to save a backup of the database, `db/save-db-backup`, which saves the current state of the database into the `db/backups` directory.

### Run the Server

7. Run the server. In the root of the project, run the following command:

   ```shell
   python -m run
   ```

   The server will be running on `http://localhost:8002`

## Code Quality

Before each commit, the code is automatically formatted, linted, and tested using a pre-commit hook.
After each push, the code is scanned by SonarCloud.

[Access SonarCloud here](https://sonarcloud.io/summary/overall?id=fedemelo_MSAPI).

### Formatting, Linting, and Testing

The code is formatted using Black and isort, linted with Flake8, and tested with Pytest.

A pre-commit hook takes care of formatting, linting, and testing the code before each commit. It must be installed by running the following command:

```shell
pre-commit install
```

#### Manual Formatting, Linting, and Testing

Should the pre-commit hook fail, the code can be manually formatted, linted, and tested.

To manually format the code:

```shell
isort . && black .
```

To lint the code:

```shell
flake8 .
```

## API Design

The API is structured based on the design illustrated in the UML class diagram below:

![MSAPI Class Diagram](https://github.com/user-attachments/assets/abee7b3d-036a-42b0-b55c-5f65bdd21cf9)

### Important Considerations

While the UML diagram provides a high-level overview of the API design, there are specific details about how deletions are handled that are not depicted in the diagram. These are outlined as follows:

- **Doctor Deletion**:  
  The API restricts the deletion of a doctor if they have patients associated with them. Any attempt to delete such a doctor will be rejected.

- **Patient Deletion**:  
  The API permits the deletion of a patient. When a patient is deleted, all associated images and predictions are automatically removed as part of the deletion process. 
