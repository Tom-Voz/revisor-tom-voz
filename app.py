import streamlit as st
import re

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

def revisar_texto(texto):
    """Revisão simples seguindo o manual"""
    
    # 1. Substituir termos formais por simples
    texto = texto.replace("O cidadão", "Você")
    texto = texto.replace("o cidadão", "você")
    texto = texto.replace("deve efetuar o pagamento", "pode pagar")
    texto = texto.replace("efetuar o pagamento", "pagar")
    texto = texto.replace("através de", "pelo")
    texto = texto.replace("mensalmente", "todo mês")
    texto = texto.replace("realizar", "fazer")
    
    # 2. Tornar dialógico
    texto = texto.replace("qualquer pessoa", "você")
    texto = texto.replace("contribuinte", "você")
    
    # 3. Simplificar RG
    texto = texto.replace("O RG", "Seu RG")
    texto = texto.replace("o RG", "seu RG")
    texto = texto.replace("pode ser retirado", "está disponível")
    
    # 4. Simplificar linguagem jurídica
    texto = texto.replace("Em vista da previsão legal da incapacidade dos menores de 16 anos responderem pelos atos da vida civil", 
                          "Menores de 16 anos não podem responder legalmente por si mesmos")
    texto = texto.replace("devidamente representados", "acompanhados dos pais ou responsáveis")
    texto = texto.replace("nas solicitações de suas carteiras de identidade", "para pedir o RG")
    texto = texto.replace("os menores devem estar", "eles precisam estar")
    
    # 5. Corrigir frases
    texto = texto.replace("Seu RG seu RG", "Seu RG")
    texto = texto.replace("você você", "você")
    
    # 6. Garantir ponto final
    if texto and texto[-1] not in '.!?':
        texto += '.'
    
    return texto

def criar_texto(assunto, tom):
    """Cria conteúdo simples"""
    
    if "iptu" in assunto.lower():
        texto = f"Você pode pagar o IPTU pelo app todo mês. É rápido e você não precisa sair de casa."
    elif "rg" in assunto.lower():
        texto = f"Seu RG fica pronto em 5 dias úteis. Você pode retirar com o número do protocolo."
    elif "atendimento" in assunto.lower():
        texto = f"Você pode falar conosco pelo telefone 156, pelo chat ou pelo app. Escolha o melhor para você."
    else:
        texto = f"Você pode resolver isso de forma simples. Acesse nossos canais digitais e faça agora mesmo."
    
    if tom == "Empático":
        texto += " Estamos aqui para ajudar você."
    elif tom == "Motivador":
        texto += " Vamos juntos construir uma São Paulo melhor!"
    elif tom == "Direto":
        texto = "Atenção: " + texto[0].lower() + texto[1:]
    
    return texto

# Interface
st.markdown("### 📖 Revisor e Criador de Conteúdo")
st.markdown("Baseado no manual oficial de tom e voz do Governo de SP")

aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    texto_original = st.text_area(
        "Texto para revisar:", 
        height=120,
        placeholder="Cole seu texto aqui..."
    )
    
    if st.button("Revisar Texto", type="primary"):
        if texto_original:
            texto_revisado = revisar_texto(texto_original)
            
            st.markdown("**📄 Original**")
            st.info(texto_original)
            
            st.markdown("**✅ Revisado**")
            st.success(texto_revisado)
        else:
            st.warning("Digite um texto para revisar.")

with aba2:
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto:", placeholder="Ex: IPTU, RG, atendimento")
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    if st.button("Criar Texto", type="primary"):
        if assunto:
            texto_criado = criar_texto(assunto, tom)
            st.markdown("**📝 Texto criado**")
            st.success(texto_criado)
        else:
            st.warning("Digite o assunto.")

st.divider()
st.caption("📌 Manual oficial: cms.sp.gov.br/cms/tomevoz")
