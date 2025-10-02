import gradio as gr
import os
from PIL import Image
from Supervisor_Agent import supervisor_prebuilt
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import uuid
import chromadb
import pandas as pd



thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": thread_id}}

def user_submit(message, image, audio, history):
    """Handle user input and correctly parse the supervisor stream - FINAL OUTPUT ONLY."""
    user_message = ""
    if image:
        try:
            Image.open(image)
            user_message = "[Image Uploaded]" + (" " + message if message else "")
        except Exception as e:
            user_message = f"[Image error: {e}]"
    elif message:
        user_message = message

    if not user_message:
        return "", None, None, history, None, gr.update(visible=False)

    history.append((user_message, "Thinking..."))
    yield "", None, None, history, None, gr.update(visible=False)

    final_response = ""
    
    try:
        # Collect all messages but only display the final one
        all_messages = []
        for chunk in supervisor_prebuilt.stream({"messages": [HumanMessage(content=user_message)]}, config=config):
            for node_name, node_output in chunk.items():
                if "messages" in node_output:
                    for msg in node_output["messages"]:
                        if isinstance(msg, AIMessage) and msg.content:
                            all_messages.append(msg.content)
        
        # Use only the last message as the final response
        if all_messages:
            final_response = all_messages[-1]  # Take only the last message
            history[-1] = (user_message, final_response)
        else:
            history[-1] = (user_message, "No response generated.")
            
    except Exception as e:
        print(f"An error occurred in the agent stream: {e}")
        history[-1] = (user_message, f"Sorry, an error occurred: {e}")
    
    # Final yield with the complete response
    yield "", None, None, history, None, gr.update(visible=False)


def reset_chat():
    """Reset the chat state."""
    global thread_id, config
    thread_id = uuid.uuid4()
    config = {"configurable": {"thread_id": thread_id}}
    return [], "", None, None, gr.update(visible=False)


def update_image_preview(file):
    return gr.update(value=file, visible=bool(file))


# --- Gradio UI ---
with gr.Blocks() as demo:
    with gr.Row():
        new_chat_btn = gr.Button("🆕 New Chat", scale=1)

    with gr.Row():
        chatbot = gr.Chatbot(
            scale=1,
            # REMOVED type="messages" - using default tuple format
            height=500,
            show_label=False,
            avatar_images=("👤", "🤖")
        )

    with gr.Row():
        msg = gr.Textbox(placeholder="Type something...", scale=6)
        send_btn = gr.Button("Send", scale=1)
        img_btn = gr.UploadButton("📷 Upload", file_types=["image"], type="filepath", scale=1)
        audio_recorder = gr.Audio(
            sources=["microphone"],
            type="filepath",
            format="wav",
            label="🎤 Record Audio",
        )
        img_preview = gr.Image(label="Uploaded Image", type="filepath", interactive=False, visible=False, scale=3)

    # Bind actions
    send_btn.click(
        user_submit,
        inputs=[msg, img_btn, audio_recorder, chatbot],
        outputs=[msg, img_btn, audio_recorder, chatbot, img_btn, img_preview],
    )

    msg.submit(
        user_submit,
        inputs=[msg, img_btn, audio_recorder, chatbot],
        outputs=[msg, img_btn, audio_recorder, chatbot, img_btn, img_preview],
    )

    new_chat_btn.click(
        reset_chat,
        inputs=None,
        outputs=[chatbot, msg, img_btn, audio_recorder, img_preview],
    )

    img_btn.upload(
        update_image_preview,
        inputs=[img_btn],
        outputs=[img_preview],
    )

demo.launch()