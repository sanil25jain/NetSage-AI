import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqLLM:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is not set."
            )

        self.client = Groq(api_key=api_key)

        self.model = "openai/gpt-oss-20b"

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are NetSage AI, a network diagnostic "
                        "assistant specializing in Cisco IOS and "
                        "Cisco Packet Tracer."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "network_diagnosis",
                    "strict": True,

                    "schema": {
                        "type": "object",

                        "properties": {

                            "root_cause": {
                                "type": "string"
                            },

                            "osi_layer": {
                                "type": "string"
                            },

                            "confidence": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1
                            },

                            "evidence": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },

                            "next_command": {
                                "type": "string"
                            },

                            "fix_steps": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            }
                        },

                        "required": [
                            "root_cause",
                            "osi_layer",
                            "confidence",
                            "evidence",
                            "next_command",
                            "fix_steps"
                        ],

                        "additionalProperties": False
                    }
                }
            }
        )

        return response.choices[0].message.content