import streamlit as st
import requests

st.set_page_config(page_title="Diagnóstico", page_icon="🔧")
st.title("🔧 Diagnóstico da API Gemini")

st.write("### Verificando Secrets...")

try:
    # Tentar ler a chave de diferentes formas
    chave = st.secrets.get("GEMINI_API_KEY", None)
    
    if chave is None:
        st.error("❌ Chave não encontrada no Secrets")
        st.write("Todas as chaves disponíveis:", list(st.secrets.keys()))
    else:
        st.success(f"✅ Chave encontrada: {chave[:10]}... (tamanho: {len(chave)})")
        
        # Testar com a chave
        url = f"https://generativelanguage.googleapis.com/v1/models?key={chave}"
        st.write("### Testando a chave...")
        
        try:
            response = requests.get(url, timeout=10)
            st.write(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                st.success("✅ Chave válida! Modelos disponíveis.")
                dados = response.json()
                modelos = [m["name"] for m in dados.get("models", [])]
                for m in modelos[:5]:
                    st.write(f"- {m}")
            else:
                st.error(f"❌ Chave inválida. Resposta: {response.text}")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
            
except Exception as e:
    st.error(f"Erro ao ler Secrets: {e}")

st.info("Se aparecer 'Chave não encontrada', configure nos Secrets do Streamlit.")
