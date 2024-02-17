from app.database.database import Base, engine, Session
from app.database.model import User


def create_database() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    user = User(
        username="admin",
        email="admin@admin.com",
        password="admin",
        full_name="admin",
        is_active=True,
        is_admin=True,
    )

    with Session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        print("Database created and user added")
