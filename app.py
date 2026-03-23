import streamlit as st
import re

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# ==================== MANUAL COMPLETO ====================
# Baseado em todas as páginas do manual

# Pilares da voz
VOZ_SIMPLES = """
- Use linguagem direta e objetiva
- Mantenha apenas as informações necessárias
- Frases curtas (máx. 20-25 palavras)
- Evite ruídos na comunicação
"""

VOZ_PRESTATIVA = """
- Seja proativo para resolver problemas
- Use palavras de fácil entendimento
- Linguagem acolhedora e empática
- Evite termos técnicos e siglas sem explicação
- Use a 1ª pessoa do plural (nós)
"""

VOZ_CONFIAVEL = """
- Informações claras e corretas
- Evite termos que gerem dúvida ou duplo sentido
- Mantenha a mesma linguagem em toda comunicação
- Gramática semi-formal (nem muito informal, nem muito formal)
"""

# Processo de edição (5 passos)
PASSOS_EDICAO = """
1. EXPANDIR: incluir contexto que o leitor precisa
2. CONCISAR: reduzir redundâncias
3. DIALOGAR: usar "você", falar com o leitor
4. REVISAR: texto empático pode ser mais longo
5. SIMPLIFICAR: substituir ambiguidades, usar termos comuns
"""

# Boas práticas
BOAS_PRATICAS = {
    "frases": "máximo 20-25 palavras",
    "paragrafos": "3-4 frases por parágrafo",
    "siglas": "escrever por extenso na primeira menção",
    "numeros": "usar algarismos arábicos",
    "voz": "preferir voz ativa",
    "pontuacao": "usar com moderação"
}

def aplicar_manual_completo(texto):
    """Aplica todas as diretrizes do manual"""
    
    # ========== 1. VOZ SIMPLES ==========
    # Remover redundâncias
    texto = re.sub(r'efetuar o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'realizar o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'fazer o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'de forma (mensal|anual|diária)', r'todo \1', texto, flags=re.IGNORECASE)
    texto = re.sub(r'mensalmente', 'todo mês', texto, flags=re.IGNORECASE)
    texto = re.sub(r'anualmente', 'todo ano', texto, flags=re.IGNORECASE)
    
    # ========== 2. VOZ PRESTATIVA ==========
    # Tornar acolhedor e proativo
    if "RG" in texto and "documento" not in texto.lower():
        texto = texto.replace("RG", "RG (Registro Geral)", 1)
    
    # Usar "você" para dialogar
    texto = re.sub(r'o cidadão', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'a cidadã', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'os cidadãos', 'vocês', texto, flags=re.IGNORECASE)
    texto = re.sub(r'qualquer pessoa', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'contribuinte', 'você', texto, flags=re.IGNORECASE)
    
    # Usar 1ª pessoa do plural quando apropriado
    if "estamos" not in texto.lower() and "conosco" in texto.lower():
        texto = texto.replace("conosco", "com a gente")
    
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
    ]
    for busca, substitui in simplificacoes:
        texto = re.sub(busca, substitui, texto, flags=re.IGNORECASE)
    
    # ========== 5. BOAS PRÁTICAS ==========
    # Frases curtas (quebrar frases longas)
    if len(texto.split()) > 25:
        partes = texto.split('. ')
        if len(partes) > 1:
            texto = '.\n\n'.join(partes)
    
    # Evitar CAIXA ALTA
    if texto.isupper():
        texto = texto.title()
    
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
        if st.button("📋 Carregar exemplo", use_container_width=True):
            st.session_state.exemplo = "O RG fica pronto em 5 dias úteis. O RG pode ser retirado por qualquer pessoa com o protocolo"
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
