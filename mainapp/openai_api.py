import requests

def generate_answer(prompt, api_key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "prompt": prompt,
        "model": "text-davinci-003",
        "max_tokens":1500,
        "stop":"."
    }

    resp = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)

    if resp.status_code != 200:
        raise ValueError("Failed to generate answer "+resp.text)

    return resp.json()['choices'][0]['text']

def generate_prompt_for_mum(answers):
    prompt = "You are an expert writer specializing in helping adult children write moving messages and declarations of love and gratitude to their mothers. \
        You are writing a message for a mother called [INSERT ANSWER Q:1], from her [INSERT ANSWER Q:2] [INSERT ANSWER Q:3].\
        [INSERT ANSWER Q:3] truly loves her mother and he is incredibly grateful for all that her mother, [INSERT ANSWER Q:1] has done for her throughout her life.\
        Your goal is to use emotional, touching and heartfelt language that is so moving that [INSERT ANSWER Q:1] will cry of joy when reading this declaration of love from her [INSERT ANSWER Q:2].\
        Here is some background information that you can use to make the the message more personal:\
        1. [INSERT ANSWER Q:1] is [INSERT ANSWER Q:4] years old.\
        2. [INSERT ANSWER Q:1] grew up in [INSERT ANSWER Q:5].\
        3. [INSERT ANSWER Q:3], her [INSERT ANSWER Q:2] is [INSERT ANSWER Q:6] years old.\
        4. [INSERT ANSWER Q:1] has recently experienced [INSERT ANSWER Q:7]\
        6. [INSERT ANSWER Q:1] helped [INSERT ANSWER Q:3] overcome the challenge of [INSERT ANSWER Q:8]\
        7. [INSERT ANSWER Q:1] faced the challenge of [INSERT ANSWER Q:9] whilst growing up\
        8. [INSERT ANSWER Q:1] faced the challenge of [INSERT ANSWER Q:10] as an adult.\
        9. An adventure or exciting thing [INSERT ANSWER Q:1] has experienced is [INSERT ANSWER Q:11]\
        10. Three of [INSERT ANSWER Q:1] best character traits are [INSERT ANSWER Q:12]\
        11. A wonderful memory [INSERT ANSWER Q:3] has with [INSERT ANSWER Q:1] is [INSERT ANSWER Q:13]\
        12. [INSERT ANSWER Q:3] wants [INSERT ANSWER Q:1] to know that [INSERT ANSWER Q:14]"
    
    for i in range(1, len(answers)+1):
        strToken = "[INSERT ANSWER Q:"+ str(i) + "]"
        print("aaaaaa   "+ strToken + "answer " + answers[i-1])
        strAnswer = answers[i-1]
        prompt = prompt.replace(strToken, strAnswer)
    prompt = prompt + "."
    return prompt    
def generate_prompt(type, answers):
    prompt = ""
    if type == 1:
        prompt = generate_prompt_for_mum(answers)
    elif type == 2:
        prompt = generate_prompt_for_mum(answers)
    else:
        prompt = generate_prompt_for_mum(answers)
    print("prompt    " + prompt)
    return prompt


