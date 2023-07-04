## Poetry hints
###

***
#### Sync dependencies in the pyproject.toml file with .lock file

To pin manually added dependencies from your pyproject.toml file to `poetry.lock`,
you must first run the poetry lock command:

```shell
poetry lock
```
If you don’t want to update any dependencies that are already in the poetry.lock file, 
then you have to add the --no-update option to the poetry lock command:
```shell
poetry lock --no-update
```
***
#### Open an interactive REPL session in Poetry’s environment
```shell
poetry run python3
```
***

#### Install poetry dependencies after locking
After locking dependencies with the poetry lock command,
you have to run the poetry install command so that you can actually use them in your project:
```shell
poetry install
```
***

#### Show poetry dependencies list
Listing all installed dependencies in project. Or show it as a tree (second option)
```shell
poetry show --help
poetry show --tree
```
***

#### Update Dependencies
For updating your dependencies, Poetry provides different options depending on two scenarios:

1. Update a dependency inside your version constraints.
2. Update a dependency outside your version constraints.

```shell
poetry update
```
The update command will update all your packages and their dependencies within their version constraints.
Afterward, Poetry will update your poetry.lock file.
***

#### Add Poetry to an Existing Project

```shell
poetry init
```
***

#### Run poetry environment
```shell
poetry shell
```
***

#### Poetry commands

Poetry Command	Explanation
```shell
poetry --version	# Show the version of your Poetry installation.
poetry new	# Create a new Poetry project.
poetry init	# Add Poetry to an existing project.
poetry run	# Execute the given command with Poetry.
poetry add	# Add a package to pyproject.toml and install it.
poetry update	# Update your project’s dependencies.
poetry install	# Install the dependencies.
poetry show	# List installed packages.
poetry lock	# Pin the latest version of your dependencies into poetry.lock.
poetry lock --no-update	# Refresh the poetry.lock file without updating any dependency version.
poetry check	# Validate pyproject.toml.
poetry config --list	# Show the Poetry configuration.
poetry env list	# List the virtual environments of your project.
poetry export	# Export poetry.lock to other formats.
```
