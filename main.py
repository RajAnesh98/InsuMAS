# import gradio as gr
# import os
# from PIL import Image
# from agent import supervisor_prebuilt
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# import uuid
# import chromadb
# import pandas as pd



# thread_id = uuid.uuid4()
# config = {"configurable": {"thread_id": thread_id}}
# # --- Functions ---

# # def user_submit(message, image, audio, history):
# #     """Handle user input (text, audio, image)."""
# #     user_message = ""

# #     if image:
# #         try:
# #             image_uploaded = Image.open(image)  # just to validate
# #             user_message = "[Image Uploaded]" + (" " + message if message else "")
# #             print(image_uploaded)
# #         except Exception as e:
# #             user_message = f"[Image error: {e}]"
# #     elif message:
# #         user_message = message

# #     if not user_message:
# #         return "", None, None, history, None, gr.update(visible=False)

# #     history.append((user_message, None))

# #     # Show user message, and that bot is thinking
# #     yield "", None, None, history, None, gr.update(visible=False)

# #     result = supervisor_prebuilt.invoke({"messages": [HumanMessage(content=user_message)]}, config=config)

# #     bot_responses = []
# #     for msg in result["messages"]:
# #         if isinstance(msg, AIMessage):
# #             bot_responses.append(msg.content)

# #     bot_response = "\n".join(bot_responses)
# #     history[-1] = (user_message, bot_response)

# #     # Clear inputs and hide image preview
# #     yield "", None, None, history, None, gr.update(visible=False)

# # def user_submit(message, image, audio, history):
# #     """Handle user input and correctly parse the supervisor stream."""
# #     user_message = ""
# #     if image:
# #         try:
# #             Image.open(image)
# #             user_message = "[Image Uploaded]" + (" " + message if message else "")
# #         except Exception as e:
# #             user_message = f"[Image error: {e}]"
# #     elif message:
# #         user_message = message

# #     if not user_message:
# #         return "", None, None, history, None, gr.update(visible=False)

# #     history.append((user_message, ""))
# #     yield "", None, None, history, None, gr.update(visible=False)

# #     full_response = ""
    
# #     # --- Corrected Streaming Logic ---
# #     try:
# #         # The stream yields a dictionary for each step, with the node name as the key
# #         for chunk in supervisor_prebuilt.stream({"messages": [HumanMessage(content=user_message)]}, config=config):
            
# #             # Use this line to see the raw output from your agent in the terminal
# #             # print(f"--- STREAM CHUNK ---\n{chunk}\n")
            
# #             # Iterate through the dictionary's items (node_name, node_output)
# #             for node_name, node_output in chunk.items():
# #                 # Check if the node's output contains the 'messages' we want
# #                 if "messages" in node_output:
# #                     for msg in node_output["messages"]:
# #                         if isinstance(msg, AIMessage) and msg.content:
# #                             # Append the new content to our full response
# #                             full_response += msg.content
# #                             # Update the last message in history
# #                             history[-1] = (user_message, full_response)
# #                             # Yield the updated UI
# #                             yield "", None, None, history, None, gr.update(visible=False)
# #     except Exception as e:
# #         # Catch and display any errors from the agent
# #         print(f"An error occurred in the agent stream: {e}")
# #         history[-1] = (user_message, f"Sorry, an error occurred: {e}")
# #         yield "", None, None, history, None, gr.update(visible=False)


# #     # Final yield to clear inputs
# #     yield "", None, None, history, None, gr.update(visible=False)


# def user_submit(message, image, audio, history):
#     """Handle user input and correctly parse the supervisor stream - FINAL OUTPUT ONLY."""
#     user_message = ""
#     if image:
#         try:
#             Image.open(image)
#             user_message = "[Image Uploaded]" + (" " + message if message else "")
#         except Exception as e:
#             user_message = f"[Image error: {e}]"
#     elif message:
#         user_message = message

#     if not user_message:
#         return "", None, None, history, None, gr.update(visible=False)

#     history.append((user_message, "Thinking..."))
#     yield "", None, None, history, None, gr.update(visible=False)

#     final_response = ""
    
