import argparse
from ast import List
import os
import openai 
import Env
import re

MAX_INPUT_LENGTH = 32

def main():
    print('Running application...')

    parser = argparse.ArgumentParser()
    parser.add_argument('--input',"-i",type=str)
    args = parser.parse_args()
    user_input = args.input

    print(f'User input: {user_input}')
    if validate_prompt(user_input):
        result_branding = generate_branding_snippet(user_input)
        result_keywords = generate_keywords(user_input)

        print(result_branding)
        print(result_keywords)
    else:
        raise ValueError('O tamanho do prompt não é valido. Dimiuir o texto!')

def validate_prompt(prompt: str) -> bool:
    return len(prompt) <= MAX_INPUT_LENGTH


def  generate_keywords(prompt: str) -> List:
    # Load your API key from an environment variable or secret management service
    # return Env.env()
    openai.api_key = Env.env()
    # return openai.api_key
    # return
    enriched_prompt = f"Gerar uma lista de palavras separadas por vírgula para o seguinte tópico: {prompt}"
    response = openai.Completion.create(model="text-davinci-003", 
                                        prompt=enriched_prompt, 
                                        temperature=0, 
                                        max_tokens=MAX_INPUT_LENGTH)

    keyword_text: str = response['choices'][0]['text']
    # return [keyword_text]
    keyword_array = re.split(",|;|-|\n",keyword_text)
    keyword_array = [k.strip() for k in keyword_array]
    keyword_array = [k for k in keyword_array if len(k) > 0]
    return keyword_array
    
def  generate_branding_snippet(prompt: str) -> str:
    # Load your API key from an environment variable or secret management service
    # return Env.env()
    openai.api_key = Env.env()
    # return openai.api_key
    # return
    enriched_prompt = f"Gerar um slogan para promover meu curso de {prompt}"
    response = openai.Completion.create(model="text-davinci-003", 
                                        prompt=enriched_prompt, 
                                        temperature=0, 
                                        max_tokens=32)
    # print(response)
    #Extract the output text
    branding_text: str = response['choices'][0]['text']

    #Strip whitespace
    branding_text = branding_text.strip()

    #Add ... to truncated statements
    last_char = branding_text[-1]
    if last_char not in {'.','!','?'}:
        branding_text += '...'

    return branding_text

if __name__ == "__main__":
    main()
    