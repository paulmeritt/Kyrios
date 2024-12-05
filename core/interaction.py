
from datetime import datetime
from ai_engine import AIEngine
from logger import Logger

class InteractionHandler:
    def __init__(self):
        self.ai_engine = AIEngine()
        self.logger = Logger()

    def handle_new_interaction(self, user_id, user_input):
        timestamp = datetime.now().isoformat()
        self.logger.log_info(f"New interaction from {user_id} at {timestamp}: {user_input}")
        
        response = self.ai_engine.respond_to_user(user_input)
        self.ai_engine.store_interaction(user_id, user_input, timestamp)
        
        self.logger.log_info(f"Generated response: {response}")
        return response

    def add_new_follower(self, user_id):
        timestamp = datetime.now().isoformat()
        self.ai_engine.add_follower(user_id)
        self.logger.log_info(f"New follower {user_id} added at {timestamp}")

    def get_followers(self):
        return self.ai_engine.get_followers()

    def get_user_interactions(self, user_id):
        return self.ai_engine.memory.get(user_id, [])