#     try:
#         # Collect all messages but only display the final one
#         all_messages = []
#         for chunk in supervisor_prebuilt.stream({"messages": [HumanMessage(content=user_message)]}, config=config):
#             for node_name, node_output in chunk.items():
#                 if "messages" in node_output:
#                     for msg in node_output["messages"]:
#                         if isinstance(msg, AIMessage) and msg.content:
#                             all_messages.append(msg.content)
        
#         # Use only the last message as the final response
#         if all_messages:
#             final_response = all_messages[-1]  # Take only the last message
#             history[-1] = (user_message, final_response)
#         else:
#             history[-1] = (user_message, "No response generated.")
            
#     except Exception as e:
#         print(f"An error occurred in the agent stream: {e}")
#         history[-1] = (user_message, f"Sorry, an error occurred: {e}")
    
#     # Final yield with the complete response
#     yield "", None, None, history, None, gr.update(visible=False)


# def reset_chat():
#     """Reset the chat state."""
#     global thread_id, config
#     thread_id = uuid.uuid4()
#     config = {"configurable": {"thread_id": thread_id}}
#     return [], "", None, None, gr.update(visible=False)


# def update_image_preview(file):
#     return gr.update(value=file, visible=bool(file))


# # --- Gradio UI ---
# with gr.Blocks() as demo:
#     with gr.Row():
#         new_chat_btn = gr.Button("🆕 New Chat", scale=1)

#     with gr.Row():
#         chatbot = gr.Chatbot(scale=1)  # tuple mode

#     with gr.Row():
#         msg = gr.Textbox(placeholder="Type something...", scale=6)
#         send_btn = gr.Button("Send", scale=1)
#         img_btn = gr.UploadButton("📷 Upload", file_types=["image"], type="filepath", scale=1)
#         audio_recorder = gr.Audio(
#             sources=["microphone"],
#             type="filepath",
#             format="wav",
#             label="🎤 Record Audio",
#         )
#         img_preview = gr.Image(label="Uploaded Image", type="filepath", interactive=False, visible=False, scale=3)

#     # Bind actions
#     send_btn.click(
#         user_submit,
#         inputs=[msg, img_btn, audio_recorder, chatbot],
#         outputs=[msg, img_btn, audio_recorder, chatbot, img_btn, img_preview],
#     )

#     msg.submit(
#         user_submit,
#         inputs=[msg, img_btn, audio_recorder, chatbot],
#         outputs=[msg, img_btn, audio_recorder, chatbot, img_btn, img_preview],
#     )

#     new_chat_btn.click(
#         reset_chat,
#         inputs=None,
#         outputs=[chatbot, msg, img_btn, audio_recorder, img_preview],
#     )

#     img_btn.upload(
#         update_image_preview,
#         inputs=[img_btn],
#         outputs=[img_preview],
#     )

# demo.launch()




























import gradio as gr
import os
from PIL import Image
from Supervisor_Agent import supervisor_prebuilt
from utils import HumanMessage, AIMessage, SystemMessage, uuid, chromadb, pd, json, io
#from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import uuid
import chromadb
import pandas as pd
import base64
import json
import io

thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": thread_id}}

# Store the current image path in a global variable or session state
current_image_path = None

