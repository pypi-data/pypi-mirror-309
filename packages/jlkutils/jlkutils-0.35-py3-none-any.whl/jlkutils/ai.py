from openai import OpenAI
import ollama

client = OpenAI()

def chatgpt(input):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": input
            }
        ]
    )

    return completion.choices[0].message.content
    
def dalle(input):
    response = client.images.generate(
      model="dall-e-3",
      prompt=input,
      size="1024x1024",
      quality="standard",
      n=1,
    )

    return response.data[0].url
    
def ollama(prompt, model=llama3.2):
    response = ollama.chat(model=model, messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])
    return response['message']['content']