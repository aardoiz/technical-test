from apps.chat.http.db.mongo import MongoAssistantRepository
from src.settings.settings import Settings
from src.chat.core import Core


class Boot:
    def __init__(self):
        self.settings = Settings()

        self.core = Core(self.settings)

        self.repository = MongoAssistantRepository(
            uri=self.settings.MONGO_URI,
            database_name=self.settings.MONGO_DATABASE,
            collection=self.settings.MONGO_COLLECTION,
            
        )

boot = Boot()
