from langchain.chains import LLMChain
from langchain.agents import LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain.agents import Tool
from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate


#this is for formating the template for the Q&A agent
class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)


class QnA_Agent:
    _instance = None
    
    @classmethod
    def get_QnA_agent(cls, llm, question_template, output_parser_QnA):
        if cls._instance is None:
            cls._instance = cls._create_instance(llm, question_template, output_parser_QnA)
        return cls._instance

    @classmethod
    def _create_instance(cls, llm, question_template, output_parser_QnA):
        prompt_with_history = CustomPromptTemplate(
            template=question_template,
            tools=[],
            input_variables=["history", "intermediate_steps", "input"]
        )
        lm_chain = LLMChain(llm=llm, prompt=prompt_with_history)
        agent = LLMSingleActionAgent(
            llm_chain=lm_chain,
            output_parser=output_parser_QnA,
            stop=["patient's response:", "\n\npatient:", "\n\npatient:"],
            allowed_tools=[]
        )
        return agent

    
class Notes_Chain:
    _instance = None

    @classmethod
    def get_notes_chain(cls, llm, Notes, medical_note_template):
        if cls._instance is None:
            cls._instance = cls._create_instance(llm, Notes, medical_note_template)
        return cls._instance

    @classmethod
    def _create_instance(cls, llm, Notes, medical_note_template):
        pydantic_message_parser = PydanticOutputParser(pydantic_object=Notes)
        format_message_instructions = pydantic_message_parser.get_format_instructions()

        message_prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(medical_note_template)
            ],
            input_variables=["patient_intake_transcription"],
            partial_variables={"format_instructions": format_message_instructions}
        )

        notes_chain = LLMChain(prompt=message_prompt, llm=llm, output_parser=pydantic_message_parser)

        return notes_chain

    
class Diagnose_Chain:
    _instance = None

    @classmethod
    def get_diagnose_chain(cls, llm, Diagnose, diagnose_template):
        if cls._instance is None:
            cls._instance = cls._create_instance(llm, Diagnose, diagnose_template)
        return cls._instance

    @classmethod
    def _create_instance(cls, llm, Diagnose, diagnose_template):
        pydantic_message_parser = PydanticOutputParser(pydantic_object=Diagnose)
        format_message_instructions = pydantic_message_parser.get_format_instructions()

        message_prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(diagnose_template)
            ],
            input_variables=["patient_intake_transcription"],
            partial_variables={"format_instructions": format_message_instructions}
        )

        diagnose_chain = LLMChain(prompt=message_prompt, llm=llm, output_parser=pydantic_message_parser)
        return diagnose_chain

    







    
            
        


        
