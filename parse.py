import os
import json
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from langchain.callbacks.tracers.langchain import LangChainTracer
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class LLMParser:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        groq_api_key = os.getenv("GROQ_API_KEY")
        os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
        os.environ["LANGCHAIN_TRACKING_V2"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT","LLM powered Web Scraper")

        # Store components
        self.tracer = LangChainTracer()
        self.config = RunnableConfig(callbacks=[self.tracer])
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)
        self.parser = StrOutputParser()

        # Prompt template
        self.template = (
            "You are an intelligent parser. Your task is to extract specific data fields from the given text content.\n\n"
            "Content to parse:\n"
            "{markdown_content}\n\n"
            "Extraction Instructions:\n"
            "1. Extract values for the following fields only: {fields}.\n"
            "2. If a field is not present in the content, return an empty string for that field.\n"
            "3. Return the output as a valid JSON object.\n"
            "4. Do not include any extra text, comments, or formatting—only return the JSON.\n\n"
            "Example (if fields were 'name, price'):\n"
            "{{\n"
            "  \"name\": \"Widget\",\n"
            "  \"price\": \"$15\"\n"
            "}}\n\n"
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
