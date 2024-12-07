from sqlalchemy import create_engine, Column, String, JSON, Table as SQLATable, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect
import json
from contextlib import contextmanager
from .utils import generate_ulid

Base = declarative_base()

class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.metadata = MetaData()

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

class CloudBase:
    def __init__(self, db_url):
        self.db = Database(db_url)

    def __call__(self, table_name):
        return Table(self.db, table_name)

class Table:
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name
        self.table = self.get_or_create_table()

    def get_or_create_table(self):
        inspector = inspect(self.db.engine)
        if not inspector.has_table(self.table_name):
            table = SQLATable(self.table_name, self.db.metadata,
                Column('id', String, primary_key=True),
                Column('data', JSON)
            )
            self.db.metadata.create_all(self.db.engine)
        else:
            table = SQLATable(self.table_name, self.db.metadata, autoload_with=self.db.engine)
        return table

    def parse_result(self, row):
        try:
            data = json.loads(row.data) if isinstance(row.data, str) else row.data
            return {'id': row.id, **data}
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON for id {row.id}. Returning raw data.")
            return {'id': row.id, 'data': row.data}

    def fetchall(self, query=None):
        with self.db.get_session() as session:
            results = session.query(self.table).all()
            parsed_results = [self.parse_result(row) for row in results]
            if query is None:
                return parsed_results
            else:
                return self.filter_results(parsed_results, query)

    def fetch(self, query=None):
        return self.fetchall(query)

    def filter_results(self, results, query):
        filtered_results = []
        for result in results:
            match = True
            for key, value in query.items():
                if "?contains" in key:
                    field = key.split("?")[0]
                    if value.lower() not in str(result.get(field, "")).lower():
                        match = False
                        break
                else:
                    if result.get(key) != value:
                        match = False
                        break
            if match:
                filtered_results.append(result)
        return filtered_results

    def put(self, data):
        id = str(generate_ulid())
        with self.db.get_session() as session:
            new_row = self.table.insert().values(id=id, data=data)
            session.execute(new_row)
            session.commit()
        return {"id": id, "msg": "success"}

    def update(self, query, id):
        with self.db.get_session() as session:
            update_stmt = self.table.update().where(self.table.c.id == id).values(data=query)
            session.execute(update_stmt)
            session.commit()

    def delete(self, id):
        with self.db.get_session() as session:
            delete_stmt = self.table.delete().where(self.table.c.id == id)
            session.execute(delete_stmt)
            session.commit()

    def truncate(self):
        with self.db.get_session() as session:
            session.execute(self.table.delete())
            session.commit()

    def drop(self):
        self.table.drop(self.db.engine)

    def get(self, id):
        with self.db.get_session() as session:
            result = session.query(self.table).filter(self.table.c.id == id).first()
            return self.parse_result(result) if result else None
        
# -----------------------------------
# # Initialize the database connection (example with SQLite)
# db_url = "postgresql://neondb_owner:5JVIgPtBlk6R@ep-fancy-mountain-a7mulxw3.ap-southeast-2.aws.neon.tech/neondb?sslmode=require"
# db = CloudBase(db_url)

# # Access the 'users' table
# users = db('users')

# # Example: Insert a user
# new_user = users.put({"name": "John Doe", "email": "john@example.com"})
# print("Inserted user:", new_user)

# # Get the user by id
# user_id = new_user['id']
# retrieved_user = users.get(user_id)
# print("Retrieved user:", retrieved_user)

# # Fetch all users
# all_users = users.fetch()
# print("All users:", all_users)

# # Update a user
# users.update({"name": "John Updated", "email": "john.updated@example.com"}, user_id)
# updated_user = users.get(user_id)
# print("Updated user:", updated_user)

# # Delete a user
# users.delete(user_id)
# deleted_user = users.get(user_id)
# print("Deleted user (should be None):", deleted_user)