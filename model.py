from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber
import torch
import numpy as np

#mean pooling
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #first element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded,1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

# To extract text from pdf
def extract_pdf_data(file_path):
    data = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                data += text
    # print(data)
    return data

def get_embeddings(sentences):

    #Load model from HuggingFace Hub
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
    model = AutoModel.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')

    #Tokenize senetences
    encoded_input = tokenizer(sentences, padding=True, truncation=True,return_tensors='pt', max_length=512)
    # print(encoded_input)

    #compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    #max pooling
    embeddings = mean_pooling(model_output,encoded_input['attention_mask'])

    return embeddings

def cosine(embeddings1, embeddings2):
    score_list = []
    for i in embeddings1:
        matchPercentage = cosine_similarity(np.array(i), np.array(embeddings2))
        matchPercentage = np.round(matchPercentage,4)*100 #round to two decimal
        print("Your resume matches about" +str(matchPercentage[0])+ "% of the job description.")
        score_list.append(str(matchPercentage[0][0]))
    return score_list

output = extract_pdf_data('D:/symca/project/resume-analysis-and-candidate-selector/resumes/Alice_Johnson_Resume.pdf')

# get_embeddings(output)