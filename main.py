from sqlalchemy import create_engine, Column, Integer, String, insert
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from promise import Promise
from itertools import chain
from time import time

from src.query import Query


# db_engine = create_engine("sqlite:///:memory:")
db_engine = create_engine("postgresql://postgres:postgres@localhost:5432/test")
Base = declarative_base()

total = 1_000_000


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(100))


def test(use_custom_query_cls: bool):
    # Create a Session class to interact with the database
    if use_custom_query_cls:
        session_factory = sessionmaker(bind=db_engine, query_cls=Query)
    else:
        session_factory = sessionmaker(bind=db_engine)
    Session = scoped_session(session_factory)
    session = Session()

    # Example: Querying for users
    start = time()
    users1 = session.query(User).all()
    end1 = time()
    print(end1 - start)
    users2 = session.query(User).all()
    end2 = time()
    print(end2 - end1)
    users3 = session.query(User).all()
    end3 = time()
    print(end3 - end2)
    resolved = [users1, users2, users3]
    if use_custom_query_cls:
        resolved = Promise.all([users1, users2, users3]).get()
    end = time()
    all_users: list[User] = list(chain.from_iterable(resolved))
    assert len(all_users) == total * len(
        resolved
    ), f"Expected {total * len(resolved)} users, got {len(all_users)}"

    session.close()

    return end - start


def main():
    Base.metadata.drop_all(db_engine)
    Base.metadata.create_all(db_engine)

    # Create a Session class to interact with the database
    session_factory = sessionmaker(bind=db_engine)
    Session = scoped_session(session_factory)

    new_users = [{"username": str(i), "email": f"{i}@mail.com"} for i in range(total)]
    session = Session()
    session.execute(insert(User), new_users)
    session.commit()
    # Close the session when done
    session.close()

    print("Async query class:", test(True))
    print("Default query class:", test(False))


if __name__ == "__main__":
    main()
