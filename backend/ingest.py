import os
import pickle

DATA_PATH = "data"
VECTORSTORE_PATH = "vectorstore"


def load_text_files():
    texts = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
                texts.append(f.read())
    return texts


def split_text(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def main():
    print("Loading data...")
    texts = load_text_files()

    chunks = []
    for text in texts:
        chunks.extend(split_text(text))

    os.makedirs(VECTORSTORE_PATH, exist_ok=True)

    with open(os.path.join(VECTORSTORE_PATH, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)

    print("Chunks stored successfully!")


if __name__ == "__main__":
    main()