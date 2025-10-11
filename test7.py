from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from operator import add


class State(TypedDict):
    user_input: str
    node_output: Annotated[list[int], add]


count = 0


def first_node(state):
    print("I'm here")
    global count
    count += 1
    return {'node_output': [count]}


def second_node(TypedDict):
    print("He sent me here")
    global count
    count += 2
    return {'node_output': [count]}


def third_node(TypedDict):
    print('I was decided')
    global count
    count += 3
    return {'node_output': [count]}


def fourth_node(TypedDict):
    print("I'm here on chance")
    global count
    count += 4
    return {'node_output': [count]}


def decide_mood(state):
    current_count = state['node_output'][-1]
    if current_count % 2 == 0:
        print(
            f"Deciding mood: current_count {current_count} is even. Going to 'to_node_3'.")
        return "node_3"
    else:
        print(
            f"Deciding mood: current_count {current_count} is odd. Going to 'to_node_4'.")
        return "node_4"

# starting graph building


builder1 = StateGraph(State)

builder1.add_node('node_1', first_node)
builder1.add_node('node_2', second_node)
builder1.add_node('node_3', third_node)
builder1.add_node('node_4', fourth_node)

builder1.add_edge(START, 'node_1')
builder1.add_edge('node_1', 'node_2')
builder1.add_conditional_edges('node_2', decide_mood, {
    "node_3": "node_3",
    "node_4": "node_4",
})
builder1.add_edge('node_3', END)
builder1.add_edge('node_4', END)

my_new_graph = builder1.compile()


my_new_graph.invoke({"user_input": "hi"})
