from common.models import State
from common.tools.nodes import app

if __name__ == "__main__":
    print("=== Welcome to HealthBot: AI-Powered Patient Education System ===\n")
    # Start the workflow with an empty state
    final_state = app.invoke(State())
    print("\n=== Session Ended ===")
