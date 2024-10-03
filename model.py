from transformers import AutoModel, AutoTokenizer

def get_embeddings(sentences):

    #Load model from HuggingFace Hub
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
    model = AutoModel.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')

    #Tokenize sentences
    encoded_input = tokenizer(sentences,padding=True)