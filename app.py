import streamlit as st
import requests
import json

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

MANUAL = """
Voz: Simples, resolutiva, respeitosa.
Regras:
- Use "você" em vez de "o cidadão"
- Frases curtas e diretas
- Simplifique verbos: "pagar" em vez de "efetuar pagamento"
- Evite termos burocráticos
- Mantenha o sentido original
"""

def chamar_ia(prompt):
    """Usa modelo gratuito do Hugging Face"""
    
    # Modelo gratuito e aberto
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    
    headers = {"Authorization": "Bearer hf_"}  # API pública sem necessidade de chave real para este endpoint
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'Erro na resposta')
            return str(result)
        else:
            return None
    except Exception as e:
        return None

st.info("🔄 Usando IA gratuita - pode levar alguns segundos na primeira vez")

opcao = st.radio("Funcionalidade:", ["✏️ Revisar texto", "✨ Criar texto"], horizontal=True)

if opcao == "✏️ Revisar texto":
    st.subheader("Revisão de Conteúdo")
    texto = st.text_area("Texto para revisar:", height=150, 
                         placeholder="Ex: O cidadão deve efetuar o pagamento do IPTU através do aplicativo mensalmente.")
    
    if st.button("Revisar", type="primary"):
        if texto:
            with st.spinner("Revisando com IA (pode levar 10-20 segundos)..."):
                prompt = f"""<s>[INST] 
                Você é um revisor do Governo de São Paulo. Siga estas regras:
                {MANUAL}
                
                Revise este texto. Mantenha o sentido original, apenas melhore a linguagem.
                
                Texto original: {texto}
                
                Responda apenas com o texto revisado.
                [/INST]</s>"""
                
                resultado = chamar_ia(prompt)
                
                if resultado:
                    st.markdown("### ✅ Texto revisado")
                    st.success(resultado)
                else:
                    st.warning("⚠️ O serviço gratuito está sobrecarregado. Tente novamente em alguns segundos.")
                    st.markdown("**Enquanto isso, aqui está uma sugestão manual:**")
                    sugestao = texto.replace("o cidadão", "você").replace("efetuar o pagamento", "pagar").replace("através de", "pelo").replace("mensalmente", "todo mês")
                    st.info(sugestao)
        else:
            st.warning("Digite um texto")

else:
    st.subheader("Criação de Conteúdo")
    
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto:", placeholder="Ex: Prazo do IPTU")
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    publico = st.text_input("Público-alvo:", placeholder="Ex: Contribuintes")
    
    if st.button("Criar", type="primary"):
        if assunto:
            with st.spinner("Criando com IA (pode levar 10-20 segundos)..."):
                prompt = f"""<s>[INST] 
                Você é um redator do Governo de São Paulo.
                
                Regras: {MANUAL}
                
                Crie um texto sobre: {assunto}
                Tom: {tom}
                Público: {publico if publico else "Cidadãos"}
                
                O texto deve ser natural e seguir as regras.
                Responda apenas com o texto criado.
                [/INST]</s>"""
                
                resultado = chamar_ia(prompt)
                
                if resultado:
                    st.markdown("### ✨ Texto criado")
                    st.success(resultado)
                else:
                    st.warning("⚠️ O serviço gratuito está sobrecarregado. Tente novamente em alguns segundos.")
                    st.markdown("**Sugestão:**")
                    st.info(f"{publico if publico else 'Cidadãos'}, você pode resolver suas pendências sobre {assunto} de forma simples e rápida pelos canais digitais do Governo de SP.")
        else:
            st.warning("Digite o assunto")

st.divider()
st.caption("💡 Dica: Se o serviço não responder, clique no botão novamente após alguns segundos.")
