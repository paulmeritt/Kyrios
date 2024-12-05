import subprocess
import os
from core.logger import Logger

class AgentExecutor:
    def __init__(self):
        self.logger = Logger()

    def execute_command(self, command):
        """
        Execute a shell command on the agent system.
        """
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.log_info(f"Command executed successfully: {command}")
                self.logger.log_info(f"Output: {result.stdout}")
                return result.stdout
            else:
                self.logger.log_error(f"Command failed: {command}")
                self.logger.log_error(f"Error: {result.stderr}")
                return None
        except Exception as e:
            self.logger.log_error(f"Error executing command: {e}")
            return None

if __name__ == "__main__":
    executor = AgentExecutor()
    command = "echo Hello, Kyrios!"
    executor.execute_command(command)
