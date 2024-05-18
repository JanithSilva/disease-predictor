from llm_chatbot.llm import InferenceLLM
from langchain.agents import AgentExecutor
from llm_chatbot.parsers import CustomOutputParser, Notes, Diagnose
from llm_chatbot.template import question_template, medical_note_template, diagnose_template
from .QnA import QnA_Agent, Diagnose_Chain, Notes_Chain


llm = InferenceLLM.get_instance()
output_parser_QnA = CustomOutputParser()
medical_notes_chain = Notes_Chain.get_notes_chain(llm, Notes, medical_note_template)
diagnose_chain  = Diagnose_Chain.get_diagnose_chain(llm, Diagnose, diagnose_template)


def get_QnA_agent_executor(memory): 
    agent_executor = AgentExecutor.from_agent_and_tools(
    agent= QnA_Agent.get_QnA_agent(llm, question_template, output_parser_QnA),
    tools=[],
    verbose=True,
    memory=memory
    )
    return agent_executor


def run_QnA_agent_executer(input, memory):
    agent_executor = get_QnA_agent_executor(memory)
    llm_output = agent_executor.run(input)

    #extracting thought
    start_index = llm_output.find("Thought:") + len("Thought:")
    end_index = llm_output.find("Question:")
    thought = llm_output[start_index:end_index].strip() 

    #extracting question
    question = llm_output.split("Question:")[-1].strip()

    return {"thought":thought,"question":question}


def prepare_medical_notes(memory):
    chat_log = memory.buffer_as_str
    notes = medical_notes_chain.predict(patient_intake_transcription = chat_log)
    return notes.medical_notes

def disgnose(medical_notes):
    diagnose = diagnose_chain.predict(patient_chart=medical_notes)
    return diagnose


  
    





  



