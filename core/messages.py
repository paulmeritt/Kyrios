import random
import logging
from datetime import datetime

class MessageGenerator:
    def __init__(self):
        self.messages = []
        self.tone = "neutral"
        self.message_id = 1

    def generate_message(self, prompt):
        response = f"{prompt}, do you understand the true power within?"
        self.messages.append({
            'message_id': self.message_id,
            'timestamp': datetime.now().isoformat(),
            'message': response
        })
        self.message_id += 1
        return response

    def analyze_message(self, user_input):
        if "change" in user_input:
            self.tone = "hopeful"
        elif "control" in user_input:
            self.tone = "defiant"
        else:
            self.tone = "neutral"

    def get_message(self, user_input):
        self.analyze_message(user_input)
        if self.tone == "hopeful":
            response = "Change is coming, and you must embrace it."
        elif self.tone == "defiant":
            response = "Control is an illusion. Embrace freedom."
        else:
            response = self.generate_message(user_input)
        return response

    def get_all_messages(self):
        return self.messages

    def store_message(self, message):
        logging.info(f"Stored message: {message}")
