from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentOutputParser
from typing import Union
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator

# class CustomOutputParser(AgentOutputParser):
#     thought = ""

#     def get_thought(self):
#         return self.thought  # Accessing class variable using self

#     def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
#         # Check if agent should finish
#         start_index = llm_output.find("Thought:") + len("Thought:")
#         end_index = llm_output.find("Question:")
#         thought = llm_output[start_index:end_index].strip()  # Removed global keyword and corrected variable name
#         self.thought = thought  # Assigning value to class variable
#         if "Question:" in llm_output:
#             return AgentFinish(
#                 return_values={"output": llm_output.split("Question:")[-1].strip()},
#                 log=llm_output,
#             )

class CustomOutputParser(AgentOutputParser):
    thought = ""

    def get_thought(self):
        return self.thought  # Accessing class variable using self

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        start_index = llm_output.find("Thought:") + len("Thought:")
        end_index = llm_output.find("Question:")
        thought = llm_output[start_index:end_index].strip()  # Removed global keyword and corrected variable name
        self.thought = thought  # Assigning value to class variable
        if "Question:" in llm_output:
            return AgentFinish(
                # return_values={"output": llm_output.split("Question:")[-1].strip()},
                return_values={"output": llm_output},
                log=llm_output,
            )



class Notes(BaseModel):
    medical_notes: str = Field(description="notes for the physician in String format")


class Diagnose(BaseModel):
    differentials: str = Field(description="Five comma seperated names of most probable diseases accrding to the symptoms in a String ")
    symptoms: str = Field(description="Formal list of symptoms in a String")
    indicators: str = Field(description="explain why this patient matches this diagnosis")
    treatment: str = Field(description="Available treatment options")
    tests: str = Field(description="Recommended follow up tests, and what you're looking for, probative information desired")
    referrals: str = Field(description="Names of the specialists for treatment")
