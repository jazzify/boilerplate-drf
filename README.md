# Django Rest Framework Base Project

### Built with:
- Docker + Compose
- Gunicorn
- Whitenoise
- MySQL
- MongoDB
- Docs (Open API 3.0)
- Debug Toolbar

## Development requirements
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [uv](https://docs.astral.sh/uv/) (`pip install uv`)
- [Task](https://taskfile.dev/)
- [pre-commit](https://pre-commit.com/) (`pip install pre-commit`)

## New project setup
1. Clone the repository:
    ```sh
    git clone https://jorgebravo-vumi@bitbucket.org/vumiteam/boilerplate-django-be.git [project_dir_name]
    cd [project_dir_name]
    ```
1. Delete the `.git` directory:
    ```sh
    rm -rf .git # for Unix based
    rm -r -fo .git # for Windows (Terminal)
    # or just right click and delete.
    ```
1. Edit this `README.md` file to match your final initial setup.
1. Create the project's git to have a clean git history:
    ```sh
    git init
    pre-commit install # install pre-commit hooks
    git add .
    git commit -m "Initial commit"
    git remote add origin <github-uri>
    git push -u --force origin [master|main]
    ```
1. Create a `.env` file just like `.env.example` with your custom data, if you add something to your `.env` file, also and keep `.env.example` updated with dummy values for key reference.

## Taskfile and Docker
The tasks defined in the Taskfile are executed within a Docker container, which has a volume mounted to the host PC. This volume specifically includes the application's codebase, allowing for a seamless integration between the development environment on the host and the containerized tasks.

Here's how it works:

1. **Code Synchronization**: The mounted volume in the `docker-compose.yaml>web` ensures that the code inside the container is the same as on the host machine. Any changes made to the code on the host are immediately reflected within the container. This is crucial for development workflows, where frequent changes to the codebase are tested and iterated upon.

1. **Docker Compose and Django Operations**: The tasks typically involve operations such as starting, stopping, or managing services using Docker Compose, as well as running commands related to Django. Since these tasks rely on the codebase, the volume ensures they operate on the latest version of the code, regardless of where the task is run.

1. **Host and Container Interaction**: While the tasks are executed in an isolated container environment, the mounted volume enables these tasks to access and manipulate the code on the host machine. This setup is particularly useful for tasks that need to interact closely with the host's file system or leverage host-specific configurations.

Run `task --list` to see a full list of available tasks with their description.

- **Common docker compose commands**
    ```bash
    # build the containers without cache
    task compose-build -- --no-cache

    # start the containers in detached mode
    task compose-up -- -d

    # stop the containers
    task compose-stop

    # down the containers
    task compose-down
    ```

- **Common manage.py commands**
    ```bash
    # create a super user
    task manage-createsuperuser

    # make migrations for a specific app
    task manage-makemigrations -- <app_name>

    # migrate a specific db
    task manage-migrate -- --database=<db_name>

    # start a new app
    task manage-startapp -- <app_name>
    ```

**DISCLAIMER**: Even with this volume approach some tasks might **NOT** reflect the changes in the host machine, for example, running `task uv-add -- requests` will install the `requests` lib dependency inside the docker container only, and you would need to install it via `uv add requests` locally if you want to have editor completitions or linting for the lib. Because we mainly work with Windows OS, this is actually the behaviour we want since there are some libraries that might work fine in the container (linux), but not in the host machine.

The best approach to install a dependency in the host and a running container is to install it locally with `uv add <dependency_name>` and then run `task uv-sync`.

If you add a new task that does not work with the volume approach intuitively, please add `[CONTAINER_ONLY]` tag to the task description.


## Testing
Currently we use [pytest-django](https://pytest-django.readthedocs.io/en/latest/index.html) for testing our code.
We use [faker](https://faker.readthedocs.io/en/latest/) along with [factory_boy](https://factoryboy.readthedocs.io/en/latest/) to generate data for our testing models.

Complete list of the default providers available in `faker`: https://faker.readthedocs.io/en/stable/providers.html

### Testing with MongoDB:
Mongoengine does not have a built-in testing framework, so we use [mongomock](https://mongomock.readthedocs.io/en/latest/) to mock the MongoDB database and then we instantiate a testing database at `apps\conftest.py::pytest_configure` at the beginning of the test suite, then we drop the database at `apps\conftest.py::pytest_teardown` at the end of each test so we don't leave any data in the database across tests.

We can still use `factory_boy` to generate data for our testing models using our Documents as models inheriting from `factory.base.Factory` instead of `factory.django.DjangoModelFactory` however we cannot use the factory to create (persist in the db) any Document instances due to the abstractions built-in the creation methods of `factory_boy`, so instead of things like:

```python
BookFactory.create_batch(size=3)
```
We would have to use:
```python
Book.objects.insert(BookFactory.build_batch(size=3))
```

### Running tests:
```bash
# Run all tests
task test

# Run a specific test file
task test -- path/to/test_file_example.py

# Run a specific test
task test -- path/to/test_file_example.py::test_example
```
## API docs generation
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/index.html)
