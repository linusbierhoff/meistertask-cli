# MeisterTask CLI

A UNOFFICIAL command-line interface for managing your [MeisterTask](https://www.meistertask.com/) projects, sections, tasks, and persons. Built with Python, Click, and Rich.

## Features

- **Projects**: List and view project details.
- **Sections**: List and view sections within projects.
- **Tasks**: List, view, create, and move tasks across sections.
- **Persons**: View your own profile and list/view other users.
- **Beautiful UI**: Uses [Rich](https://github.com/Textualize/rich) for formatted tables and colored output.

## Installation

### Using uv (Recommended)

```bash
 uv tool install .
```

### Using pipx

```bash
 pipx install .
 ```


## Getting Started

1. **Get a Personal Access Token**:
   Log in to MeisterTask, go to your account settings, and create a [Personal Access Token](https://www.meistertask.com/developers/auth).

2. **Configure the CLI**:
   Run the following command and enter your token when prompted:

   ```bash
   mtask configure
   ```

## Usage

The CLI is accessible via the `mtask` command.

### Projects

```bash
# List all projects
mtask projects list

# Get details for a specific project
mtask projects get <project_id>
```

### Sections

```bash
# List all sections
mtask sections list

# List sections for a specific project
mtask sections list --project <project_id/project_name>

# Get details for a specific section
mtask sections get <section_id>
```

### Tasks

```bash
# List all tasks
mtask tasks list

# List tasks assigned to you
mtask tasks list --mine

# List tasks for a specific project
mtask tasks list --project <project_id/project_name>

# List tasks for a specific section
mtask tasks list --section <section_id/section_name>

# Create a new task
mtask tasks create --name "My New Task" --section <section_id/section_name> --project <project_id/project_name>

# Move a task to a different section
mtask tasks edit <task_id> --section <new_section_id/new_section_name>

# Get details for a specific task
mtask tasks get <task_id>
```

### Persons

```bash
# Show your own profile
mtask persons me

# List persons in a project
mtask persons list --project <project_id/project_name>

# Get details for a specific person
mtask persons get <person_id>
```