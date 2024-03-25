import openai
#chatgpt 调用示例
openai.api_key = ""
openai.api_base = "https://api.openai-proxy.com/v1"

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "nginx如何代理hfish"}
    ]
)

print(completion.choices[0].message.content)
