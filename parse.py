import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM

class LLMParser:
    def __init__(self):
        
        self.llm = OllamaLLM(model="llama3:8b")
        self.parser = StrOutputParser()
        

        # Prompt template
        self.template = (
                "You are an intelligent parser. Your task is to extract specific data fields from the given **markdown-formatted** text content.\n\n"
                "Markdown Content to parse:\n"
                "{markdown_content}\n\n"
                "Extraction Instructions:\n"
                "1. Extract values for the following fields only: {fields}.\n"
                "2. If a field is not present in the content, return an empty string for that field.\n"
                "3. Return the output as a valid JSON object.\n"
                "4. Enclose the JSON output strictly within triple backticks and label it as a JSON code block (```json ... ```).\n"
                "5. Do not include any other text, explanation, or formatting — only return the JSON block.\n\n"
                "Example (if fields were 'name, price'):\n"
                "```json\n"
                "{{\n"
                "  \"name\": \"Widget\",\n"
                "  \"price\": \"$15\"\n"
                "}}\n"
                "```\n\n"
                "Now extract the fields: {fields}"
            )

        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.llm | self.parser

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

    def parse(self, markdown_content: str, fields) -> list:
        if isinstance(fields, list):
            fields = ", ".join(fields)

        dom_chunks = self.splitter.split_text(markdown_content)

        results = []
        for i, chunk in enumerate(dom_chunks, start=1):
            response = self.chain.invoke({
                "markdown_content": chunk,
                "fields": fields
            })
            print(f"Parsed chunk {i} of {len(dom_chunks)}")
            try:
                parsed = json.loads(response)
                results.append(parsed)
            except json.JSONDecodeError:
                print(f"Warning: Chunk {i} produced invalid JSON.")
                results.append({})

        return results
