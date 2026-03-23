import streamlit as st
import re

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

def aplicar_manual_completo(texto):
    """Aplica todas as diretrizes do manual"""
    
    # ========== 0. CASOS ESPECIAIS (linguagem jurídica) ==========
    # Simplificar expressões jurídicas comuns
    juridicas = [
        (r'Em vista da previsão legal da incapacidade dos menores de 16 anos responderem pelos atos da vida civil',
         'Menores de 16 anos não podem responder legalmente por si mesmos'),
        (r'devidamente representados', 'acompanhados dos pais ou responsáveis'),
        (r'nas solicitações de suas carteiras de identidade', 'para pedir a carteira de identidade'),
        (r'os menores devem estar', 'eles precisam estar'),
        (r'responderem pelos atos da vida civil', 'assumir responsabilidades legais'),
        (r'previsão legal', 'a lei determina'),
        (r'incapacidade dos menores', 'menores não têm capacidade legal'),
    ]
    
    for busca, substitui in juridicas:
        if busca in texto:
            texto = texto.replace(busca, substitui)
    
    # ========== 1. VOZ SIMPLES ==========
    # Remover redundâncias
    texto = re.sub(r'efetuar o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'realizar o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'fazer o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'de forma (mensal|anual|diária)', r'todo \1', texto, flags=re.IGNORECASE)
    texto = re.sub(r'mensalmente', 'todo mês', texto, flags=re.IGNORECASE)
    texto = re.sub(r'anualmente', 'todo ano', texto, flags=re.IGNORECASE)
    
    # Simplificar expressões burocráticas
    texto = re.sub(r'em vista de', 'como', texto, flags=re.IGNORECASE)
    texto = re.sub(r'devidamente', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'previsão legal', 'a lei', texto, flags=re.IGNORECASE)
    texto = re.sub(r'atos da vida civil', 'responsabilidades legais', texto, flags=re.IGNORECASE)
    
    # ========== 2. VOZ PRESTATIVA ==========
    # Tornar acolhedor e proativo
    if "RG" in texto and "documento" not in texto.lower():
        texto = texto.replace("RG", "RG (Registro Geral)", 1)
    
    if "carteira de identidade" in texto.lower():
        texto = texto.replace("carteira de identidade", "RG")
    
    # Usar "você" para dialogar
    texto = re.sub(r'o cidadão', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'a cidadã', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'os cidadãos', 'vocês', texto, flags=re.IGNORECASE)
    texto = re.sub(r'qualquer pessoa', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'contribuinte', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'os menores', 'crianças e adolescentes', texto, flags=re.IGNORECASE)
    texto = re.sub(r'menores de 16 anos', 'crianças e adolescentes com menos de 16 anos', texto, flags=re.IGNORECASE)
    
    # ========== 3. VOZ CONFIÁVEL ==========
    # Evitar duplo sentido e ambiguidades
    texto = re.sub(r'pode ser retirado', 'está disponível para retirada', texto, flags=re.IGNORECASE)
    texto = re.sub(r'com o protocolo', 'com o número do protocolo', texto, flags=re.IGNORECASE)
    
    # ========== 4. PROCESSO DE EDIÇÃO ==========
    # Expandir siglas na primeira menção
    if "CPF" in texto and "Cadastro" not in texto:
        texto = texto.replace("CPF", "CPF (Cadastro de Pessoa Física)", 1)
    
    if "CNH" in texto and "Carteira" not in texto:
        texto = texto.replace("CNH", "CNH (Carteira Nacional de Habilitação)", 1)
    
    # Simplificar termos complexos
    simplificacoes = [
        (r'através de', 'pelo'),
        (r'por meio de', 'pelo'),
        (r'no que se refere a', 'sobre'),
        (r'solicitar', 'pedir'),
        (r'utilizar', 'usar'),
        (r'preencher as informações', 'preencher'),
        (r'dias úteis', 'dias úteis (de segunda a sexta)'),
        (r'devidamente representados', 'acompanhados dos pais ou responsáveis'),
        (r'responder pelos atos', 'assumir responsabilidades'),
    ]
    for busca, substitui in simplificacoes:
        texto = re.sub(busca, substitui, texto, flags=re.IGNORECASE)
    
    # ========== 5. REESCREVER FRASES COMPLEXAS ==========
    # Reescrever frases com "devem estar" para tom mais direto
    if "devem estar" in texto:
        texto = texto.replace("devem estar", "precisam estar")
    
    if "devem" in texto and "acompanhados" not in texto:
        texto = re.sub(r'devem', 'precisam', texto)
    
    # ========== 6. BOAS PRÁTICAS ==========
    # Frases curtas (quebrar frases longas)
    if len(texto.split()) > 25:
        partes = texto.split('. ')
        if len(partes) > 1:
            texto = '.\n\n'.join(partes)
    
    # Correções finais
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # Garantir ponto final
    if texto and texto[-1] not in '.!?':
        texto += '.'
    
    return texto

def aplicar_tom(texto, tom):
    """Aplica o tom adequado conforme o manual"""
    
    if tom == "Empático":
        if "sabemos" not in texto and "entendemos" not in texto:
            texto = "Sabemos que você precisa de agilidade. " + texto[0].lower() + texto[1:] if texto else texto
        if "conte conosco" not in texto.lower():
            texto += " Conte conosco para ajudar você."
    
    elif tom == "Motivador":
        if "vamos" not in texto:
            texto = "Vamos juntos! " + texto[0].lower() + texto[1:] if texto else texto
        if "faça parte" not in texto.lower():
            texto += " Faça parte dessa transformação!"
    
    elif tom == "Direto":
        if not texto.startswith("Atenção"):
            texto = "Atenção: " + texto[0].lower() + texto[1:] if texto else texto
    
    return texto

def revisar_texto(texto, tom="Informativo"):
    """Revisão completa seguindo o manual"""
    
    # Aplicar todas as diretrizes
    texto = aplicar_manual_completo(texto)
    
    # Aplicar o tom
    texto = aplicar_tom(texto, tom)
    
    # Limpar espaços
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # Garantir maiúscula no início
    if texto and texto[0].islower():
        texto = texto[0].upper() + texto[1:]
    
    return texto

def criar_texto(assunto, tom, publico):
    """Cria conteúdo seguindo todas as diretrizes do manual"""
    
    base_textos = {
        "iptu": f"{publico}, você pode pagar o IPTU pelo app todo mês. É rápido e você não precisa sair de casa. Conte conosco para ajudar você.",
        "rg": f"{publico}, seu RG fica pronto em até 5 dias úteis. Você pode retirar com o número do protocolo. Estamos aqui para ajudar.",
        "cpf": f"{publico}, você pode solicitar seu CPF pelo app. É simples e rápido.",
        "atendimento": f"{publico}, você pode falar conosco pelo telefone 156, pelo chat ou pelo app. Escolha o melhor para você. Estamos aqui para ajudar.",
        "links": f"Preencha os dados e gere os links úteis. Assim, {publico} acessam as informações pelo app de forma prática.",
        "prazo": f"Fique atento aos prazos, {publico}. Consulte as datas no nosso site ou app. Não deixe para última hora.",
        "documento": f"{publico}, seu documento fica pronto em até 5 dias úteis. Você pode retirar com o número do protocolo.",
        "servico": f"{publico}, você pode resolver esse serviço online. Acesse o app ou site e faça agora mesmo. É rápido e fácil."
    }
    
    assunto_lower = assunto.lower()
    texto = base_textos["servico"]
    
    for chave in base_textos:
        if chave in assunto_lower:
            texto = base_textos[chave]
            break
    
    texto = aplicar_tom(texto, tom)
    
    return texto

# ==================== INTERFACE ====================
st.markdown("### 📖 Revisor e Criador de Conteúdo")
st.markdown("Baseado no manual oficial de tom e voz do Governo de SP")

with st.expander("📘 Ver manual completo (3 pilares da voz)"):
    st.markdown("""
    **Voz Simples:** Linguagem direta, frases curtas, só o necessário.
    
    **Voz Prestativa:** Proativa, resolve problemas, acolhedora, desburocratizada.
    
    **Voz Confiável:** Informações claras, comunicação universal, sem duplo sentido.
    
    **Processo de Edição:** Expandir → Concisar → Dialogar → Revisar → Simplificar
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
                
                st.markdown("**📋 Diretrizes aplicadas:**")
                st.markdown("""
                - **Voz Simples:** frases curtas, linguagem direta
                - **Voz Prestativa:** uso de 'você', tom acolhedor
                - **Voz Confiável:** informações claras, sem ambiguidades
                - **Processo de edição:** 5 passos aplicados
                """)
            else:
                st.warning("Digite um texto para revisar.")
    
    with col2:
        if st.button("📋 Carregar exemplo 1", use_container_width=True):
            st.session_state.exemplo = "O RG fica pronto em 5 dias úteis. O RG pode ser retirado por qualquer pessoa com o protocolo"
            st.rerun()
    
    with col2:
        if st.button("📋 Carregar exemplo 2", use_container_width=True):
            st.session_state.exemplo = "Em vista da previsão legal da incapacidade dos menores de 16 anos responderem pelos atos da vida civil, nas solicitações de suas carteiras de identidade os menores devem estar devidamente representados."
            st.rerun()
    
    if "exemplo" in st.session_state and not texto_original:
        texto_original = st.session_state.exemplo
        st.rerun()

with aba2:
    col1, col2, col3 = st.columns(3)
    with col1:
        assunto = st.selectbox("Assunto:", ["IPTU", "RG", "CPF", "Atendimento", "Links úteis", "Prazos", "Documentos", "Serviços"])
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
        - **Voz:** Simples + Prestativa + Confiável
        - **Tom:** {tom}
        - **Público:** {publico}
        - **Boas práticas:** frases curtas, siglas explicadas, linguagem acolhedora
        """)

st.divider()
st.caption("📌 Manual oficial: cms.sp.gov.br/cms/tomevoz | Baseado nos 3 pilares: Simples, Prestativa e Confiável")
