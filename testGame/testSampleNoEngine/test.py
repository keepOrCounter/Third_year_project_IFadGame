import openai

# Set up the OpenAI API client
openai.api_key = "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"

# Set up the model and prompt
prompt = """This is the key info from an advanture game, could you please write a short description to players? Here is an exmaple of description in another game:"At End Of Road
You are standing at the end of a road before a small brick building. Around you
is a forest. A small stream flows out of the building and down a gully. 
There are some keys on the ground here." Now please give a short description. key info: {
	"location": "Edge of cliff",
	"Interactive object": {
		"unportable": ["stream(∞)", "bare rock(∞)"], 
		"portable": ["empty bottle(1)"]
	}
}"""

# Generate a response
response = openai.ChatCompletion.create(
model="gpt-3.5-turbo",#gpt-3.5-turbo-0301
messages=[
{"role": "user", "content": prompt}
],
temperature=0.5,
max_tokens=1000,
top_p=1,
frequency_penalty=0,
presence_penalty=0,
)

print(response.choices[0].message.content)
