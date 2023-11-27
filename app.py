
import time
import config
import gradio as gr

from openai import OpenAI

client = OpenAI(api_key=config.OPENAI_API_KEY)

# Initialize the client
# Set your OpenAI API key

'''file = client.files.create(
    file=open("songs.txt", "rb"),
    purpose='assistants'
)'''

# Step 1: Create an Assistant
assistant = client.beta.assistants.create(
    name="Customer Service Assistant",
    instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
    model="gpt-4-1106-preview",
  #  file_ids=[file.id],
    tools=[{"type": "retrieval"}]
)

# Step 2: Create a Thread
thread = client.beta.threads.create()

def main(query, history):
    # Step 3: Add a Message to a Thread
    history=history,
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=query
    )

    # Step 4: Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as John"
    )

    while True:
        # Wait for 5 seconds
        time.sleep(5)

        # Retrieve the run status
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        # If run is completed, get messages
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            response = ""
            # Loop through messages and print content based on role
            for msg in messages.data:
                role = msg.role
                content = msg.content[0].text.value
                response += f"{role.capitalize()}: {content}\n\n"
            return response+"\n\n"
        else:
            continue

# Create a Gradio Interface

iface = gr.ChatInterface(main, title="Chatbot").queue()
if __name__ == "__main__":
    iface.launch()