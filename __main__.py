from llama_index.llms.anthropic import Anthropic
from llama_index.core.llms import ChatMessage, MessageRole, ChatResponse
import os
from rich import print as rprint
from tqdm import tqdm
import json
from prompts import CANDIDATE_PROMPT_SYSTEM, INTERVIEWER_PROMPT_SYSTEM


class Interview:
    messages_interviewer: list
    messages_candidate: list

    def __init__(self, interviewer_system_prompt, candidate_system_prompt):
        self.messages_interviewer = [
            ChatMessage(role=MessageRole.SYSTEM, content=interviewer_system_prompt)
        ]
        self.messages_candidate = [
            ChatMessage(role=MessageRole.SYSTEM, content=candidate_system_prompt)
        ]

    def add_interviewer_message(self, message: str, first_message: bool = False):
        self.messages_interviewer.append(
            ChatMessage(role=MessageRole.ASSISTANT, content=message)
        )
        self.messages_candidate.append(
            ChatMessage(role=MessageRole.USER, content=message)
        )

    def add_candidate_message(self, message: str, first_message: bool = False):
        self.messages_interviewer.append(
            ChatMessage(role=MessageRole.USER, content=message)
        )
        if not first_message:
            self.messages_candidate.append(
                ChatMessage(role=MessageRole.ASSISTANT, content=message)
            )

    def export_json(self):
        interview = []
        for message in self.messages_interviewer:
            if message.role == MessageRole.SYSTEM:
                continue
            elif message.role == MessageRole.ASSISTANT:
                interview.append({"role": "Interviewer", "content": message.content})
            else:
                interview.append({"role": "Candidate", "content": message.content})
        with open("interview.json", "w") as f:
            json.dump(interview, f, indent=4)


def get_agent():
    llm = Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"], model="claude-3-haiku-20240307"
    )
    return llm


def conduct_interview(
    interactions: int = 2,
    field: str = "Machine Learning Engineer",
    domain: str = "machine learning",
):
    interviewer = get_agent()
    candidate = get_agent()
    interview: Interview = Interview(
        interviewer_system_prompt=INTERVIEWER_PROMPT_SYSTEM.format(
            field=field, domain=domain
        ),
        candidate_system_prompt=CANDIDATE_PROMPT_SYSTEM.format(field=field),
    )
    interview.add_candidate_message(
        "Hi can we start the interview?", first_message=True
    )
    for _ in tqdm(range(interactions)):
        interviewer_message: ChatResponse = interviewer.chat(
            interview.messages_interviewer
        )
        interview.add_interviewer_message(interviewer_message.message.content.__str__())
        candidate_message: ChatResponse = candidate.chat(interview.messages_candidate)
        interview.add_candidate_message(candidate_message.message.content.__str__())
    interview.export_json()


if __name__ == "__main__":
    conduct_interview(interactions=2, field="Machine Learning Engineer", domain="NPL")
