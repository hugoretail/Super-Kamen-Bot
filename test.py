import ollama

response = ollama.chat(model='llama2:7b-chat', messages=[
  {'role':'user','content':'Translate this in Japanese: "My cat is brown."'}
])

print(response['message']['content'])