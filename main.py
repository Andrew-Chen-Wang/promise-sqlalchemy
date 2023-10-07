from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

db_engine = create_engine("sqlite:///:memory:")

# Create a Session class to interact with the database
Session = sessionmaker(bind=db_engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)


# Create the table in the database
Base.metadata.create_all(db_engine)

# Example: Inserting a new user
new_user = User(username="john_doe", email="john@example.com")
session = Session()
session.add(new_user)
session.commit()

# Example: Querying for users
users = session.query(User).all()
for user in users:
    print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}")

# Close the session when done
session.close()
