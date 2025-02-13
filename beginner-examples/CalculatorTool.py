from langchain_community.tools import tool


@tool("Calculator")
def calculate(equation):
    """ Useful for solving math equations """

    return eval(equation)
