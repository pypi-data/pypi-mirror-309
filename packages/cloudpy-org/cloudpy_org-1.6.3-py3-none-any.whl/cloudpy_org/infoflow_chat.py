"""
███████████████████████████infoflow_chat of cloudpy_org███████████████████████████
Copyright © 2023-2024 Cloudpy.org

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Find documentation at https://www.cloudpy.org
"""
from cloudpy_org import processing_tools
import os
import openai
import pyttsx3
import soundfile
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
class cloudpy_org_customizable_chatbot:
    def __init__(self
                 ,cloudpy_org_aws_framework_client:object=None
                 ,duration_in_secs:int=0
                 ,language:str='en_US'
                 ,model_provider:str='openai'
                 ,model_name:str='gpt-4o-mini'
                 ,type_of_request:str="default"
                 ,api_key:str=None
                 ,api_organization:str=None):
        model_name = model_name.lower().replace(' ','')
        self.co_fclient = cloudpy_org_aws_framework_client
        self.accepted_models = {}
        self.accepted_models['openai'] = ['gpt-4o-mini','gpt-4o','gpt-4','gpt-4-turbo']
        self.possible_models=[]
        self.type_of_request = type_of_request
        self.model_name = model_name
        self.total_tokens_used = 0
        self.last_answer = ""
        self.__s = {}
        k1 = 'default'
        self.__s[k1] = {}
        k2 = 'content'
        self.__s[k1][k2] = ""
        k2 = 'temperature'
        self.__s[k1][k2] = 0
        k2 = 'max_tokens'
        self.__s[k1][k2] = 256
        k2 = 'top_p'
        self.__s[k1][k2] = 1
        k2 = 'frequency_penalty'
        self.__s[k1][k2] = 0
        k2 = 'presence_penalty'
        self.__s[k1][k2] = 0
        #_____________________________________________
        k1 = 'unstructured_data_to_csv'
        self.__s[k1] = {}
        k2 = 'content'
        self.__s[k1][k2] = "You will be provided with unstructured data, and your task is to parse it into CSV format."
        k2 = 'temperature'
        self.__s[k1][k2] = 0
        k2 = 'max_tokens'
        self.__s[k1][k2] = 256
        k2 = 'top_p'
        self.__s[k1][k2] = 1
        k2 = 'frequency_penalty'
        self.__s[k1][k2] = 0
        k2 = 'presence_penalty'
        self.__s[k1][k2] = 0
        #_____________________________________________
        k1 = 'explain_code'
        self.__s[k1] = {}
        k2 = 'content'
        self.__s[k1][k2] = "You will be provided with a piece of code, and your task is to explain it in a concise way."
        k2 = 'temperature'
        self.__s[k1][k2] = 0
        k2 = 'max_tokens'
        self.__s[k1][k2] = 1024
        k2 = 'top_p'
        self.__s[k1][k2] = 1
        k2 = 'frequency_penalty'
        self.__s[k1][k2] = 0
        k2 = 'presence_penalty'
        self.__s[k1][k2] = 0
        #_____________________________________________
        k1 = 'create_instructions'
        self.__s[k1] = {}
        k2 = 'content'
        self.__s[k1][k2] = "You will be provided with a text, and your task is to create a numbered list of step-by-step directions from it."
        k2 = 'temperature'
        self.__s[k1][k2] = 0.3
        k2 = 'max_tokens'
        self.__s[k1][k2] = 256
        k2 = 'top_p'
        self.__s[k1][k2] = 1
        k2 = 'frequency_penalty'
        self.__s[k1][k2] = 0
        k2 = 'presence_penalty'
        self.__s[k1][k2] = 0
        #_____________________________________________
        k1 = 'natural_language_sql'
        self.__s[k1] = {}
        k2 = 'content'
        self.__s[k1][k2] = "Given the following SQL tables, your job is to write queries given a user’s request.\n\n@tables"
        k2 = 'temperature'
        self.__s[k1][k2] = 0
        k2 = 'max_tokens'
        self.__s[k1][k2] = 1024
        k2 = 'top_p'
        self.__s[k1][k2] = 1
        k2 = 'frequency_penalty'
        self.__s[k1][k2] = 0
        k2 = 'presence_penalty'
        self.__s[k1][k2] = 0
        self.gpt_default = ''\
        'response = openai.ChatCompletion.create('\
        'model="@gpt_version"'\
        ',messages=[{"role": "system","content": "@content"},@input]'\
        ',temperature=@temperature'\
        ',max_tokens=@max_tokens'\
        ',top_p=@top_p'\
        ',frequency_penalty=@frequency_penalty'\
        ',presence_penalty=@presence_penalty'\
        ')'
        self.available_languages = {'ar_SA',
                                    'cs_CZ',
                                    'da_DK',
                                    'de_DE',
                                    'el_GR',
                                    'en-scotland',
                                    'en_AU',
                                    'en_GB',
                                    'en_IE',
                                    'en_IN',
                                    'en_US',
                                    'en_ZA',
                                    'es_AR',
                                    'es_ES',
                                    'es_MX',
                                    'fi_FI',
                                    'fr_CA',
                                    'fr_FR',
                                    'he_IL',
                                    'hi_IN',
                                    'hu_HU',
                                    'id_ID',
                                    'it_IT',
                                    'ja_JP',
                                    'ko_KR',
                                    'nb_NO',
                                    'nl_BE',
                                    'nl_NL',
                                    'pl_PL',
                                    'pt_BR',
                                    'pt_PT',
                                    'ro_RO',
                                    'ru_RU',
                                    'sk_SK',
                                    'sv_SE',
                                    'th_TH',
                                    'tr_TR',
                                    'zh_CN',
                                    'zh_HK',
                                    'zh_TW'}
        self.language = language
        self.duration_in_secs = duration_in_secs
        self.__known_facts = {}
        self.__openai_api_key = api_key
        self.__openai_api_organization = api_organization
        openai.organization = self.__openai_api_organization
        openai.api_key = self.__openai_api_key
    def set_chatbot_context_local(self,file_path:str):
        self.__known_facts = {}
        with open(file_path,'r') as f:
            self.__known_facts["file_input"] = f.read()
        self.__set_messages()
    def set_chatbot_context_direct(self,context:str):
        self.__known_facts = {}
        self.__known_facts["file_input"] = context
        self.__set_messages()
    def set_chatbot_context(self,page_name:str,file_name:str):
        self.__known_facts = {}
        file_name_ref = file_name.lower()
        if file_name_ref.endswith('.pdf') or file_name_ref.endswith('.csv') or file_name_ref.endswith('.txt') or file_name_ref.endswith('.json') or file_name_ref.endswith('.xlsx'):
            self.__known_facts["file_input"] = self.co_fclient.extract_text_from_file(page_name=page_name, file_name=file_name)
            self.__set_messages()
        else:
            print('Only these file extensions are allowed: .pdf,.csv,.txt,.json,.xlsx')
    def __set_messages(self):
        content="Respond only accordingly to the text between '***' and nothing else:"
        content += '\n***' + self.__known_facts["file_input"] + '***\n\n'
        messages = []
        if self.type_of_request != "default":
            messages.append({"role": "system","content": self.__s[self.type_of_request]["content"]})
        messages.append({"role": "system","content": content})
        return messages
    def machine_response(self,inputStr:str)->str:
        if self.model_name == "text-davinci-003":
            messages = self.__set_messages()
            messages.append({"role": "user","content": inputStr})
            prompt = ''
            for i in range(len(messages)):
                prompt += '\n' + messages[i]["content"]
            response = openai.Completion.create(
            model=self.model_name
            ,prompt=prompt
            ,temperature=0.9
            ,max_tokens=150
            ,top_p=1
            ,frequency_penalty=0.0
            ,presence_penalty=0.6
            ,stop=[" Human:", " AI:"]
            )
            self.total_tokens_used += int(response['usage']['total_tokens'])
            answer = dict(response)['choices'][0]['text']
            answer = answer.replace("\n","")
            self.last_answer = answer
        else:
            self.new_machine_response(inputStr = inputStr)
            

    def new_machine_response(self,inputStr:str)->str:
        messages = self.__set_messages()
        messages.append({"role": "user","content": inputStr})
        response = openai.ChatCompletion.create(
        model=self.model_name
        ,messages=messages
        ,temperature=self.__s[self.type_of_request]['temperature']
        ,max_tokens=self.__s[self.type_of_request]['max_tokens']
        ,top_p=self.__s[self.type_of_request]['top_p']
        ,frequency_penalty=self.__s[self.type_of_request]['frequency_penalty']
        ,presence_penalty=self.__s[self.type_of_request]['presence_penalty']
        ,stop=[" Human:", " AI:"]
        )
        
        self.total_tokens_used += int(response['usage']['total_tokens'])
        answer = response['choices'][0]['message']['content']
        self.last_answer = answer
        #return self.last_answer
        #answer = dict(response)['choices'][0]['text']
        #answer = answer.replace("\n","")
        
    def talk_with_machine(self,conversation_input:str=None,language:str=None,output_type:str="speech")->str:
        if conversation_input == None:
            print('Type your question:')
            conversation_input = input()
        self.machine_response(inputStr = conversation_input)
        if output_type == "speech":
            engine = pyttsx3.init()
            engine.setProperty('rate', 190)
            if language != None:
                engine.setProperty('language', language)
                for voice in engine.getProperty('voices'):
                    if language in voice.languages:
                        engine.setProperty('voice', voice.id)
                        break
            engine.setProperty('volume', 1)
            engine.say(self.last_answer)
            engine.runAndWait()

            
        
    def record_my_voice(self,outputName:str="recording0",duration:int=10)->str:
        fileName = outputName.lower().strip().replace('.wav','') + '.wav'
        pre_fileName = 'pre_' + fileName
        freq = 44100
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
        sd.wait()
        write(pre_fileName, freq, recording)
        data, samplerate = soundfile.read(pre_fileName)
        soundfile.write(fileName, data, samplerate, subtype='PCM_16')
        os.remove(pre_fileName)
        return fileName
    
    def transcript_audio_file(self,fileName:str=None)->str:
        r = sr.Recognizer()
        with sr.AudioFile(fileName) as source:
            audio_text = r.listen(source)
            try:
                text = r.recognize_google(audio_text)
                print('Recognizing speach ...')
                return text
            except Exception as e:
                ...
                #print(e)
                    
    def conversation_with_machine(self,input_type:str="text",output_type:str="speech",conversation_input:str=None):
        if self.__known_facts != {} and len(list(self.__known_facts.keys())) > 0:
            if input_type.lower().strip() == "speech":
                fileName = self.record_my_voice(outputName="message_recording",duration=self.duration_in_secs)
                conversation_input = self.transcript_audio_file(fileName)
                self.talk_with_machine(conversation_input=conversation_input,language=self.language,output_type=output_type)
            else:
                self.talk_with_machine(conversation_input=conversation_input,language=self.language,output_type=output_type)
        else:
            self.last_answer = """Chatbot context not set yet. 
            Use cloudpy_org_customizable_chatbot.set_chatbot_context(page_name,file_name) function to set it.""" 
""" 
hint on installing pyaudio on mac:

xcode-select --install
brew remove portaudio
brew install portaudio
pip3 install pyaudio

in ubuntu:
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install ffmpeg libav-tools
python3.8 -m pip install pyaudio
"""