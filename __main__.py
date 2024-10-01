from llama_index.llms.anthropic import Anthropic
from llama_index.core.llms import ChatMessage, MessageRole, ChatResponse
import os
from rich import print as rprint
from tqdm import tqdm
import json
from prompts import CANDIDATE_PROMPT_SYSTEM, INTERVIEWER_PROMPT_SYSTEM


class Interview:
    """
    The Interview class facilitates the management of an interview process by handling messages between an interviewer and a candidate.
    Attributes:
        messages_interviewer (list): A list of messages from the interviewer.
        messages_candidate (list): A list of messages from the candidate.
        interactions (list): A list of interactions between the interviewer and the candidate.
    Methods:
        __init__(interviewer_system_prompt, candidate_system_prompt):
            Initializes the Interview class with system prompts for both the interviewer and the candidate.
        add_interaction(role: str, message: str):
            Adds an interaction to the interactions list.
        generate_question_to_candidate(question: str):
            Generates a list of messages for the candidate, including a new question.
        update_interviewer_messages(message: str):
            Updates the interviewer's messages with a new message and a prompt to ask a question.
        export_json(filename: str):
            Exports the interactions to a JSON file.
    """

    messages_interviewer: list
    messages_candidate: list
    interactions: list

    def __init__(self, interviewer_system_prompt, candidate_system_prompt):
        self.messages_interviewer = [
            ChatMessage(role=MessageRole.SYSTEM, content=interviewer_system_prompt),
            ChatMessage(role=MessageRole.USER, content="Ask a question"),
        ]
        self.messages_candidate = [
            ChatMessage(role=MessageRole.SYSTEM, content=candidate_system_prompt)
        ]
        self.interactions = []

    def add_interaction(self, role: str, message: str):
        self.interactions.append({"role": role, "message": message})

    def generate_question_to_candidate(self, question: str):
        return self.messages_candidate + [
            ChatMessage(role=MessageRole.USER, content=question)
        ]

    def update_interviewer_messages(self, message: str):
        self.messages_interviewer += [
            ChatMessage(role=MessageRole.ASSISTANT, content=message),
            ChatMessage(
                role=MessageRole.USER,
                content="Ask a question, return only the question:",
            ),
        ]

    def export_json(self, filename: str):
        with open(filename, "w") as f:
            json.dump(self.interactions, f, indent=4)


def get_agent(model_name: str = "claude-3-haiku-20240307") -> Anthropic:
    llm = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], model=model_name)
    return llm


def conduct_interview(
    interactions: int = 2,
    field: str = "Machine Learning Engineer",
    domain: str = "Machine Learning",
    filename: str = "interview.json",
):
    interviewer = get_agent()
    candidate = get_agent(model_name="claude-3-opus-20240229")
    interview: Interview = Interview(
        interviewer_system_prompt=INTERVIEWER_PROMPT_SYSTEM.format(
            field=field, domain=domain
        ),
        candidate_system_prompt=CANDIDATE_PROMPT_SYSTEM.format(field=field),
    )
    for _ in tqdm(range(interactions)):
        question: str = interviewer.chat(
            interview.messages_interviewer
        ).message.content.__str__()
        candidate_message: ChatResponse = candidate.chat(
            interview.generate_question_to_candidate(question)
        )
        # add the interaction to not ask the same question again
        interview.update_interviewer_messages(question)
        # log the conversation
        interview.add_interaction(role="Interviewer", message=question)
        interview.add_interaction(
            role="Candidate", message=candidate_message.message.content.__str__()
        )
    interview.export_json(filename)


if __name__ == "__main__":
    conduct_interview(
        interactions=15,
        field="Software Engineer",
        domain="ML and AI",
        filename="software_engineer_ml_and_ai.json",
    )
