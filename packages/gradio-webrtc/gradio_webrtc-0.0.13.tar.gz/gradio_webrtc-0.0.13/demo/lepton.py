import gradio as gr
from gradio_webrtc import WebRTC, ReplyOnPause, AdditionalOutputs
import numpy as np
import io
from pydub import AudioSegment
import openai
import time
import base64
import os

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

if account_sid and auth_token:
    from twilio.rest import Client
    client = Client(account_sid, auth_token)

    token = client.tokens.create()

    rtc_configuration = {
        "iceServers": token.ice_servers,
        "iceTransportPolicy": "relay",
    }
else:
    rtc_configuration = None



def update_or_append_conversation(conversation, id, role, content):
    # Find if there's an existing message with the given id
    for message in conversation:
        if message.get("id") == id and message.get("role") == role:
            message["content"] = content
            return
    # If not found, append a new message
    conversation.append({"id": id, "role": role, "content": content})


def generate_response_and_audio(audio_bytes: bytes, lepton_conversation: list[dict],
                                client: openai.OpenAI):
    if client is None:
        raise gr.Error("Please enter a valid API key first.")

    # mp3 bitrate
    bitrate = 128 
    audio_data = base64.b64encode(audio_bytes).decode()

    try:
        stream = client.chat.completions.create(
            extra_body={
                "require_audio": True,
                "tts_preset_id": "jessica",
                "tts_audio_format": "mp3",
                "tts_audio_bitrate": bitrate
            },
            model="llama3.1-8b",
            messages=lepton_conversation + [{"role": "user", "content": [{"type": "audio", "data": audio_data}]}],
            temperature=0.7,
            max_tokens=256,
            stream=True,
        )

        id = str(time.time())
        full_response = ""
        asr_result = ""
        all_audio = b""

        for i, chunk in enumerate(stream):
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            content = delta.content
            audio = getattr(chunk.choices[0], "audio", [])
            asr_results = getattr(chunk.choices[0], "asr_results", [])

            if asr_results:
                print(i, "asr_results")
                asr_result += "".join(asr_results)
                yield id, None, asr_result, None

            if content:
                print(i, "content")
                full_response += content
                yield id, full_response, None, None

            if audio:
                print(i, "audio")
                # Accumulate audio bytes and yield them
                audio_bytes_accumulated = b''.join([base64.b64decode(a) for a in audio])
                all_audio += audio_bytes_accumulated
                audio = AudioSegment.from_file(io.BytesIO(audio_bytes_accumulated), format="mp3")
                audio_array = np.array(audio.get_array_of_samples(), dtype=np.int16).reshape(1, -1)
                print("audio.frame_rate", audio.frame_rate)

                yield id, None, None, (audio.frame_rate, audio_array)
        
        if all_audio:
            all_audio = AudioSegment.from_file(io.BytesIO(all_audio), format="mp3")
            all_audio.export("all_audio.mp3", format="mp3")

        yield id, full_response, asr_result, None
        print("finishing loop")
    except Exception as e:
        raise gr.Error(f"Error during audio streaming: {e}")

def response(audio: tuple[int, np.ndarray], lepton_conversation: list[dict],
             gradio_conversation: list[dict], client: openai.OpenAI):
    
    audio_buffer = io.BytesIO()
    segment = AudioSegment(
        audio[1].tobytes(),
        frame_rate=audio[0],
        sample_width=audio[1].dtype.itemsize,
        channels=1,
    )
    segment.export(audio_buffer, format="mp3")

    generator = generate_response_and_audio(audio_buffer.getvalue(), lepton_conversation, client)

    for id, text, asr, audio in generator:
        if asr:
            update_or_append_conversation(lepton_conversation, id, "user", asr)
            update_or_append_conversation(gradio_conversation, id, "user", asr)
            yield AdditionalOutputs(lepton_conversation, gradio_conversation)
        if text:
            update_or_append_conversation(lepton_conversation, id, "assistant", text)
            update_or_append_conversation(gradio_conversation, id, "assistant", text)
            yield AdditionalOutputs(lepton_conversation, gradio_conversation)
        if audio:
            yield audio
        else:
            yield AdditionalOutputs(lepton_conversation, gradio_conversation)


def set_api_key(lepton_api_key):
    try:
       client = openai.OpenAI(
        base_url="https://llama3-1-8b.lepton.run/api/v1/",
        api_key=lepton_api_key
    )
    except:
        raise gr.Error("Invalid API keys. Please try again.")
    gr.Info("Successfully set API keys.", duration=3)
    return client, gr.update(visible=True), gr.update(visible=False)


with gr.Blocks() as demo:
    with gr.Group():
        with gr.Row():
            chatbot = gr.Chatbot(label="Conversation", type="messages")
        with gr.Row(visible=False) as mic_row:
            audio = WebRTC(modality="audio", mode="send-receive",
                                label="Audio Stream",
                                rtc_configuration=rtc_configuration)
        with gr.Row(equal_height=True) as api_row:
            api_key_input = gr.Textbox(type="password", value=os.getenv("LEPTONAI_API_KEY"),
                                                label="Enter Your Lepton AI Key")
           

    client_state = gr.State(None)
    lepton_conversation = gr.State([{"role": "system",
                                     "content": "You are a knowledgeable assistant who will engage in spoken conversations with users. "
                                     "Keep your answers short and natural as they will be read aloud."}])

    api_key_input.submit(set_api_key, inputs=[api_key_input],
                         outputs=[client_state, mic_row, api_row])
    audio.stream(
        ReplyOnPause(response, output_sample_rate=44100, output_frame_size=882),
        inputs=[audio, lepton_conversation, chatbot, client_state],
        outputs=[audio]
    )
    audio.on_additional_outputs(lambda l, g: (l, g), outputs=[lepton_conversation, chatbot],
                                queue=False, show_progress="hidden")

    demo.launch()