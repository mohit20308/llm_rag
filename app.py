import requests
import streamlit as st

import translatePlay

st.title("RAG based LLM")
tab1, tab2, tab3 = st.tabs(['Part 1', 'Part 2', 'Part 3'])

debug_mode = True

def get_part1_response(input_text):
    response = requests.post("http://localhost:8000/part1/invoke", json={'input': {'input': input_text}})
    return response.json()

def get_part2_response(input_text):
    response = requests.post("http://localhost:8000/part2/invoke", json={'input': {'input': input_text}})
    return response.json()

def get_part3_response(input_text):
    response = requests.post("http://localhost:8000/part3/invoke", json={'input': {'input': input_text}})
    return response.json()

with tab1:
    input_text = st.text_input("Write your query!", key = 'user_input_1')

    if input_text:
        st.markdown('**Output**')
        output = get_part1_response(input_text)['output']['answer']
        if debug_mode:
            print('Answer to Part 1', output)
        st.container(border=True).write(output)

with tab2:
    input_text = st.text_input("Write your query!", key = 'user_input_2')

    if input_text:
        st.markdown('**Output**')
        output = get_part2_response(input_text)['output']['output']
        if debug_mode:
            print('Answer to Part 2', output)
        st.container(border=True).write(output)
        

with tab3:
    input_text = st.text_input("Write your query!", key = 'user_input_3')

    if input_text:
        st.markdown('**Output**')
        output = get_part3_response(input_text)['output']['output']
        if debug_mode:
            print('Answer to Part 3', output)
        st.container(border=True).write(output)

        translate_obj = translatePlay.TranslateTTS()
        translated_text = translate_obj.translate_text(output)
        st.markdown('**Translated Text (Sarvam Translation English to Hindi)**')
        st.container(border=True).write(translated_text)

        st.markdown('**Sarvam Text to Speech**')
        message = translate_obj.tts(translated_text)
        if 'File Created':
            st.audio(data='output.wav', format='audio/wav', autoplay=True)