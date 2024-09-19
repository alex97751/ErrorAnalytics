from gradio_client import Client

client = Client("https://llm2-compute.cms.hu-berlin.de/")

def main():
    while True:
        user_input = input("Enter your question (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        result = client.predict(user_input, api_name="/chat")
        print("Response:", result)

if __name__ == "__main__":
    main()