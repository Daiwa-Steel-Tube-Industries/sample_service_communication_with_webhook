from sqlmodel import Field, Session, SQLModel, create_engine


class Hook(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    event: str = Field(index=True)
    url: str = Field()


class Order(SQLModel, table=True):
    id: int = Field(primary_key=True)
    data: str = Field()


sqlite_filename = "db.sqlite"
sqlite_url = f"sqlite:///{sqlite_filename}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def insert_order_if_not_exists():
    with Session(engine) as session:
        existing_order = session.get(Order, 1)

        if not existing_order:
            new_order = Order(id=1, data="test")
            session.add(new_order)
            session.commit()
            print("✅ Order with id=1 inserted.")
        else:
            # The order already exists, do nothing
            print("ℹ️ Order with id=1 already exists. Doing nothing.")
