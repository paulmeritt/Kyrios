from firmware_agents.agent_comm import AgentComm
from firmware_agents.data_processor import DataProcessor
from firmware_agents.security import Security
from core.logger import Logger

class AgentManager:
    def __init__(self):
        self.logger = Logger()
        self.agent_comm = AgentComm("127.0.0.1", 9999)
        self.data_processor = DataProcessor()
        self.security = Security()

    def start(self):
        """
        Start the agent manager and initialize all agent services.
        """
        try:
            self.logger.log_info("Starting agent manager.")
            self.agent_comm.start_server()
        except Exception as e:
            self.logger.log_error(f"Error starting agent manager: {e}")

if __name__ == "__main__":
    agent_manager = AgentManager()
    agent_manager.start()
