from common.States import State
from common.client import llm, tavily_client
import uuid
from langchain_core.messages import HumanMessage
from langgraph.graph import START, END, StateGraph


# --- NODE IMPLEMENTATIONS ---
def ask_user_node(state: State) -> State:
    """Ask the patient what health topic or condition they’d like to learn about."""
    topic = input(
        "What health topic or medical condition would you like to learn about? "
    )
    state.input = topic
    state.messages.append(HumanMessage(content=topic, id=str(uuid.uuid4())))
    return state


def tavily_search_node(state: State) -> State:
    """Search Tavily for the patient’s topic."""
    response = tavily_client.search(state.input)
    state.output = response
    return state


def summarize_conversation(state: State) -> State:
    """Summarize Tavily results in patient-friendly language."""
    summary_prompt = HumanMessage(
        content=f"Summarize the following health information for a patient in simple, easy-to-understand language:\n\n{state.output}"
    )
    ai_message = llm.invoke([summary_prompt])
    ai_message.id = str(uuid.uuid4())

    state.summary = ai_message.content
    state.messages.append(ai_message)
    return state


def present_summary_node(state: State) -> State:
    """Present the summary to the patient."""
    print("\n--- Health Information Summary ---\n")
    print(state.summary)
    print("\n---------------------------------\n")
    return state


def wait_for_ready_node(state: State) -> State:
    """Wait until the patient is ready for the quiz."""
    ready = False
    while not ready:
        response = input("Are you ready for the quiz? Type 'ready' to continue: ")
        ready = response.strip().lower() == "ready"
    return state


def make_quiz_node(state: State) -> State:
    """Generate a one-question quiz from the health summary."""
    quiz_prompt = HumanMessage(
        content=f"Create a single quiz question (with expected answer) to test comprehension of this summary:\n\n{state.summary}"
    )
    ai_message = llm.invoke([quiz_prompt])
    ai_message.id = str(uuid.uuid4())

    state.quiz_question = ai_message.content
    state.messages.append(ai_message)
    return state


def present_question_node(state: State) -> State:
    """Present the quiz question to the patient."""
    print("\n--- Quiz Question ---\n")
    print(state.quiz_question)
    print("\n---------------------\n")
    return state


def collect_answer_node(state: State) -> State:
    """Collect the patient’s answer."""
    answer = input("Your answer: ")
    state.user_answer = answer
    state.messages.append(HumanMessage(content=answer, id=str(uuid.uuid4())))
    return state


def grade_node(state: State) -> State:
    """Grade the patient’s answer and provide justification with citations."""
    grader_prompt = HumanMessage(
        content=f"""
        Patient’s answer: {state.user_answer}
        Health summary: {state.summary}

        Grade the patient’s answer (Correct/Partially Correct/Incorrect).
        Provide justification for the grade and cite relevant parts of the health summary.
        """
    )
    grade_message = llm.invoke([grader_prompt])
    grade_message.id = str(uuid.uuid4())

    state.grade = grade_message.content
    state.messages.append(grade_message)
    return state


def present_grade_node(state: State) -> State:
    """Present the grade and feedback to the patient."""
    print("\n--- Quiz Feedback ---\n")
    print(state.grade)
    print("\n---------------------\n")
    return state


def restart_node(state: State) -> State:
    """Ask if the patient wants to restart or exit."""
    response = input("Would you like to learn about another health topic? (Y/N): ")
    state.restart = response.strip().lower() == "y"

    # Reset state if restarting 
    if state.restart:
        state.input = None
        state.output = None
        state.summary = None
        state.quiz_question = None
        state.user_answer = None
        state.grade = None
        state.messages = []

    return state


# Define graph
workflow = StateGraph(State)

# --- NODES ---
workflow.add_node("ask_user", ask_user_node)
workflow.add_node("search_tavily", tavily_search_node)
workflow.add_node("summarize", summarize_conversation)
workflow.add_node("present_summary", present_summary_node)
workflow.add_node("wait_ready", wait_for_ready_node)
workflow.add_node("make_quiz", make_quiz_node)
workflow.add_node("present_question", present_question_node)
workflow.add_node("collect_answer", collect_answer_node)
workflow.add_node("grade", grade_node)
workflow.add_node("present_grade", present_grade_node)
workflow.add_node("restart", restart_node)

# --- EDGES ---
workflow.add_edge(START, "ask_user")
workflow.add_edge("ask_user", "search_tavily")
workflow.add_edge("search_tavily", "summarize")
workflow.add_edge("summarize", "present_summary")
workflow.add_edge("present_summary", "wait_ready")
workflow.add_edge("wait_ready", "make_quiz")
workflow.add_edge("make_quiz", "present_question")
workflow.add_edge("present_question", "collect_answer")
workflow.add_edge("collect_answer", "grade")
workflow.add_edge("grade", "present_grade")
workflow.add_edge("present_grade", "restart")


# --- CONDITIONAL ENDING ---
def check_restart(state: State) -> str:
    return "ask_user" if state.restart else END


workflow.add_conditional_edges(
    "restart", check_restart, {"ask_user": "ask_user", END: END}
)

# Compile graph
app = workflow.compile()
