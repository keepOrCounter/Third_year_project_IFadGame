from sample import Gpt3

systemRole = "" #put your test system config here, which is use to tell gpt about \
    #context and define the style of response

prompt = "" # put your test prompt here

GptWarpper = Gpt3("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", systemRole, "")

print(GptWarpper.inquiry(prompt)) # gpt response will be printed here