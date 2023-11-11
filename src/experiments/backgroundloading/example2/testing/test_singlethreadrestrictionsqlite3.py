import pytest
import threading
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DBAPIError

# Define a simple table for testing
metadata = MetaData()
test_table = Table('test', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('data', String))

# Function to perform database operation in a thread
def db_operation(engine, barrier):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        barrier.wait()
        # Insert operation
        session.execute(test_table.insert().values(data="data"))
        session.commit()
    except Exception as e:
        raise e
    finally:
        session.close()

# Pytest function
def test_sqlite_sqlalchemy_threading():
    # Setup SQLAlchemy engine for shared in-memory database
    engine = create_engine('sqlite:///file:memdb1?mode=memory&cache=shared')
    metadata.create_all(engine)

    # Using a barrier to ensure threads start simultaneously
    barrier = threading.Barrier(2)

    # Creating threads
    thread1 = threading.Thread(target=db_operation, args=(engine, barrier))
    thread2 = threading.Thread(target=db_operation, args=(engine, barrier))

    # Starting threads
    thread1.start()
    thread2.start()

    # Expecting a database error due to threading issues
    # with pytest.raises(DBAPIError):
    thread1.join()
    thread2.join()

