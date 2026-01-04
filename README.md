# AI YAML Assistant

An AI-powered YAML editing assistant in Python that updates YAML configuration files based on natural language instructions using the OpenAI API.  
This tool reads a YAML file, asks an LLM for **structured update instructions**, applies them safely, and writes the updated YAML back. The design avoids hallucinations and keeps updates deterministic.

## 🚀 Features

- 🤖 Uses OpenAI GPT models to interpret human instructions  
- 📄 Reads and writes YAML files safely  
- 🛠️ Structured schema-guided updates to YAML (no freeform rewriting)  
- 🔁 Works interactively in Jupyter or as a standalone script  
- ✅ Easy to integrate into GitHub workflows or automation pipelines

## 🧠 How It Works

1. Read the existing YAML from disk.
2. Send the YAML + user instruction to the OpenAI API with a strict schema prompt.
3. Parse the model’s structured response for fields and values to update.
4. Apply the update paths safely in Python.
5. Write the updated YAML back to disk.

> This approach avoids the LLM **rewriting the entire file**, and instead produces deterministic, structured changes.


## 🔨Prerequisites to run the code

OPENAI_API_KEY=your_api_key_here or any open source LLM model works fine (OLLAMA). 


⚙️ Design Overview

1. Pydantic models enforce safe structured output from the LLM.
2. The script uses a strict system prompt to constrain generation.
3. YAML paths are validated before mutation to prevent invalid edits.