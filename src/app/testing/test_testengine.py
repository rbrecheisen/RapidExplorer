from data.databasemanager import DatabaseManager


def test_initializeEngineForTesting():
    manager = DatabaseManager()
    # assert manager.testing