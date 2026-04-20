import requests


class MeisterTaskClient:
    BASE_URL = "https://www.meistertask.com/api"

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _request(self, method, path, **kwargs):
        url = f"{self.BASE_URL}/{path.lstrip('/')}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def _get_project_id(self, project):
        if isinstance(project, int):
            return project
        project_data = self.find_project_by_name(project)
        if project_data:
            return project_data["id"]

    def _get_person_id(self, person, project=None):
        if isinstance(person, int):
            return person
        persons = self.find_person_by_name(person, project)
        if persons:
            return persons[0]["id"]

    def _get_section_id(self, section, project=None):
        if isinstance(section, int):
            return section
        section_data = self.find_section_by_name(section, project=project)
        if section_data:
            return section_data["id"]

    def _get_task_id(self, task, project=None):
        if isinstance(task, int):
            return task
        task_data = self.find_task_by_name(task, project=project)

        if task_data:
            return task_data["id"]

    # Projects

    def get_projects(self, sort):
        projects = self._request("GET", "projects", params={"sort": sort})
        return projects

    def get_project_by_id(self, project_id):
        return self._request("GET", f"projects/{project_id}")

    def find_project_by_name(self, name):
        projects = self.get_projects(sort="name")
        for project in projects:
            if project["name"].lower() == name.lower():
                return project
        return None

    # Sections

    def get_sections(self, sort, project=None):
        project_id = self._get_project_id(project) if project else None

        path = f"projects/{project_id}/sections" if project_id else "sections"
        sections = self._request("GET", path, params={"sort": sort})
        return sections

    def get_section_by_id(self, section_id):
        return self._request("GET", f"sections/{section_id}")

    def find_section_by_name(self, name, project=None):
        project_id = self._get_project_id(project) if project else None

        path = f"projects/{project_id}/sections" if project_id else "sections"
        sections = self._request("GET", path, params={"sort": "name"})
        for section in sections:
            if section["name"].lower() == name.lower():
                return section
        return None

    # Persons

    def get_persons(self, sort, project=None):
        project_id = self._get_project_id(project) if project else None

        path = f"projects/{project_id}/persons" if project_id else "persons"
        persons = self._request("GET", path, params={"sort": sort})
        return persons

    def get_me(self):
        return self._request("GET", "persons/me")

    def get_person_by_id(self, person_id):
        return self._request("GET", f"persons/{person_id}")

    def find_person_by_name(self, name, project=None):
        project_id = self._get_project_id(project) if project else None

        path = f"projects/{project_id}/persons" if project_id else "persons"
        persons = self._request("GET", path, params={"sort": "name"})
        for person in persons:
            if person["name"].lower() == name.lower():
                return person
        return None

    # Tasks

    def get_tasks(
        self,
        sort,
        assigned_to_me=False,
        unassigned=False,
        assign_to=None,  # ID or name
        project=None,  # ID or name
        section=None,  # ID or name
    ):
        project_id = self._get_project_id(project) if project else None
        section_id = self._get_section_id(section, project=project) if section else None
        assign_to_id = (
            self._get_person_id(assign_to, project=project) if assign_to else None
        )

        path = f"projects/{project_id}/tasks" if project_id else "tasks"

        query_params = {"status": "open", "sort": sort, "items": 1000}

        if assigned_to_me:
            query_params["assigned_to_me"] = "true"

        tasks = self._request("GET", path, params=query_params)

        if section_id:
            tasks = [t for t in tasks if t.get("section_id") == section_id]

        if assign_to_id:
            tasks = [t for t in tasks if t.get("assigned_to_id") == assign_to_id]

        if unassigned:
            tasks = [t for t in tasks if t.get("assigned_to_id") is None]

        persons = self.get_persons(sort="last_name", project=project)

        for task in tasks:
            assigned_to_id = task.get("assigned_to_id")

            if assigned_to_id:
                person = next((p for p in persons if p["id"] == assigned_to_id), None)
                task["assigned_to_name"] = (
                    f"{person['firstname']} {person['lastname']}"
                    if person
                    else "Unknown"
                )

        return tasks

    def get_task_by_id(self, task_id):
        task = self._request("GET", f"tasks/{task_id}")

        assigned_to_id = task.get("assigned_to_id")

        persons = self.get_persons(sort="lastname", project=task["project_id"])

        if assigned_to_id:
            person = next((p for p in persons if p["id"] == assigned_to_id), None)
            task["assigned_to_name"] = (
                f"{person['firstname']} {person['lastname']}" if person else "Unknown"
            )

        return task

    def find_task_by_name(self, name, project=None):
        tasks = self.get_tasks(sort="name", project=project)
        for task in tasks:
            if task["name"].lower() == name.lower():
                return task
        return None

    def create_task(self, name, section, project):
        section_id = self._get_section_id(section, project=project)
        return self._request(
            "POST", f"sections/{section_id}/tasks", json={"name": name}
        )

    def move_task(self, task, section):
        task_id = self._get_task_id(task)
        section_id = self._get_section_id(section)
        return self._request("PUT", f"tasks/{task_id}", json={"section_id": section_id})
