import os
from langchain_community.llms import HuggingFaceTextGenInference
from dotenv import load_dotenv

from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

"""
Initialize llm for inference
"""
class InferenceLLM:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._create_instance()
        return cls._instance

    @classmethod
    def _create_instance(cls):
        load_dotenv()  # Load environment variables from .env file
        inference_server_url = "http://94.61.157.224:53709"#os.getenv('INFERENCE_SERVER_URL')
        llm = HuggingFaceTextGenInference(
            inference_server_url=inference_server_url,
            max_new_tokens=1000,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            repetition_penalty=1.00,
        )
        return llm

# class InferenceLLM:
#     _instance = None

#     @classmethod
#     def get_instance(cls):
#         if cls._instance is None:
#             cls._instance = cls._create_instance()
#         return cls._instance

#     @classmethod
#     def _create_instance(cls):
#         load_dotenv()  # Load environment variables from .env file
#         endpoint_url = "http://31.12.82.146:21012"#os.getenv('INFERENCE_SERVER_URL')
#         llm = HuggingFaceEndpoint(
#             endpoint_url=endpoint_url,
#             max_new_tokens=1000,
#             top_k=10,
#             top_p=0.95,
#             typical_p=0.95,
#             temperature=0.01,
#             repetition_penalty=1.00,
#             huggingfacehub_api_token = "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"
#         )
#         return llm
    

