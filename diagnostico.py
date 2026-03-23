import streamlit as st
import requests

st.set_page_config(page_title="Diagnóstico", page_icon="🔧")
st.title("🔧 Diagnóstico da API Gemini")

# Pegar chave
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    st.write(f"✅ Chave encontrada: {API_KEY[:10]}... (tamanho: {len(API_KEY)})")
except Exception as e:
    st.error(f"❌ Chave não encontrada: {e}")
    st.stop()

# Testar endpoint de listagem de modelos
st.write("### Teste 1: Listar modelos disponíveis")

url_lista = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"
try:
    response = requests.get(url_lista, timeout=10)
    st.write(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        dados = response.json()
        modelos = [m["name"] for m in dados.get("models", [])]
        st.success(f"✅ Modelos encontrados: {len(modelos)}")
        for m in modelos[:5]:
            st.write(f"- {m}")
    else:
        st.error(f"Erro: {response.text}")
except Exception as e:
    st.error(f"Erro na requisição: {e}")

# Testar com modelo específico
st.write("### Teste 2: Testar modelo gemini-2.0-flash")

url_teste = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={API_KEY}"
headers = {"Content-Type": "application/json"}
data = {
    "contents": [{
        "parts": [{"text": "Diga apenas: OK funcionou"}]
    }]
}

try:
    response = requests.post(url_teste, headers=headers, json=data, timeout=15)
    st.write(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        resultado = response.json()
        texto = resultado["candidates"][0]["content"]["parts"][0]["text"]
        st.success(f"✅ Funcionou! Resposta: {texto}")
    else:
        st.error(f"Erro: {response.text}")
except Exception as e:
    st.error(f"Erro: {e}")

st.info("Copie esta página para mim para que eu possa ver o resultado.")
