import streamlit as st
import google.generativeai as genai

st.title("Teste de Modelos Gemini")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    st.write("### Modelos disponíveis:")
    
    # Listar todos os modelos
    models = genai.list_models()
    
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            st.write(f"- **{model.name}**")
            
    st.success("Teste concluído!")
    
except Exception as e:
    st.error(f"Erro: {e}")
