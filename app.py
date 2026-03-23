import streamlit as st
import requests
import json

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# Manual de tom e voz completo
MANUAL = """
Você é um especialista em comunicação do Governo de São Paulo.

Nossa voz (sempre):
- Simples: linguagem clara, frases curtas, só o necessário
- Prestativa: proativa, resolve problemas, acolhedora, desburocratizada
- Confiável: informações corretas, sem ambiguidades, comunicação universal

Regras práticas:
- Use "você" em vez de "o cidadão"
- Use "pagar" em vez de "efetuar pagamento"
- Use "pelo" em vez de "através de"
- Use "todo mês" em vez de "mensalmente"
- Use "pelo app" em vez de "através do aplicativo"
- Frases curtas e diretas
- Seja acolhedor quando apropriado
- Evite termos técnicos desnecessários

Processo de edição:
1. Expanda com contexto importante
2. Torne conciso (remova redundâncias)
3. Torne dialógico (use "você")
4. Simplifique (termos mais comuns)
"""

# Pegar chave
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Configure a chave API em Settings → Secrets")
    st.stop()

# Usando gemini-2.0-flash (disponível na lista)
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def chamar_gemini(prompt):
    """Chama a API do Gemini"""
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            resultado = response.json()
            return resultado["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return None
    except Exception as e:
        return None

# Teste de conexão
with st.spinner("Verificando conexão com o Gemini..."):
    teste = chamar_gemini("Diga apenas: OK")
    if teste:
        st.success("✅ Conectado ao Gemini 2.0 Flash!")
    else:
        st.error("❌ Falha na conexão. Verifique sua chave API.")

st.divider()

aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    texto = st.text_area("Texto para revisar:", height=150, 
                         placeholder="Ex: Acesse o portal Poupatempo e digite Consulta de matrícula na barra de busca e siga as orientações")
    
    if st.button("Revisar", type="primary"):
        if texto:
            with st.spinner("Revisando com IA..."):
                prompt = f"""
                {MANUAL}
                
                Revise este texto seguindo as regras acima.
                Mantenha o sentido original, apenas melhore a linguagem.
                
                TEXTO ORIGINAL: {texto}
                
                Responda APENAS com o texto revisado.
                """
                resultado = chamar_gemini(prompt)
                if resultado:
                    st.markdown("**📄 Original**")
                    st.info(texto)
                    st.markdown("**✅ Revisado**")
                    st.success(resultado)
                else:
                    st.error("Erro ao revisar. Tente novamente.")
        else:
            st.warning("Digite um texto para revisar")

with aba2:
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto:", placeholder="Ex: Consulta de matrícula, IPTU, RG")
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    if st.button("Criar", type="primary"):
        if assunto:
            with st.spinner("Criando com IA..."):
                prompt = f"""
                {MANUAL}
                
                Crie um texto sobre: {assunto}
                Tom: {tom}
                Público: Cidadãos de São Paulo
                
                O texto deve ser natural, acolhedor e seguir todas as regras.
                Responda APENAS com o texto criado.
                """
                resultado = chamar_gemini(prompt)
                if resultado:
                    st.markdown("**✨ Texto criado**")
                    st.success(resultado)
                else:
                    st.error("Erro ao criar. Tente novamente.")
        else:
            st.warning("Digite o assunto")

st.divider()
st.caption("📌 Manual oficial: cms.sp.gov.br/cms/tomevoz | IA: Gemini 2.0 Flash")
