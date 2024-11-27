import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

def read_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def main():
    st.title("PDF 문서 분석기 with Gemini")

    # API 키 입력
    api_key = st.text_input("Google API 키를 입력하세요", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        
        # PDF 파일 업로드
        uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=['pdf'])
        
        if uploaded_file is not None:
            # PDF 텍스트 추출
            pdf_text = read_pdf(uploaded_file)
            
            # 사용자 질문 입력
            user_question = st.text_input("PDF에 대해 질문하세요")
            
            if user_question:
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(
                        f"다음 텍스트에 대해 답변해주세요. 질문: {user_question}\n\n텍스트: {pdf_text}"
                    )
                    st.write("답변:", response.text)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
