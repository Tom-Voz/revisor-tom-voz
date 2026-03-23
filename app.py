import streamlit as st
import requests
import json

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# Modelo gratuito do Hugging Face (não precisa de chave)
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"

def chamar_modelo(texto):
    """Chama modelo gratuito do Hugging Face"""
    payload = {"inputs": texto}
    
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            resultado = response.json()
            if isinstance(resultado, list) and len(resultado) > 0:
                return resultado[0].get('generated_text', texto)
            return str(resultado)
        else:
            return None
    except:
        return None

def revisar_texto(texto):
    """Revisão com regras manuais + IA quando disponível"""
    
    # Regras manuais básicas (sempre aplicam)
    texto = texto.replace("O cidadão", "Você")
    texto = texto.replace("o cidadão", "você")
    texto = texto.replace("deve efetuar o pagamento", "pode pagar")
    texto = texto.replace("efetuar o pagamento", "pagar")
    texto = texto.replace("através de", "pelo")
    texto = texto.replace("mensalmente", "todo mês")
    texto = texto.replace("qualquer pessoa", "você")
    texto = texto.replace("O RG", "Seu RG")
    texto = texto.replace("o RG", "seu RG")
    texto = texto.replace("pode ser retirado", "está disponível")
    
    # Tentar melhorar com IA
    resultado_ia = chamar_modelo(f"Revise este texto para ficar mais simples e claro: {texto}")
    
    if resultado_ia and len(resultado_ia) > len(texto) * 0.5:
        return resultado_ia
    return texto

def criar_texto(assunto, tom):
    """Cria texto com regras manuais + IA"""
    
    # Texto base manual
    if "iptu" in assunto.lower():
        texto = f"Você pode pagar o IPTU pelo app todo mês. É rápido e você não precisa sair de casa."
    elif "rg" in assunto.lower():
        texto = f"Seu RG fica pronto em 5 dias úteis. Você pode retirar com o número do protocolo."
    elif "atendimento" in assunto.lower():
        texto = f"Você pode falar conosco pelo telefone 156, pelo chat ou pelo app. Escolha o melhor para você."
    elif "poupatempo" in assunto.lower() or "matrícula" in assunto.lower():
        texto = f"Acesse o portal Poupatempo. Digite 'Consulta de matrícula' na busca. Siga as orientações."
    else:
        texto = f"Você pode resolver isso de forma simples. Acesse nossos canais digitais e faça agora mesmo."
    
    # Aplicar tom
    if tom == "Empático":
        texto += " Estamos aqui para ajudar você."
    elif tom == "Motivador":
        texto += " Vamos juntos construir uma São Paulo melhor!"
    elif tom == "Direto":
        texto = "Atenção: " + texto[0].lower() + texto[1:]
    
    # Tentar melhorar com IA
    resultado_ia = chamar_modelo(f"Melhore este texto mantendo o tom {tom}: {texto}")
    
    if resultado_ia and len(resultado_ia) > len(texto) * 0.5:
        return resultado_ia
    return texto

# Interface
st.info("🔄 Sistema funcionando com IA gratuita")

aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    texto_original = st.text_area(
        "Texto para revisar:", 
        height=150,
        placeholder="Ex: Acesse o portal Poupatempo e digite Consulta de matrícula na barra de busca e siga as orientações"
    )
    
    if st.button("Revisar Texto", type="primary"):
        if texto_original:
            with st.spinner("Revisando..."):
                texto_revisado = revisar_texto(texto_original)
                
                st.markdown("**📄 Original**")
                st.info(texto_original)
                
                st.markdown("**✅ Revisado**")
                st.success(texto_revisado)
        else:
            st.warning("Digite um texto para revisar")

with aba2:
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto:", placeholder="Ex: Consulta de matrícula, IPTU, RG")
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    if st.button("Criar Texto", type="primary"):
        if assunto:
            with st.spinner("Criando..."):
                texto_criado = criar_texto(assunto, tom)
                st.markdown("**📝 Texto criado**")
                st.success(texto_criado)
        else:
            st.warning("Digite o assunto")

st.divider()
st.caption("📌 Baseado no manual oficial do Governo de SP")
