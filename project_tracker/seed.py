from django.contrib.auth.models import User, Group
from accounts.models import Profile
from clients.models import Client
from projects.models import Project
from tasks.models import Task
from datetime import date, timedelta

print("=== Seeding Database ===")

# 1️⃣ Ensure Groups Exist
groups = ["Admin", "Project Manager", "Developer"]
for g in groups:
    Group.objects.get_or_create(name=g)

# 2️⃣ Helper to Create Users with Roles
def create_user(username, role, first, last):
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password("pass1234")
        user.first_name = first
        user.last_name = last
        user.save()
        profile = user.profile
        profile.role = role
        profile.save()

        group_map = {'ADMIN': 'Admin', 'PM': 'Project Manager', 'DEV': 'Developer'}
        user.groups.add(Group.objects.get(name=group_map[role]))
        print(f"Created user: {username} ({role})")
    else:
        profile = user.profile
        if profile.role != role:
            profile.role = role
            profile.save()
        print(f"User already exists: {username} ({role})")
    return user

admin = create_user("admin_user", "ADMIN", "Manoj", "M")
pm = create_user("pm_user", "PM", "Priya", "Mehta")
dev1 = create_user("dev_raj", "DEV", "Raj", "Kumar")
dev2 = create_user("dev_anu", "DEV", "Anu", "Patel")
 
# 3️⃣ Create Clients
clients_data = [
    {"name": "TechVision Pvt Ltd", "contact_person": "Rohit Sharma", "email": "rohit@techvision.com"},
    {"name": "GreenSoft Solutions", "contact_person": "Sneha Verma", "email": "sneha@greensoft.in"},
    {"name": "InnoWave Systems", "contact_person": "Amit Desai", "email": "amit@innowave.io"},
    {"name": "RCC", "contact_person": "Amit ", "email": "rcc@innowave.io"},
]
clients = []

for data in clients_data:
    c, created = Client.objects.get_or_create(name=data["name"], defaults=data)
    if not created:
        updated = False
        for key, value in data.items():
            if getattr(c, key) != value:
                setattr(c, key, value)
                updated = True
        if updated:
            c.save()
    clients.append(c)

print(f"Created/Ensured {len(clients)} clients.")

# 4️⃣ Create Projects
if len(clients) < 3:
    raise RuntimeError("Not enough clients created.")

projects_data = [
    {"client": clients[0], "name": "Website Redesign", "manager": pm, "status": "IN_PROGRESS", "description": "UI/UX revamp and CMS migration"},
    {"client": clients[1], "name": "Mobile App Development", "manager": pm, "status": "PROSPECT", "description": "Hybrid app for e-commerce"},
    {"client": clients[2], "name": "Data Analytics Platform", "manager": pm, "status": "LEAD", "description": "Custom analytics dashboards"},
]

projects = []
for p in projects_data:
    obj, created = Project.objects.get_or_create(
        client=p["client"],
        name=p["name"],
        defaults={
            "description": p["description"],
            "manager": p["manager"],
            "status": p["status"],
            "start_date": date.today() - timedelta(days=10),
            "end_date": date.today() + timedelta(days=30),
        }
    )
    if not created:
        changed = False
        for key in ["description", "manager", "status"]:
            if getattr(obj, key) != p[key]:
                setattr(obj, key, p[key])
                changed = True
        if changed:
            obj.save()
    projects.append(obj)

print(f"Created/Ensured {len(projects)} projects.")

# 5️⃣ Create Tasks
if len(projects) < 3:
    raise RuntimeError("Not enough projects created.")

tasks_data = [
    {"project": projects[0], "title": "Design Landing Page", "assignee": dev1, "status": "IN_PROGRESS", "priority": "HIGH", "progress": 60},
    {"project": projects[0], "title": "Setup CMS", "assignee": dev2, "status": "TODO", "priority": "MEDIUM"},
    {"project": projects[1], "title": "Develop Login Module", "assignee": dev1, "status": "REVIEW", "priority": "HIGH", "progress": 90},
    {"project": projects[2], "title": "Create Dashboard API", "assignee": dev2, "status": "TODO", "priority": "HIGH"},
    {"project": projects[2], "title": "Integrate Charts", "assignee": dev1, "status": "TODO", "priority": "MEDIUM"},
]

for t in tasks_data:
    obj, created = Task.objects.get_or_create(
        project=t["project"],
        title=t["title"],
        defaults={
            "description": t.get("description", ""),
            "assignee": t["assignee"],
            "status": t["status"],
            "priority": t["priority"],
            "progress": t.get("progress", 0),
            "estimate_hours": 0,
            "due_date": date.today() + timedelta(days=7),
        }
    )
    if not created:
        changed = False
        for key in ["assignee", "status", "priority", "progress"]:
            if getattr(obj, key) != t.get(key, getattr(obj, key)):
                setattr(obj, key, t[key])
                changed = True
        if changed:
            obj.save()

print(f"Created/Ensured {len(tasks_data)} tasks.")
print("=== Seeding Complete ===")