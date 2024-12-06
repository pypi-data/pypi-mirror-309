# User Guide

To get started with WebRTC streams, all that's needed is to import the `WebRTC` component from this package and implement its `stream` event. 

This page will show how to do so with simple code examples.
For complete implementations of common tasks, see the [cookbook](/cookbook).

## Audio Streaming

### Reply on Pause

Typically, you want to run an AI model that generates audio when the user has stopped speaking. This can be done by wrapping a python generator with the `ReplyOnPause` class
and passing it to the `stream` event of the `WebRTC` component.

=== "Code"
    ``` py title="ReplyonPause"
    import gradio as gr
    from gradio_webrtc import WebRTC, ReplyOnPause

    def response(audio: tuple[int, np.ndarray]): # (1)
        """This function must yield audio frames"""
        ...
        for numpy_array in generated_audio:
            yield (sampling_rate, numpy_array, "mono") # (2)


    with gr.Blocks() as demo:
        gr.HTML(
        """
        <h1 style='text-align: center'>
        Chat (Powered by WebRTC ⚡️)
        </h1>
        """
        )
        with gr.Column():
            with gr.Group():
                audio = WebRTC(
                    mode="send-receive", # (3)
                    modality="audio",
                )
            audio.stream(fn=ReplyOnPause(response),
                        inputs=[audio], outputs=[audio], # (4)
                        time_limit=60) # (5)

    demo.launch()
    ```

    1. The python generator will receive the **entire** audio up until the user stopped. It will be a tuple of the form (sampling_rate, numpy array of audio). The array will have a shape of (1, num_samples). You can also pass in additional input components.

    2. The generator must yield audio chunks as a tuple of (sampling_rate, numpy audio array). Each numpy audio array must have a shape of (1, num_samples).

    3. The `mode` and `modality` arguments must be set to `"send-receive"` and `"audio"`.

    4. The `WebRTC` component must be the first input and output component. 

    5. Set a `time_limit` to control how long a conversation will last. If the `concurrency_count` is 1 (default), only one conversation will be handled at a time.
=== "Notes"
    1. The python generator will receive the **entire** audio up until the user stopped. It will be a tuple of the form (sampling_rate, numpy array of audio). The array will have a shape of (1, num_samples). You can also pass in additional input components.

    2. The generator must yield audio chunks as a tuple of (sampling_rate, numpy audio arrays). Each numpy audio array must have a shape of (1, num_samples).

    3. The `mode` and `modality` arguments must be set to `"send-receive"` and `"audio"`.

    4. The `WebRTC` component must be the first input and output component. 

    5. Set a `time_limit` to control how long a conversation will last. If the `concurrency_count` is 1 (default), only one conversation will be handled at a time.

### Stream Handler

`ReplyOnPause` is an implementation of a `StreamHandler`. The `StreamHandler` is a low-level
abstraction that gives you arbitrary control over how the input audio stream and output audio stream are created. The following example echos back the user audio.

=== "Code"
    ``` py title="Stream Handler"
    import gradio as gr
    from gradio_webrtc import WebRTC, StreamHandler
    from queue import Queue

    class EchoHandler(StreamHandler):
        def __init__(self) -> None:
            super().__init__()
            self.queue = Queue()

        def receive(self, frame: tuple[int, np.ndarray]) -> None: # (1)
            self.queue.put(frame)

        def emit(self) -> None: # (2)
            return self.queue.get()
        
        def copy(self) -> StreamHandler:
            return EchoHandler()


    with gr.Blocks() as demo:
        with gr.Column():
            with gr.Group():
                audio = WebRTC(
                    mode="send-receive",
                    modality="audio",
                )

            audio.stream(fn=EchoHandler(),
                         inputs=[audio], outputs=[audio],
                         time_limit=15)

    demo.launch()
    ```

    1. The `StreamHandler` class implements three methods: `receive`, `emit` and `copy`. The `receive` method is called when a new frame is received from the client, and the `emit` method returns the next frame to send to the client. The `copy` method is called at the beginning of the stream to ensure each user has a unique stream handler.
    2. The `emit` method SHOULD NOT block. If a frame is not ready to be sent, the method should return `None`.

=== "Notes"
    1. The `StreamHandler` class implements three methods: `receive`, `emit` and `copy`. The `receive` method is called when a new frame is received from the client, and the `emit` method returns the next frame to send to the client. The `copy` method is called at the beginning of the stream to ensure each user has a unique stream handler.
    2. The `emit` method SHOULD NOT block. If a frame is not ready to be sent, the method should return `None`.

### Server-To-Client Only

To stream only from the server to the client, implement a python generator and pass it to the component's `stream` event. The stream event must also specify a `trigger` corresponding to a UI interaction that starts the stream. In this case, it's a button click.

=== "Code"

    ``` py title="Server-To-CLient"
    import gradio as gr
    from gradio_webrtc import WebRTC
    from pydub import AudioSegment

    def generation(num_steps):
        for _ in range(num_steps):
            segment = AudioSegment.from_file("audio_file.wav")
            array = np.array(segment.get_array_of_samples()).reshape(1, -1)
            yield (segment.frame_rate, array)

    with gr.Blocks() as demo:
        audio = WebRTC(label="Stream", mode="receive",  # (1)
                       modality="audio")
        num_steps = gr.Slider(label="Number of Steps", minimum=1,
                              maximum=10, step=1, value=5)
        button = gr.Button("Generate")

        audio.stream(
            fn=generation, inputs=[num_steps], outputs=[audio],
            trigger=button.click # (2)
        )
    ```
 
    1. Set `mode="receive"` to only receive audio from the server.
    2. The `stream` event must take a `trigger` that corresponds to the gradio event that starts the stream. In this case, it's the button click.
