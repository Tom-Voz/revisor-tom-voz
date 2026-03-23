import streamlit as st
import requests

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor de Tom e Voz")
st.caption("Seguindo o manual do Governo de SP")

# Manual
MANUAL = """
Regras:
- Use linguagem simples e clara
- Use "você" para se dirigir ao leitor
- Seja direto e resolutivo
- Trate com respeito
"""

# Modelo gratuito do Hugging Face
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

def chamar_modelo(texto):
    """Chama a API gratuita do Hugging Face"""
    payload = {"inputs": texto}
    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return f"Erro: {response.status_code}"

st.write("### ✅ Sistema pronto!")

opcao = st.radio("Escolha:", ["Revisar texto", "Criar texto"])

if opcao == "Revisar texto":
    texto = st.text_area("Texto original:", height=150, placeholder="Ex: O cidadão deve efetuar o pagamento do IPTU...")
    if st.button("Revisar"):
        if texto:
            with st.spinner("Revisando..."):
                prompt = f"{MANUAL}\n\nRevise este texto: {texto}\n\nTexto revisado:"
                resposta = chamar_modelo(prompt)
                st.write("### Texto revisado:")
                st.write(resposta)

else:
    assunto = st.text_input("Assunto:", placeholder="Ex: Prazo do IPTU")
    if st.button("Criar"):
        if assunto:
            with st.spinner("Criando..."):
                prompt = f"{MANUAL}\n\nCrie um texto sobre: {assunto}\n\nTexto:"
                resposta = chamar_modelo(prompt)
                st.write("### Texto criado:")
                st.write(resposta)