def encode_image_to_base64(image_path):
    """Convert image to base64 string for sending to agents."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def resize_image(image_path, max_size=(800, 800)):
    """Resize image while maintaining aspect ratio."""
    with Image.open(image_path) as img:
        # Convert to RGB if needed
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        
        # Calculate new size maintaining aspect ratio
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save to a bytes buffer
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85, optimize=True)
        return buffer.getvalue()

def create_message_with_image(text_content, image_path):
    """
    Create a message that includes both text and image information with compression.
    """
    try:
        # Resize and compress the image
        image_data = resize_image(image_path)
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Create a simpler message format
        message_content = f"{text_content if text_content else 'Please analyze this image'}\n[Attached Image: {os.path.basename(image_path)}]"
        
        return message_content
    except Exception as e:
        print(f"Error processing image: {e}")
        return text_content

def user_submit(message, image, audio, history):
    """Handle user input including images for agent processing."""
    if not message and not image:
        return "", None, None, history, None, gr.update(visible=False)

    try:
        if image:
            # Process image upload
            try:
                img = Image.open(image)
                img.verify()  # Verify it's a valid image
                
                # For chatbot display, we send a list for images
                display_message = (None, image) if not message else (message, image)
                agent_message = create_message_with_image(
                    message if message else "Please analyze this image",
                    image
                )
            except Exception as e:
                print(f"Image error: {e}")
                history.append((f"❌ Error processing image: {e}", None))
                yield "", None, None, history, None, gr.update(visible=False)
                return
        else:
            # Text-only message
            display_message = message
            agent_message = message

        # Add message to history and show "thinking" state
        history.append((display_message, "🤔 Thinking..."))
        yield "", None, None, history, None, gr.update(visible=bool(image))

        # Process through the agent
        result = supervisor_prebuilt.invoke(
            {"messages": [HumanMessage(content=agent_message)]},
            config=config
        )

        # Process bot response
        bot_responses = []
        for msg in result["messages"]:
            if isinstance(msg, AIMessage):
                bot_responses.append(msg.content)

        # Update history with the complete response
        if bot_responses:
            bot_response = "\n".join(bot_responses)
            history[-1] = (display_message, bot_response)
        else:
            history[-1] = (display_message, "No response generated.")

    except Exception as e:
        print(f"Error in processing: {e}")
        history[-1] = (
            display_message if 'display_message' in locals() else message or "[Image]",
            f"Sorry, an error occurred: {str(e)}"
        )

    # Final yield with cleared inputs
    yield "", None, None, history, None, gr.update(visible=False)

def reset_chat():
    """Reset the chat state."""
    global thread_id, config, current_image_path
    thread_id = uuid.uuid4()
    config = {"configurable": {"thread_id": thread_id}}
    current_image_path = None
    return [], "", None, None, gr.update(visible=False)

def update_image_preview(file):
    """Update the image preview when a file is uploaded."""
    if file:
        try:
            # Validate it's a valid image
            img = Image.open(file)
            img.verify()
            return gr.update(value=file, visible=True)
        except Exception as e:
            print(f"Invalid image file: {e}")
            return gr.update(value=None, visible=False)
    return gr.update(value=None, visible=False)

# --- Gradio UI ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏥 Insurance & Healthcare Assistant")
    gr.Markdown("Upload images for medical specialty recommendations, ask about insurance, or get help finding doctors.")
    
    with gr.Row():
        new_chat_btn = gr.Button("🆕 New Chat", scale=1, variant="secondary")

    with gr.Row():
        chatbot = gr.Chatbot(
            scale=1,
            height=500,
            show_label=False,
            avatar_images=(None, "🤖")
        )

    with gr.Row():
        with gr.Column(scale=8):
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Type your message here... (You can also upload an image for medical condition analysis)",
                    scale=6,
                    show_label=False,
                    container=False
                )
                send_btn = gr.Button("📤 Send", scale=1, variant="primary")
            
            with gr.Row():
                img_btn = gr.UploadButton(
                    "📷 Upload Image",
                    file_types=["image"],
                    type="filepath",
                    scale=1,
                    variant="secondary"
                )
                audio_recorder = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    format="wav",
                    label="🎤 Record Audio",
                    scale=2
                )
        
        with gr.Column(scale=2):
            img_preview = gr.Image(
                label="📸 Uploaded Image",
                type="filepath",
                interactive=False,
                visible=False
            )
            gr.Markdown(
                """
                ### Tips:
                - Upload medical images for specialty recommendations
                - Provide your county and state for doctor searches
                - Ask about insurance coverage and costs
                """,
                visible=True
            )

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

    # Add examples
    gr.Examples(
        examples=[
            ["I have a weird rash on my arm", None],
            ["What's covered under a Silver PPO plan?", None],
            ["Find me a cardiologist in Miami-Dade County, Florida", None],
            ["Calculate my costs for a $50,000 surgery", None],
        ],
        inputs=[msg, img_btn],
        label="Example Queries"
    )

demo.launch()