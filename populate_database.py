from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from get_embedding_function import get_embedding_function



CHROMA_PATH = "chroma"
DATA_PATH = "data"


def main():
    documents = load_documents()
    chunks = split_documents(documents)
    save_to_chroma(chunks)


def load_documents():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    # Ensure page numbers are explicitly present
    for chunk in chunks:
        if "page" not in chunk.metadata:
            chunk.metadata["page"] = "unknown"

    return chunks



def save_to_chroma(chunks):
    embedding_function = get_embedding_function()

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function
    )

    db.add_documents(chunks)
    db.persist()

    print(f"✅ Added {len(chunks)} chunks to Chroma")


if __name__ == "__main__":
    main()
