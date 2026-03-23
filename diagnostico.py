import streamlit as st
import google.generativeai as genai

st.title("Diagnóstico da API Gemini")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.write(f"✅ Chave carregada (tamanho: {len(api_key)} caracteres)")
    
    # Configurar
    genai.configure(api_key=api_key)
    
    # Listar TODOS os modelos
    st.write("### Lista completa de modelos:")
    modelos = genai.list_models()
    
    lista_modelos = list(modelos)
    
    if len(lista_modelos) == 0:
        st.error("❌ Nenhum modelo retornado pela API")
        st.info("Isso geralmente significa que a chave API é inválida ou não tem permissões")
    else:
        for m in lista_modelos:
            st.write(f"- {m.name}")
            st.write(f"  Métodos: {m.supported_generation_methods}")
            st.write("---")
            
except Exception as e:
    st.error(f"Erro: {e}")
    st.write("Tipo do erro:", type(e).__name__)
