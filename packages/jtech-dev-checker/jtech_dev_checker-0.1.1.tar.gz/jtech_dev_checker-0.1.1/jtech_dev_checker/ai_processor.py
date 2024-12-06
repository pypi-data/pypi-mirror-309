from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def analyze_code_with_manifesto(manifesto, diff):
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.0)

        prompt = f"""
        Você é um assistente de revisão de código. Use o manifesto a seguir para avaliar as mudanças no código.

        Manifesto:
        {manifesto}

        Código Modificado (Diff):
        {diff}

        Sugira melhorias e valide a conformidade com o manifesto.
        """
        template = ChatPromptTemplate.from_template(prompt)
        out = StrOutputParser()
        chain = template | llm | out
        return chain.invoke({"manifesto": manifesto, "diff": diff})
    except Exception as e:
        raise RuntimeError(f"Erro ao processar com LangChain: {e}")
