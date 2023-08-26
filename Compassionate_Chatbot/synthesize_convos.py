import os
import openai
from time import time,sleep


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_convo(text, topic):
    with open('finetuning_mt3/%s_%s.txt' % (topic, time()), 'w', encoding='utf-8') as outfile:
        outfile.write(text)


openai.api_key = "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"

def gpt3_completion(prompt, engine='gpt-4', temp=0.7, top_p=0.5, tokens=1000, freq_pen=0.0, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            message=[{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages = message,
                temperature=0.9,
                max_tokens=3000,
                frequency_penalty=0.0
                )
            
            print(response)
            text = response['choices'][0]['message']['content'].strip()
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT4 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(0.25)


if __name__ == '__main__':
    topics = open_file('topics2.txt').splitlines()
    for topic in topics:
        print(topic)
        prompt = open_file('syn_prompt1.txt').replace('<<TOPIC>>', topic)
        response = gpt3_completion(prompt)
        outtext = '%s' % response
        print(outtext)
        tpc = topic.replace(' ', '')[0:15]
        save_convo(outtext, tpc)
        #exit()
        