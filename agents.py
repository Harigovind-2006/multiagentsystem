from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [web_search, scrape_url]

#first agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools= [web_search],
    )

#second agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools= [scrape_url],
    )


#writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write a clear, structured and insightful report"),
    ("human", """Write a detailed research report on the following topic:
    
    Topic: {topic}
    
    Research Gathered:
    {research}
    
    Structure the report as follows:
    - Introduction
    - Key findings
    - Analysis
    - Conclusion
    - Citations

    Be detailed, Factual and Professional.  """),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constuctive research critiv. Be honest and Specific"),
    ("human", """Review the Reasearch report below and evaluate it strictly.
    
    Report: {report}
    
    Respond in this exact format:

    Score: X/10

    Strengths:
    -...
    -...
    -...

    Area to improve:
    -...
    -...
    -...

    One line Verdict:
    -...

     """),
])

critic_chain = critic_prompt | llm | StrOutputParser()

#reviewer chain
reviewer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful editor. Your job is to make the report better based on the critic's feedback."),
    ("human", """You are reviewing a research report. Use the critic's feedback to improve it.
    
    Original Report: {report}
    
    Critic's Feedback: {feedback}
    
    Your Task:
    - Rewrite the report to address the critic's points
    - Keep the tone professional and factual
    - Improve clarity and structure
    - Add or correct information where needed
    - Ensure the final report is polished and accurate
    
    Output the revised report:"""),
])

reviewer_chain = reviewer_prompt | llm | StrOutputParser()

