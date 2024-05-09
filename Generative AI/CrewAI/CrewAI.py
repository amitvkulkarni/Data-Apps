import os
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process


# Set the environment variable for the Google API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# Set gemini pro as llm
llm = ChatGoogleGenerativeAI(model="gemini-pro", verbose=True, temperature=0.6)


researcher = Agent(
    role="Senior Finance Analyst",
    goal="Fetch the stock value of Tesla Inc.",
    backstory="""You work at a leading investment banking think tank.
  Your expertise lies analysis data and you have a knack for dissecting complex data and presenting
  actionable insights. Keep the report simple and easy to understand within 300 words""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)


analyst = Agent(
    role="Investor",
    goal="Highlight the key metrics of Tesla Inc. stock value",
    backstory="""You are a renowned analyst and investor, known for
  your number crunching and insights from data. You transform complex concepts into compelling narratives.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

designer = Agent(
    role="Visualizer",
    goal="Visualize the key metrics from task2 using a graph",
    backstory="""You are a renowned graphics designer known for amazing visualization of numbers and great story telling""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)


# Create tasks for your agents
task1 = Task(
    description="""Conduct a comprehensive analysis, get the key stock metrics and 
  your final answer MUST be a paragraph not exceeding 100 words.""",
    expected_output="""A detailed report summarizing key findings highlighting information that could be relevant for the research.""",
    agent=researcher,
)


task2 = Task(
    description="""Using the content from task1, highlight key metrics.  
  Avoid complex words so it doesn't sound like AI.
  """,
    expected_output="""A blog highlighting findings from the research.""",
    agent=analyst,
)

task3 = Task(
    description="""Visualize the key metrics from task2 using a graph""",
    expected_output="""write a python code and create a chart using the findings from the research.""",
    agent=designer,
)


# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, analyst, designer],
    tasks=[task1, task2, task3],
    verbose=1,
)


# Get your crew to work!
result = crew.kickoff()
