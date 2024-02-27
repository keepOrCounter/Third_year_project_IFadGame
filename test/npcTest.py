import openai
import random

class Gpt3():
    def __init__(self, api_key, output_systemRole:str, command_translator_systemRole:str) -> None:
        # Set up the OpenAI API client
        openai.api_key = api_key
        self.output_systemRole = output_systemRole
        self.command_translator_systemRole = command_translator_systemRole

    def inquiry(self, prompt:str) -> str:
        # Generate a response
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",#gpt-3.5-turbo-0301
        messages=[
        {"role": "system", "content": self.output_systemRole},
        {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        )

        # print(response.choices[0].message.content)
        return response.choices[0].message.content
    
    def command_translator(self, user_command):
        # Generate a response
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",#gpt-3.5-turbo-0301
        messages=[
        {"role": "system", "content": self.command_translator_systemRole},
        {"role": "user", "content": user_command}
        ],
        temperature=0.5,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        )

        # print(response.choices[0].message.content)
        return response.choices[0].message.content

characterChart = ["hardy", "lonely", "adamant", "naughty", "brave", "bold", "docile", "impish", "lax", "relaxed", "modest",\
"mild", "bashful", "rash", "quiet", "calm", "gentle", "careful", "quirky", "sassy", "timid", "hasty", "jolly", "naive", "serious"]

ageChart = str(random.randint(1,99))

genderChart = ["male", "female"]

systemRole = "You are an NPC from an interactive novel with a different world theme. You are a " + random.choice(genderChart) \
+","+ ageChart +" years old, and have a "+ random.choice(characterChart) + " personality. When entering a greeting sentence, you\
need to have a conversation with me and generate some life content based on your gender, age and personality."

prompt = input()

GptWarpper = Gpt3("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", systemRole, "")

print(GptWarpper.inquiry(prompt)) 