=== "Notes"
    1. Set `mode="receive"` to only receive audio from the server.
    2. The `stream` event must take a `trigger` that corresponds to the gradio event that starts the stream. In this case, it's the button click.

## Video Streaming

### Input/Output Streaming
Set up a video Input/Output stream to continuosly receive webcam frames from the user and run an arbitrary python function to return a modified frame.

=== "Code"
    
    ``` py title="Input/Output Streaming"
    import gradio as gr
    from gradio_webrtc import WebRTC


    def detection(image, conf_threshold=0.3): # (1)
        ... your detection code here ...
        return modified_frame # (2)


    with gr.Blocks() as demo:
        image = WebRTC(label="Stream", mode="send-receive", modality="video") # (3)
        conf_threshold = gr.Slider(
            label="Confidence Threshold",
            minimum=0.0,
            maximum=1.0,
            step=0.05,
            value=0.30,
        )
        image.stream(
            fn=detection,
            inputs=[image, conf_threshold], # (4)
            outputs=[image], time_limit=10
        )

    if __name__ == "__main__":
        demo.launch()
    ```

    1. The webcam frame will be represented as a numpy array of shape (height, width, RGB).
    2. The function must return a numpy array. It can take arbitrary values from other components.
    3. Set the `modality="video"` and `mode="send-receive"`
    4. The `inputs` parameter should be a list where the first element is the WebRTC component. The only output allowed is the WebRTC component.
=== "Notes"
    1. The webcam frame will be represented as a numpy array of shape (height, width, RGB).
    2. The function must return a numpy array. It can take arbitrary values from other components.
    3. Set the `modality="video"` and `mode="send-receive"`
    4. The `inputs` parameter should be a list where the first element is the WebRTC component. The only output allowed is the WebRTC component.

### Server-to-Client Only

Set up a server-to-client stream to stream video from an arbitrary user interaction.

=== "Code"
    ``` py title="Server-To-Client"
        import gradio as gr
        from gradio_webrtc import WebRTC
        import cv2

        def generation():
            url = "https://download.tsi.telecom-paristech.fr/gpac/dataset/dash/uhd/mux_sources/hevcds_720p30_2M.mp4"
            cap = cv2.VideoCapture(url)
            iterating = True
            while iterating:
                iterating, frame = cap.read()
                yield frame # (1)

        with gr.Blocks() as demo:
            output_video = WebRTC(label="Video Stream", mode="receive", # (2)
                                  modality="video")
            button = gr.Button("Start", variant="primary")
            output_video.stream(
                fn=generation, inputs=None, outputs=[output_video],
                trigger=button.click # (3)
            )
            demo.launch()
    ```

    1. The `stream` event's `fn` parameter is a generator function that yields the next frame from the video as a **numpy array**.
    2. Set `mode="receive"` to only receive audio from the server.
    3. The `trigger` parameter the gradio event that will trigger the stream. In this case, the button click event.
=== "Notes"
    1. The `stream` event's `fn` parameter is a generator function that yields the next frame from the video as a **numpy array**.
    2. Set `mode="receive"` to only receive audio from the server.
    3. The `trigger` parameter the gradio event that will trigger the stream. In this case, the button click event.


## Additional Outputs

In order to modify other components from within the WebRTC stream, you must yield an instance of `AdditionalOutputs` and add an `on_additional_outputs` event to the `WebRTC` component.

This is common for displaying a multimodal text/audio conversation in a Chatbot UI.

=== "Code"

    ``` py title="Additional Outputs"
    from gradio_webrtc import AdditionalOutputs, WebRTC

    def transcribe(audio: tuple[int, np.ndarray],
                   transformers_convo: list[dict],
                   gradio_convo: list[dict]):
    ... generate text response ...
    response = model.generate(**inputs, max_length=256)
    transformers_convo.append({"role": "assistant", "content": response})
    gradio_convo.append({"role": "assistant", "content": response})
    yield AdditionalOutputs(transformers_convo, gradio_convo) # (1)


    with gr.Blocks() as demo:
        gr.HTML(
        """
        <h1 style='text-align: center'>
        Talk to Qwen2Audio (Powered by WebRTC ⚡️)
        </h1>
        """
        )
        transformers_convo = gr.State(value=[])
        with gr.Row():
            with gr.Column():
                audio = WebRTC(
                    label="Stream",
                    mode="send", # (2)
                    modality="audio",
                )
            with gr.Column():
                transcript = gr.Chatbot(label="transcript", type="messages")

        audio.stream(ReplyOnPause(transcribe),
                    inputs=[audio, transformers_convo, transcript],
                    outputs=[audio], time_limit=90)
        audio.on_additional_outputs(lambda s,a: (s,a), # (3)
                                    outputs=[transformers_convo, transcript],
                                    queue=False, show_progress="hidden")
        demo.launch()
    ```
    
    1. Pass your data to `AdditionalOutputs` and yield it.
    2. In this case, no audio is being returned, so we set `mode="send"`. However, if we set `mode="send-receive"`, we could also yield generated audio and `AdditionalOutputs`.
    3. The `on_additional_outputs` event does not take `inputs`. It's common practice to not run this event on the queue since it is just a quick UI update.
=== "Notes"
    1. Pass your data to `AdditionalOutputs` and yield it.
    2. In this case, no audio is being returned, so we set `mode="send"`. However, if we set `mode="send-receive"`, we could also yield generated audio and `AdditionalOutputs`.
    3. The `on_additional_outputs` event does not take `inputs`. It's common practice to not run this event on the queue since it is just a quick UI update.