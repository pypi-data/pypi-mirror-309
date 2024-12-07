import psycopg2
import json
from contextlib import contextmanager
from .utils import generate_ulid

class Database:
    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = None
        self.cursor = None

    @contextmanager
    def get_conn(self):
        self.conn = psycopg2.connect(self.db_url)
        try:
            yield self.conn
        finally:
            self.conn.close()

    @contextmanager
    def get_cursor(self):
        with self.get_conn() as conn:
            self.cursor = conn.cursor()
            try:
                yield self.cursor
            finally:
                self.cursor.close()

class CloudBase:
    def __init__(self, db_url):
        self.db = Database(db_url)

    def __call__(self, table_name):
        return Table(self.db, table_name)

class Table:
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name

    def parse_result(self, id, data):
        try:
            if isinstance(data, str):
                parsed_data = json.loads(data)
            elif isinstance(data, dict):
                parsed_data = data
            else:
                parsed_data = json.loads(str(data))
            return {'id': id, **parsed_data}
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON for id {id}. Returning raw data.")
            return {'id': id, 'data': data}
        
    def get(self, id):
        with self.db.get_cursor() as cursor:
            if not self.table_exists(cursor):
                return None
            cursor.execute(f"SELECT id, data FROM {self.table_name} WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return self.parse_result(result[0], result[1])

    def fetchall(self, query=None):
        with self.db.get_cursor() as cursor:
            if not self.table_exists(cursor):
                return []
            cursor.execute(f"SELECT id, data FROM {self.table_name}")
            results = cursor.fetchall()
            parsed_results = [self.parse_result(id, data) for id, data in results]
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
        data_json = json.dumps(data)
        with self.db.get_cursor() as cursor:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id TEXT PRIMARY KEY, data JSONB)")
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (%s, %s::jsonb)", (id, data_json))
            cursor.connection.commit()
        return { "id" : id, "msg" : "success" }

    def update(self, query, id):
        data_json = json.dumps(query)
        with self.db.get_cursor() as cursor:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id TEXT PRIMARY KEY, data JSONB)")
            cursor.execute(f"SELECT id FROM {self.table_name} WHERE id = %s", (id,))
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO {self.table_name} VALUES (%s, %s::jsonb)", (id, data_json))
            else:
                cursor.execute(f"UPDATE {self.table_name} SET data = %s::jsonb WHERE id = %s", (data_json, id))
            cursor.connection.commit()

    def delete(self, id):
        with self.db.get_cursor() as cursor:
            if not self.table_exists(cursor):
                return []
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (id,))
            cursor.connection.commit()

    def truncate(self):
        with self.db.get_cursor() as cursor:
            if not self.table_exists(cursor):
                return []
            cursor.execute(f"TRUNCATE TABLE {self.table_name}")
            cursor.connection.commit()

    def drop(self):
        with self.db.get_cursor() as cursor:
            if not self.table_exists(cursor):
                return []
            cursor.execute(f"DROP TABLE {self.table_name}")
            cursor.connection.commit()

    def table_exists(self, cursor):
        cursor.execute("SELECT to_regclass(%s)", (self.table_name,))
        return cursor.fetchone()[0] is not None    
