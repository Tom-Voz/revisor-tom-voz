import streamlit as st
import re

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

def revisar_texto(texto):
    """Revisa o texto com regras precisas"""
    
    # Guardar original para referência
    original = texto
    
    # 1. Substituir sujeitos (mapeamento direto)
    texto = re.sub(r'\bO cidadão\b', 'Você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bo cidadão\b', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bcontribuinte\b', 'você', texto, flags=re.IGNORECASE)
    
    # 2. Simplificar verbos
    texto = re.sub(r'\befetuar o pagamento\b', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\brealizar o pagamento\b', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bdeve\b', 'pode', texto, flags=re.IGNORECASE)
    
    # 3. Simplificar preposições
    texto = re.sub(r'\batravés de\b', 'pelo', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bpor meio de\b', 'pelo', texto, flags=re.IGNORECASE)
    
    # 4. Simplificar advérbios
    texto = re.sub(r'\bmensalmente\b', 'todo mês', texto, flags=re.IGNORECASE)
    
    # 5. CORREÇÃO: Evitar duplicação do IPTU
    # Se tiver "pagar o IPTU do IPTU", corrigir
    texto = re.sub(r'pagar o IPTU do IPTU', 'pagar o IPTU', texto, flags=re.IGNORECASE)
    texto = re.sub(r'pagar IPTU do IPTU', 'pagar o IPTU', texto, flags=re.IGNORECASE)
    texto = re.sub(r'do IPTU do IPTU', 'do IPTU', texto, flags=re.IGNORECASE)
    
    # 6. Garantir que "IPTU" apareça corretamente
    if "IPTU" in original and "IPTU" not in texto:
        texto = texto.replace("pagar", "pagar o IPTU")
    
    # 7. Limpar espaços duplicados
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # 8. Capitalizar início
    if texto and texto[0].islower():
        texto = texto[0].upper() + texto[1:]
    
    # 9. Garantir ponto final
    if not texto.endswith(('.', '!', '?')):
        texto += '.'
    
    return texto

def criar_texto(assunto, tom, publico):
    """Cria textos naturais"""
    
    textos = {
        "iptu": {
            "informativo": f"{publico}, você pode pagar o IPTU pelo app todo mês.",
            "empatico": f"{publico}, para facilitar sua vida, você pode pagar o IPTU pelo app, sem sair de casa.",
            "motivador": f"{publico}, faça sua parte com facilidade! Pague o IPTU pelo app.",
            "direto": f"Atenção, {publico}: pague o IPTU pelo app e evite multas."
        },
        "links": {
            "informativo": f"Preencha os dados e gere os links úteis. Assim, {publico} acessam as informações pelo app.",
            "empatico": f"Quer facilitar o trabalho da sua equipe? Preencha os dados e gere os links úteis para o app.",
            "motivador": f"Vamos facilitar! Gere os links úteis e ajude {publico} a acessar as informações.",
            "direto": f"Preencha os dados. Gere os links. {publico} acessam pelo app."
        },
        "atendimento": {
            "informativo": f"{publico} pode falar conosco pelo telefone 156, pelo chat ou pelo app.",
            "empatico": f"Precisa de ajuda? Estamos aqui para você. Ligue 156, use o chat ou o app.",
            "motivador": f"Atendimento fácil e rápido! Fale conosco pelo 156, chat ou app.",
            "direto": f"Atendimento: Ligue 156, acesse o chat ou o app."
        }
    }
    
    # Identificar categoria
    assunto_lower = assunto.lower()
    if "link" in assunto_lower or "útil" in assunto_lower:
        categoria = "links"
    elif "atendimento" in assunto_lower or "contato" in assunto_lower or "ajuda" in assunto_lower:
        categoria = "atendimento"
    else:
        categoria = "iptu"
    
    # Pegar texto
    tom_key = tom.lower()
    texto = textos[categoria].get(tom_key, textos[categoria]["informativo"])
    
    return texto

# Interface
st.markdown("### 📖 Revisor e Criador de Conteúdo")
st.markdown("Baseado no manual oficial de tom e voz do Governo de SP")

aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    texto_original = st.text_area(
        "Texto para revisar:", 
        height=120,
        placeholder="Ex: O cidadão deve efetuar o pagamento do IPTU através do aplicativo mensalmente."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Revisar", type="primary", use_container_width=True):
            if texto_original:
                texto_revisado = revisar_texto(texto_original)
                
                st.markdown("**Original**")
                st.info(texto_original)
                
                st.markdown("**Revisado**")
                st.success(texto_revisado)
            else:
                st.warning("Digite um texto para revisar.")
    
    with col2:
        if st.button("📋 Carregar exemplo", use_container_width=True):
            st.session_state.exemplo = "O cidadão deve efetuar o pagamento do IPTU através do aplicativo mensalmente."
            st.rerun()
    
    if "exemplo" in st.session_state:
        texto_original = st.session_state.exemplo
        st.rerun()

with aba2:
    col1, col2, col3 = st.columns(3)
    with col1:
        assunto = st.selectbox("Assunto:", ["IPTU", "Links úteis", "Atendimento"])
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    with col3:
        publico = st.selectbox("Público:", ["Cidadãos", "Servidores", "Empresas"])
    
    if st.button("✨ Criar Texto", type="primary", use_container_width=True):
        texto_criado = criar_texto(assunto, tom, publico)
        st.markdown("**Texto criado**")
        st.success(texto_criado)
        
        st.caption(f"🎯 Voz: simples e resolutiva | Tom: {tom} | Público: {publico}")

st.divider()
st.caption("📌 Manual oficial: cms.sp.gov.br/cms/tomevoz/sobre")
