from common.States import State
from common.nodes import app

print("=== Welcome to HealthBot: AI-Powered Patient Education System ===\n")
# Start the workflow with an empty state
final_state = app.invoke(State())
print("\n=== Session Ended ===")