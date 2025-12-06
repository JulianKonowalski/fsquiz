import dotenv

from db.Database import Database

if __name__ == "__main__":
    dotenv.load_dotenv()
    db = Database()
    print(db.insertEvent("test_event"))