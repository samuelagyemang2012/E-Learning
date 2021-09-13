from migrations.database import init_db, db_session
from migrations.roles_migration import Role
from models.roles_model import RoleModel
# Create database
init_db()
print("Tables created")

# Create Roles
role_model = RoleModel()
teacher = Role("teacher")
student = Role('student')

role_model.create(teacher)
role_model.create(student)

print("Roles added")

