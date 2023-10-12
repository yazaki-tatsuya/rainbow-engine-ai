import logging
import os
from typing import List
from langchain.document_loaders import ConfluenceLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
#---- 掲載時不要START ----#
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import env
#---- 掲載時不要END ----#

# Setup logger
handler = logging.StreamHandler()
formatter = logging.Formatter('LANGCHAIN-VECTORIZE: %(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Confluenceドキュメント取得準備
def create_confluence_loader(BASE_URL: str, USER: str, SECRET: str) -> ConfluenceLoader:
    logger.info(f"STEP1: Generate ConfluenceLoader with base URL: {BASE_URL}")
    return ConfluenceLoader(
        url=BASE_URL,
        username=USER,
        api_key=SECRET
    )

# Confluenceからドキュメントをロード
def load_confluence_documents(space: str, loader: ConfluenceLoader) -> List[Document]:
    logger.info("STEP2: START loading documents from Confluence.")
    documents = loader.load(space_key=space, limit=1000)
    # 取得したConfluenceドキュメントの件数を表示
    logger.info(f"STEP2: END loading documents from Confluence. Fetched {len(documents)} document objects.")
    return documents

# ドキュメント分割
def split_documents(documents: List[Document]) -> List[Document]:
    # 長いテキストをチャンク分割（意味的に関連する部分に分割）
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    logger.info(f"STEP3: START splitting documents.")
    splitted = splitter.split_documents(documents)
    logger.info(f"STEP3: END splitting documents. {len(documents)} documents are splitted into {len(splitted)}")
    return splitted

# Prepare for embedding
def create_openai_embeddings(ENBEDDING_DEPLOYMENT: str, ENBEDDING_MODEL: str) -> OpenAIEmbeddings:
    logger.info(f"STEP4: create OpenAIEmbeddings instance.")
    # ベクトル変換のためにOpenAIEmbeddingsクラスを生成
    return OpenAIEmbeddings(
        deployment=ENBEDDING_DEPLOYMENT,
        model=ENBEDDING_MODEL,
        chunk_size=1
    )

# Create Chroma
def create_chroma_db(embeddings: OpenAIEmbeddings, CHROMA_DB_DIR: str):
    # ベクトルデータベースを作成
    logger.info(f"STEP5: create Chroma database.")
    return Chroma(
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_DIR
    )

# Create Chroma vectorstore
def create_vectorstore(documents: List[Document], vectorestore):
    total = len(documents)
    for idx, doc in enumerate(documents):
        logger.info(f" ∟Vectorize {idx + 1} of {total}")
        vectorestore.add_documents([doc])
        vectorestore.persist()
    logger.info("STEP6: Completed persist of vector index.")

# Query Chroma DB
def query_chroma_db(query: str, chroma):
    # Chromaを使った類似検索を実行
    documents = chroma.similarity_search(query=query)
    # 類似検索でヒットした件数を取得
    logger.info(f"STEP7: Similarity search fetched {len(documents)} documents.")
    # 結果をループして表示（上位表示のものほど、類似度が高い）
    for idx, doc in enumerate(documents):
        logger.info(f" ∟検索結果{idx + 1}: {doc.page_content}")

if __name__ == "__main__":
    # Confluence settings
    CONFLUENCE_BASE_URL = env.get_env_variable("CONFLUENCE_BASE_URL")
    CONFLUENCE_USER_ID = env.get_env_variable("CONFLUENCE_USER_ID")
    CONFLUENCE_API_TOKEN = env.get_env_variable("CONFLUENCE_API_TOKEN")
    loader = create_confluence_loader(CONFLUENCE_BASE_URL, CONFLUENCE_USER_ID, CONFLUENCE_API_TOKEN)
    documents = load_confluence_documents("20231230IT", loader)
    documents = split_documents(documents)

    # OpenAI settings
    OPENAI_API_KEY = env.get_env_variable("OPEN_AI_KEY")
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    OPENAI_ENBEDDING_DEPLOYMENT = 'text-embedding-ada-002'
    OPENAI_ENBEDDING_MODEL = 'text-embedding-ada-002'
    embeddings = create_openai_embeddings(OPENAI_ENBEDDING_DEPLOYMENT, OPENAI_ENBEDDING_MODEL)

    # Chroma Vector Database settings
    CHROMA_DB_DIR = ".chroma/vector_index"
    vectorstore = create_chroma_db(embeddings, CHROMA_DB_DIR)
    create_vectorstore(documents, vectorstore)
    query_chroma_db("心臓病の予防に役立つ飲み物は何ですか?", vectorstore)