import streamlit as st
import pdfplumber

# To extract text from pdf
def extract_pdf_data(file_path):
    data = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                data += text
    return data

# To extract text from text_area(JD)
def extract_text_data(file_path):
    with open(file_path,'r') as file:
        data = file.read()

    return data


st.header("Application Tracking System")
# Main content
tab1,tab2 = st.tabs(["Home","Result"])

with tab1:
    JD = st.text_area("Enter Job Description", "Type Here ...", height = 200)
    uploaded_files = st.file_uploader("Choose your resume.pdf file: ",type="pdf",accept_multiple_files=True)
    compare_pressed = st.button("Compare")
    if compare_pressed and uploaded_files:
        uploaded_file_paths = [extract_pdf_data(file) for file in uploaded_files]
        score = compare(uploaded_file_paths,JD)


# Results
with tab2:
    st.header("Results")
    my_dict={}
    if compare_pressed and uploaded_files:
        for i in range(len(score)):
            my_dict[uploaded_files[i].name] = score[i]
        sorted_dict = dict(sorted(my_dict.items()))
        for i in sorted_dict.items():
            with st.expander(str[i[0]]):
                st.write("Score is: ",i[1])

        

