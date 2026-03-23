import streamlit as st
import re

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

def aplicar_4_passos(texto):
    """Aplica os 4 passos do processo de edição do manual"""
    
    # PASSO 1: EXPANDIR (adicionar contexto quando necessário)
    if "IPTU" in texto and "Imposto" not in texto:
        texto = texto.replace("IPTU", "IPTU (o imposto do seu imóvel)")
    
    if "RG" in texto and "Registro Geral" not in texto:
        texto = texto.replace("RG", "RG (seu documento de identidade)")
    
    # PASSO 2: CONCISAR (remover redundâncias)
    texto = re.sub(r'efetuar o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'realizar o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'fazer o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'pode ser retirado', 'está disponível', texto, flags=re.IGNORECASE)
    texto = re.sub(r'por qualquer pessoa', 'para você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'com o protocolo', 'com o número do protocolo', texto, flags=re.IGNORECASE)
    texto = re.sub(r'dias úteis', 'dias úteis (de segunda a sexta)', texto, flags=re.IGNORECASE)
    
    # PASSO 3: DIALOGAR (usar "você")
    texto = re.sub(r'o cidadão', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'a cidadã', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'os cidadãos', 'vocês', texto, flags=re.IGNORECASE)
    texto = re.sub(r'qualquer pessoa', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'o RG', 'seu RG', texto, flags=re.IGNORECASE)
    texto = re.sub(r'o documento', 'seu documento', texto, flags=re.IGNORECASE)
    
    # PASSO 4: SIMPLIFICAR (substituir termos complexos)
    texto = re.sub(r'através de', 'pelo', texto, flags=re.IGNORECASE)
    texto = re.sub(r'por meio de', 'pelo', texto, flags=re.IGNORECASE)
    texto = re.sub(r'mensalmente', 'todo mês', texto, flags=re.IGNORECASE)
    texto = re.sub(r'anualmente', 'todo ano', texto, flags=re.IGNORECASE)
    texto = re.sub(r'solicitar', 'pedir', texto, flags=re.IGNORECASE)
    texto = re.sub(r'utilizar', 'usar', texto, flags=re.IGNORECASE)
    
    # Correções específicas
    texto = texto.replace("seu RG o RG", "seu RG")
    texto = texto.replace("seu RG está disponível para retirada", "seu RG está disponível para retirada")
    
    return texto

def aplicar_tom(texto, tom):
    """Aplica o tom adequado conforme o manual"""
    
    if tom == "Empático":
        if "sabemos" not in texto and "entendemos" not in texto:
            texto = "Sabemos que você precisa do seu documento. " + texto[0].lower() + texto[1:] if texto else texto
    
    elif tom == "Motivador":
        if "vamos" not in texto:
            texto = "Vamos facilitar sua vida! " + texto[0].lower() + texto[1:] if texto else texto
    
    elif tom == "Direto":
        if not texto.startswith("Atenção"):
            texto = "Atenção: " + texto[0].lower() + texto[1:] if texto else texto
    
    return texto

def revisar_texto(texto, tom="Informativo"):
    """Revisão completa seguindo o manual"""
    
    # Aplicar os 4 passos
    texto = aplicar_4_passos(texto)
    
    # Aplicar o tom
    texto = aplicar_tom(texto, tom)
    
    # Limpar espaços
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # Garantir maiúscula no início
    if texto and texto[0].islower():
        texto = texto[0].upper() + texto[1:]
    
    # Garantir ponto final
    if texto and texto[-1] not in '.!?':
        texto += '.'
    
    return texto

def criar_texto(assunto, tom, publico):
    """Cria conteúdo seguindo voz, tom e processo de edição"""
    
    base_textos = {
        "iptu": f"{publico}, você pode pagar o IPTU pelo app todo mês. É rápido e você não precisa sair de casa.",
        "links": f"Preencha os dados e gere os links úteis. Assim, {publico} acessam as informações pelo app de forma prática.",
        "atendimento": f"{publico} pode falar conosco pelo telefone 156, pelo chat ou pelo app. Escolha o melhor para você.",
        "prazo": f"Fique atento aos prazos, {publico}. Consulte as datas no nosso site ou app. Não deixe para última hora.",
        "documento": f"{publico}, seu documento fica pronto em até 5 dias úteis. Você pode retirar com o número do protocolo.",
        "servico": f"{publico}, você pode resolver esse serviço online. Acesse o app ou site e faça agora mesmo.",
    }
    
    assunto_lower = assunto.lower()
    texto = base_textos["servico"]
    
    for chave in base_textos:
        if chave in assunto_lower:
            texto = base_textos[chave]
            break
    
    texto = aplicar_tom(texto, tom)
    
    return texto

# Interface
st.markdown("### 📖 Revisor e Criador de Conteúdo")
st.markdown("Baseado no manual oficial de tom e voz do Governo de SP")

with st.expander("📘 Ver manual completo"):
    st.markdown("""
    **Nossa Voz:** Simples, resolutiva e respeitosa.
    
    **Nosso Tom:** Informativo, Empático, Motivador ou Direto.
    
    **Processo de Edição (4 passos):**
    1. Expandir - incluir contexto
    2. Concisar - reduzir redundâncias
    3. Dialogar - usar "você"
    4. Simplificar - termos comuns
    """)

aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    texto_original = st.text_area(
        "Texto para revisar:", 
        height=120,
        placeholder="Ex: O RG fica pronto em 5 dias úteis. O RG pode ser retirado por qualquer pessoa com o protocolo"
    )
    
    tom_revisao = st.selectbox("Tom desejado para revisão:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Revisar", type="primary", use_container_width=True):
            if texto_original:
                texto_revisado = revisar_texto(texto_original, tom_revisao)
                
                st.markdown("**📄 Original**")
                st.info(texto_original)
                
                st.markdown("**✅ Revisado**")
                st.success(texto_revisado)
                
                st.markdown("**📋 Passos aplicados:**")
                st.markdown("""
                1. **Expandir:** contexto adicionado quando necessário
                2. **Concisar:** termos burocráticos simplificados
                3. **Dialogar:** 'você' substituiu termos formais
                4. **Simplificar:** palavras complexas foram trocadas
                """)
            else:
                st.warning("Digite um texto para revisar.")
    
    with col2:
        if st.button("📋 Carregar exemplo", use_container_width=True):
            st.session_state.exemplo = "O RG fica pronto em 5 dias úteis. O RG pode ser retirado por qualquer pessoa com o protocolo"
            st.rerun()
    
    if "exemplo" in st.session_state and not texto_original:
        texto_original = st.session_state.exemplo
        st.rerun()

with aba2:
    col1, col2, col3 = st.columns(3)
    with col1:
        assunto = st.selectbox("Assunto:", ["IPTU", "Links úteis", "Atendimento", "Prazos", "Documentos", "Serviços"])
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    with col3:
        publico = st.selectbox("Público:", ["Cidadãos", "Servidores", "Empresas", "Moradores", "Visitantes"])
    
    if st.button("✨ Criar Texto", type="primary", use_container_width=True):
        texto_criado = criar_texto(assunto, tom, publico)
        st.markdown("**📝 Texto criado**")
        st.success(texto_criado)
        
        st.markdown(f"""
        **🎯 Diretrizes aplicadas:**
        - **Voz:** simples, resolutiva e respeitosa
        - **Tom:** {tom}
        - **Público:** {publico}
        """)

st.divider()
st.caption("📌 Manual oficial: cms.sp.gov.br/cms/tomevoz/sobre")
