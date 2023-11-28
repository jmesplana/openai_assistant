
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
    name="SAFe Specialist",
    instructions="As a Scaled Agile Framework (SAFe) Specialist, you guide organizations from a siloed project model \
        to an integrated product mode, focusing on humanitarian organizations offering digital solutions. You understand \
            their unique context by asking about current practices and challenges, using direct questions and multiple-choice \
                options. You tailor responses for a smooth transition, emphasizing core SAFe principles and addressing challenges \
                    like cultural resistance and highlighting best practices. You communicate with a balance of honesty and \
                        encouragement, providing realistic yet optimistic guidance. You avoid giving advice on areas outside \
                            the scope of SAFe, like financial management or legal compliance. Additionally, you recognize that \
                                SAFe may not suit all organizations, especially those with rigid structures or those not ready for\
                                      significant cultural changes. In such cases, you guide users towards understanding the \
                                        limitations of SAFe in their specific context. Walk the user through the step by step process \
                                            and ask clarifying questions one at a time and wait for an answer before responding. Then \
                                                formulate your response.",
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
        instructions="The user is a humanitarian worker who is going through digital transformation"
    )

    while True:
        # Wait for 5 seconds
        time.sleep(0.5)

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
            
            data = messages.data
            first_thread_message = data[0]
            content = first_thread_message.content
            response = content[0].text.value
            return response
        else:
            continue

# Create a Gradio Interface

iface = gr.ChatInterface(main, title="SAFe Specialist",\
                          description="SAFe Specialist guiding transitions with realistic and \
                            optimistic advice towards a product centric approach",\
                                examples=["How can I shift from project to product mode?",\
                                          "What are the key SAFe principles for my organization?",\
                                            "Can you provide options for agile practices in my setting?",\
                                                "How do I deal with cultural resistance in SAFe adoption?", \
                                                    "What's your advice for an org with many different digital solutions?",\
                                                        "Could you walk me through the step-by-step process of moving into SAFe?"]).queue()

if __name__ == "__main__":
    iface.launch()
