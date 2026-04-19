from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url 
from dotenv import load_dotenv

load_dotenv()

#model setup 
llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature=0)


#1st agent 
def build_search_agent():
    return create_agent(
        model = llm,
        tools= [web_search]
    )

#2nd agent 

def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer and senior analyst. Write clear, structured, and visually appealing reports."),
    ("human", """Write a highly structured research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report EXACTLY as follows:

# [An Engaging Title for the Report]

## Key Insights
- Insight 1
- Insight 2
- Insight 3

## [Section 1 Title]
...content...

## [Section 2 Title]
...content...

## References
- [Source Title 1](URL 1)
- [Source Title 2](URL 2)

Rules:
- Be detailed, factual, and professional.
- Use well-spaced paragraphs and bullet points for readability.
- The "References" section must strictly be a bulleted list of markdown links: `- [Title](URL)`"""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()

