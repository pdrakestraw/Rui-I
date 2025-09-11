from piper import PiperVoice, SynthesisConfig
import pyaudio
from openai import OpenAI
from dotenv import load_dotenv
import os

p = pyaudio.PyAudio()

#Loading and configuring Piper voice, 
voice = PiperVoice.load("voices/en_GB-northern_english_male-medium.onnx")
syn_config = SynthesisConfig(
    volume=0.5,
    length_scale=1.25,
    noise_scale=1.0,
    noise_w_scale=1,
    normalize_audio=False, 
)

# Loading the API Key, use your own API key here. See ReadMe for instructions
load_dotenv()
assistant = OpenAI(api_key=os.getenv("MY_API_KEY"))

# Initializing pyaudio, this is what plays the audio from computer without saving to file
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=22050, 
    output=True
)

# Start of the loop
text = ""
while(text != "exit"):
    text = input("Text: ")
    
    if text.lower() == "exit":
        break
    response = assistant.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Respond to the prompt as a help assistant, assisting in technical problems. Limit your response to 2 sentences. "},
            {"role": "user", "content": text}
        ],
        n=1
    )
    message = response.choices[0].message.content.strip()

    # In the terminal, it'll display the amount of tokens used for each response
    print("Tokens Used: ", response.usage.total_tokens)

    # 
    for chunk in voice.synthesize(message, syn_config):
        if chunk.audio_int16_bytes:
            stream.write(chunk.audio_int16_bytes)
        
stream.stop_stream
stream.close()
p.terminate()

