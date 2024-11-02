import pandas as pd
import config

genai.configure(api_key=config.Gemini_API)

model = genai.GenerativeModel('gemini-pro')

def get_time(prompt:str):
    print(prompt)