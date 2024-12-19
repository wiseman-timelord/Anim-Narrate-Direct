# ./scripts/interface.py

import gradio as gr

def create_interface(
    available_models,
    default_model,
    initial_audio_status,
    settings,
    threads_slider_initial_visible,
    handle_generate_and_play,
    handle_save_audio,
    handle_restart_session,
    exit_program,
    handle_update_settings
):
    with gr.Blocks(title="Gen-Gradio-Voice") as demo:
        with gr.Tab("Narrate"):
            gr.Markdown("### Narration Interface")
            gr.Textbox(
                value=default_model,  # Replace with settings["voice_model"] if dynamic
                label="Current Model",
                interactive=False  # This makes it non-editable
            )
            audio_status = gr.Textbox(label="Audio Status", value=initial_audio_status, interactive=False)
            text_input = gr.Textbox(label="Enter Text", lines=10)
            
            with gr.Row():
                generate_button = gr.Button("Generate And Play")
                save_button = gr.Button("Save Audio")
            with gr.Row():
                restart_button = gr.Button("Restart Session")
                exit_button = gr.Button("Exit Program")

            generate_button.click(
                fn=handle_generate_and_play,
                inputs=[text_input],
                outputs=audio_status
            )

            save_button.click(
                fn=handle_save_audio,
                inputs=None,
                outputs=audio_status
            )

        with gr.Tab("Configure"):
            gr.Markdown("### Configuration Options")
            model_selector = gr.Dropdown(
                label="Select TTS Model",
                choices=available_models,
                value=default_model
            )
            speed_slider = gr.Slider(
                label="Speed",
                minimum=0.5,
                maximum=2.0,
                step=0.1,
                value=settings["speed"]
            )
            pitch_slider = gr.Slider(
                label="Pitch",
                minimum=0.5,
                maximum=2.0,
                step=0.1,
                value=settings["pitch"]
            )
            volume_gain_slider = gr.Slider(
                label="Volume Gain (dB)",
                minimum=-20.0,
                maximum=20.0,
                step=1.0,
                value=settings["volume_gain"]
            )
            threads_percent_slider = gr.Slider(
                label="Threads Percent (%)",
                minimum=10,
                maximum=100,
                step=10,
                value=settings["threads_percent"],
                visible=threads_slider_initial_visible
            )
            save_format_dropdown = gr.Dropdown(
                label="Preferred Save Format",
                choices=["mp3", "wav"],
                value=settings["save_format"]
            )
            update_status = gr.Textbox(
                label="Update Status",
                interactive=False
            )
            update_button = gr.Button("Update Settings")
            update_button.click(
                fn=handle_update_settings,
                inputs=[model_selector, speed_slider, pitch_slider, volume_gain_slider, threads_percent_slider, save_format_dropdown],
                outputs=[update_status]
            )

        # Bind restart after threads_percent_slider is defined
        restart_button.click(
            fn=handle_restart_session,
            inputs=None,
            outputs=[audio_status, threads_percent_slider]
        )

        exit_button.click(
            fn=lambda: exit_program(),  # Wrap the exit_program function
            inputs=None,
            outputs=None
        )

    return demo
