from openai import OpenAI
client = OpenAI()

sys_role = input('Please provide how you would like the system to respond to the user:\n(e.g. "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.")\n')
print('\n'*3)
usr_message = input('Please provide the user message:\n(e.g. "Compose a poem that explains the concept of closure in programming.")\n')

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": sys_role},
    {"role": "user", "content": usr_message}
  ]
)

print(completion.choices[0].message.content)