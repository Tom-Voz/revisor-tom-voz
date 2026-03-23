import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Teste Modelos", page_icon="🔧")
st.title("🔧 Teste de Modelos Gemini")

try:
    # Pegar a chave dos secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    st.write("✅ API configurada com sucesso!")
    st.write("")
    st.write("### 📋 Modelos disponíveis para generateContent:")
    
    # Listar todos os modelos
    models = genai.list_models()
    
    encontrou = False
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            st.write(f"- **{model.name}**")
            encontrou = True
    
    if not encontrou:
        st.warning("Nenhum modelo com generateContent encontrado.")
    
    # Teste rápido com um modelo simples
    st.write("")
    st.write("### 🧪 Teste rápido:")
    
    try:
        # Tentar usar gemini-pro (nome mais comum)
        test_model = genai.GenerativeModel('gemini-pro')
        response = test_model.generate_content("Diga apenas: OK funcionou!")
        st.success(f"✅ Modelo gemini-pro funcionou! Resposta: {response.text}")
    except Exception as e:
        st.error(f"❌ gemini-pro falhou: {e}")
    
except Exception as e:
    st.error(f"❌ Erro geral: {e}")
    st.write("Verifique se a chave API está correta nos Secrets.")
