# LangChain and Temporal Integration

This project leverages the combined strengths of LangChain and Temporal to create powerful, scalable language processing applications. LangChain provides advanced capabilities for building language model applications, such as chatbots or translation services, using state-of-the-art AI. Temporal complements this by offering robust workflow orchestration, ensuring these applications are not only intelligent but also reliable and maintainable. This integration is ideal for developers seeking to deploy complex language-driven workflows with ease, efficiency, and resilience.

## Setup

To set up the project, you need to install the required tools and dependencies. Follow these steps to get started:

### Installing Dependencies

Run the following commands to install the necessary Python packages:

```bash
pip install temporalio
pip install langchain
pip install openai
```

### Configuring OpenAI API Key

Export your OpenAI API key as an environment variable. Replace `YOUR_API_KEY` with your actual OpenAI API key.

```bash
export OPENAI_API_KEY='YOUR_API_KEY'
```

### Running the Temporal Server

If you have installed the Temporal CLI, open a new terminal window and start the Temporal development server with the following command:

```bash
# terminal zero
temporal server start-dev
```

### Running the Worker and Server

In separate terminal windows, run the worker script and the server script:

```bash
# terminal one
python worker.py

# terminal two
python server.py
```

## Using the Application

### Example Requests

Once the server is running, you can test the translation functionality using `curl` commands. Here are some examples:

```bash
curl -X POST "http://localhost:8000/translate?phrase=hello%20world&language=Spanish"
curl -X POST "http://localhost:8000/translate?phrase=hello%20world&language=French"
```

### Expected Results

You should receive translated responses in JSON format. For example:

```json
{"translation":"Hola mundo"}
{"translation":"Bonjour tout le monde"}
```