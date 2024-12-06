import gradio as gr
from gradio_webrtc import WebRTC, AdditionalOutputs, ReplyOnPause
from pydub import AudioSegment
from io import BytesIO
import numpy as np
import librosa
import tempfile
from twilio.rest import Client
import os
#import spaces
import uuid
# from transformers import Qwen2AudioForConditionalGeneration, AutoProcessor
import logging

# Configure the root logger to WARNING to suppress debug messages from other libraries
logging.basicConfig(level=logging.WARNING)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Configure the logger for your specific library
logger = logging.getLogger("gradio_webrtc")
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)


# processor = AutoProcessor.from_pretrained("Qwen/Qwen2-Audio-7B-Instruct")
# model = Qwen2AudioForConditionalGeneration.from_pretrained("Qwen/Qwen2-Audio-7B-Instruct", device_map="auto")

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

if account_sid and auth_token:
    client = Client(account_sid, auth_token)

    token = client.tokens.create()

    rtc_configuration = {
        "iceServers": token.ice_servers,
        "iceTransportPolicy": "relay",
    }
else:
    rtc_configuration = None



def yield_audio(audio: tuple[int, np.ndarray]):
    yield AdditionalOutputs(audio)



#@spaces.GPU
def respond(transformers_convo: list[dict], gradio_convo: list[dict], audio: tuple[int, np.ndarray], ):
    segment = AudioSegment(audio[1].tobytes(), frame_rate=audio[0], sample_width=audio[1].dtype.itemsize, channels=1)

    name = str(uuid.uuid4()) + ".mp3"
    segment.export(name, format="mp3")
    transformers_convo.append({"role": "user", "content": [{"type": "audio", "audio_url": name}]})
    gradio_convo.append({"role": "assistant", "content": gr.Audio(value=name)})
    text = processor.apply_chat_template(transformers_convo, add_generation_prompt=True, tokenize=False)
    audios = []
    for message in transformers_convo:
        if isinstance(message["content"], list):
            for ele in message["content"]:
                if ele["type"] == "audio":
                    audios.append(librosa.load(
                        BytesIO(open(ele['audio_url'], "rb").read()), 
                        sr=processor.feature_extractor.sampling_rate)[0]
                    )
    inputs = processor(text=text, audios=audios, return_tensors="pt", padding=True)
    inputs = dict(**inputs)
    inputs["input_ids"] = inputs["input_ids"].to("cuda:0")

    generate_ids = model.generate(**inputs, max_length=256)
    generate_ids = generate_ids[:, inputs["input_ids"].size(1):]
    response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    transformers_convo.append({"role": "assistant", "content": response})
    gradio_convo.append({"role": "assistant", "content": response})

    yield transformers_convo, gradio_convo


with gr.Blocks() as demo:
    gr.HTML(
    """
    <h1 style='text-align: center'>
    Talk to Qwen2Audio (Powered by WebRTC ⚡️)
    </h1>
    <p style='text-align: center'>
    Once you grant access to your microphone, you can talk naturally to Qwen2Audio.
    When you stop talking, the audio will be sent for processing.
    </p>
    <p style='text-align: center'>
    There will be some delay in responding due to acquiring the ZeroGPU resources.
    </p>
    <p style='text-align: center'>
    Each conversation is limited to 90 seconds. Once the time limit is up you can rejoin the conversation.
    </p>
    """
    )
    transformers_convo = gr.State(value=[])
    with gr.Row():
        with gr.Column():
            audio = WebRTC(
                rtc_configuration=rtc_configuration,
                label="Stream",
                mode="send",
                modality="audio",
            )
        with gr.Column():
            transcript = gr.Chatbot(label="transcript", type="messages")

    audio.stream(ReplyOnPause(yield_audio), inputs=[audio], outputs=[audio])
    audio.on_additional_outputs(respond, outputs=[transformers_convo, transcript])

if __name__ == "__main__":
    demo.launch()