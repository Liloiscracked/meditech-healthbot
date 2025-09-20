from common.models import State

from common.client import open_ai_client, tavily_client


def ask_user_node(state: State) -> None:
    """
    Asks user for input
    """
    state["input"] = input(str("Ask your question"))


def tavily_search_node(state: State) -> None:
    """
    Return top search results for a given search query
    """
    response = tavily_client.search(state["input"])
    state["output"] = response
    return response


def summarize(state: State) -> None:
    open_ai_client(state["messages"][-1])


def present_summary_node(state: State) -> None:
    print(state["messages"][-1])


def wait_for_ready_node(state: State) -> None:
    ready = False
    while not ready:
        response = input("Are you ready for the quiz? Type 'ready'")
        ready = response == "ready"


def make_quiz_node(state: State):
    return


def present_question_node(state: State):
    return


def collect_answer_node(state: State):
    return


def grade_node(state: State):
    return


def presetn_grade_node(state: State):
    return


def restart_node(state: State):
    return
