import streamlit as st
import requests

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# ========== DIAGNÓSTICO ==========
st.write("### 🔧 Diagnóstico da API")

try:
    chave = st.secrets.get("GEMINI_API_KEY", None)
    
    if chave is None:
        st.error("❌ Chave não encontrada no Secrets")
        st.write("Configure nos Secrets do Streamlit com o nome: GEMINI_API_KEY")
        st.stop()
    else:
        st.success(f"✅ Chave encontrada (começa com: {chave[:10]}...)")
        
        # Testar a chave
        url = f"https://generativelanguage.googleapis.com/v1/models?key={chave}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                st.success("✅ Chave válida! API funcionando.")
                dados = response.json()
                modelos = [m["name"] for m in dados.get("models", [])]
                st.write(f"Modelos disponíveis: {len(modelos)}")
            else:
                st.error(f"❌ Chave inválida. Status: {response.status_code}")
                st.write(f"Resposta: {response.text[:200]}")
                st.stop()
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
            st.stop()
            
except Exception as e:
    st.error(f"Erro ao ler Secrets: {e}")
    st.stop()

st.divider()
st.write("### ✅ Sistema pronto para usar!")

# ========== FUNÇÕES ==========
MANUAL = """
Você é um especialista em comunicação do Governo de São Paulo.

Nossa voz:
- Simples: linguagem clara, frases curtas
- Prestativa: proativa, resolve problemas, acolhedora
- Confiável: informações corretas, sem ambiguidades

Regras:
- Use "você" em vez de "o cidadão"
- Use "pagar" em vez de "efetuar pagamento"
- Use "pelo" em vez de "através de"
- Use "todo mês" em vez de "mensalmente"
- Frases curtas e diretas
"""

def chamar_gemini(prompt):
    """Chama a API do Gemini"""
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={st.secrets['GEMINI_API_KEY']}"
    headers = {"Content-Type": "application/json"}
    
    # Formato correto da API
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        # Log para diagnóstico
        st.write(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            resultado = response.json()
            return resultado["candidates"][0]["content"]["parts"][0]["text"]
        else:
            st.write(f"Erro: {response.text}")
            return None
    except Exception as e:
        st.write(f"Exceção: {e}")
        return None

# ========== INTERFACE ==========
aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    texto = st.text_area("Texto para revisar:", height=150)
    
    if st.button("Revisar", type="primary"):
        if texto:
            with st.spinner("Revisando com IA..."):
                prompt = f"{MANUAL}\n\nRevise este texto: {texto}\n\nResponda APENAS com o texto revisado."
                resultado = chamar_gemini(prompt)
                if resultado:
                    st.markdown("**Original**")
                    st.info(texto)
                    st.markdown("**Revisado**")
                    st.success(resultado)
                else:
                    st.error("Erro ao revisar. Tente novamente.")
        else:
            st.warning("Digite um texto")

with aba2:
    assunto = st.text_input("Assunto:")
    tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    if st.button("Criar", type="primary"):
        if assunto:
            with st.spinner("Criando com IA..."):
                prompt = f"{MANUAL}\n\nCrie um texto sobre: {assunto}\nTom: {tom}\n\nResponda APENAS com o texto criado."
                resultado = chamar_gemini(prompt)
                if resultado:
                    st.markdown("**Texto criado**")
                    st.success(resultado)
                else:
                    st.error("Erro ao criar. Tente novamente.")
        else:
            st.warning("Digite o assunto")
