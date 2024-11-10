from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from core.config import settings
import asyncio

class ChatService:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY,
            model_name="gpt-3.5-turbo"
        )
        
        self.prompt = PromptTemplate(
            input_variables=["history", "input"],
            template="""
            You are a helpful AI assistant. Use the following conversation history
            and the human's latest input to provide a helpful response.
            
            Conversation History: {history}
            Human: {input}
            AI Assistant:"""
        )
        
        self.memory = ConversationBufferMemory(return_messages=True)
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt,
            verbose=True
        )
    
    async def get_response(self, message: str) -> str:
        """Get AI response for user message"""
        # Run in threadpool since LangChain's methods are synchronous
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            self.conversation.predict, 
            message
        )
        return response

    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
        