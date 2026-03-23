import streamlit as st
import re

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# ==================== MANUAL OFICIAL ====================
MANUAL_COMPLETO = """
Nossa Voz (sempre):
- Simples: linguagem clara, sem termos técnicos desnecessários
- Resolutiva: focar em resolver problemas do cidadão
- Respeitosa: tratar todos com educação, sem informalidade excessiva

Nosso Tom (varia):
- Informativo: objetivo, com dados claros
- Empático: acolhedor, para situações que exigem cuidado
- Motivador: empolga e engaja, para eventos e campanhas
- Direto: focado na ação, para mensagens de erro ou avisos

Processo de Edição (4 passos):
1. EXPANDIR: incluir contexto importante que o leitor precisa saber
2. CONCISAR: reduzir redundâncias e informações desnecessárias
3. DIALOGAR: usar "você" como se estivesse conversando
4. SIMPLIFICAR: substituir palavras complexas por termos comuns

Linguagem Inclusiva:
- Usar "pessoas" em vez de "homens"
- Evitar generalizações desnecessárias
"""

def aplicar_4_passos(texto):
    """Aplica os 4 passos do processo de edição do manual"""
    
    # PASSO 1: EXPANDIR (adicionar contexto quando necessário)
    if "IPTU" in texto and "Imposto" not in texto:
        # Expandir apenas se for primeira menção
        texto = texto.replace("IPTU", "IPTU (o imposto do seu imóvel)")
    
    # PASSO 2: CONCISAR (remover redundâncias)
    redundancias = [
        (r'efetuar o pagamento', 'pagar'),
        (r'realizar o pagamento', 'pagar'),
        (r'fazer o pagamento', 'pagar'),
        (r'de forma (mensal|anual|diária)', r'todo \1'),
        (r'é necessário que', ''),
        (r'para que seja possível', 'para'),
    ]
    for busca, substitui in redundancias:
        texto = re.sub(busca, substitui, texto, flags=re.IGNORECASE)
    
    # PASSO 3: DIALOGAR (usar "você")
    dialogos = [
        (r'o cidadão', 'você'),
        (r'a cidadã', 'você'),
        (r'os cidadãos', 'vocês'),
        (r'as cidadãs', 'vocês'),
        (r'contribuinte', 'você'),
        (r'os contribuintes', 'vocês'),
        (r'o usuário', 'você'),
        (r'os usuários', 'vocês'),
    ]
    for busca, substitui in dialogos:
        texto = re.sub(busca, substitui, texto, flags=re.IGNORECASE)
    
    # PASSO 4: SIMPLIFICAR (substituir termos complexos)
    simplificacoes = [
        (r'através de', 'pelo'),
        (r'por meio de', 'pelo'),
        (r'no que se refere a', 'sobre'),
        (r'a partir de', 'com'),
        (r'mediante', 'com'),
        (r'solicitar', 'pedir'),
        (r'efetuar', 'fazer'),
        (r'utilizar', 'usar'),
        (r'preencher as informações', 'preencher'),
        (r'mensalmente', 'todo mês'),
        (r'anualmente', 'todo ano'),
        (r'diariamente', 'todo dia'),
        (r'posteriormente', 'depois'),
        (r'anteriormente', 'antes'),
    ]
    for busca, substitui in simplificacoes:
        texto = re.sub(busca, substitui, texto, flags=re.IGNORECASE)
    
    return texto

def aplicar_tom(texto, tom):
    """Aplica o tom adequado conforme o manual"""
    
    if tom == "Empático":
        # Adicionar acolhimento
        if not any(p in texto for p in ["sabemos", "entendemos", "conte conosco"]):
            texto = texto.replace("Você", "Sabemos que você tem uma rotina corrida. Por isso, você")
            if not texto.endswith("."):
                texto += " Estamos aqui para ajudar."
    
    elif tom == "Motivador":
        # Adicionar entusiasmo
        if not any(p in texto for p in ["vamos", "juntos", "faça parte"]):
            texto = texto.replace("Você", "Vamos juntos! Você")
            texto += " Faça parte dessa transformação!"
    
    elif tom == "Direto":
        # Ser objetivo e focado na ação
        if not texto.startswith("Atenção:"):
            texto = f"Atenção: {texto[0].lower() + texto[1:] if texto else texto}"
    
    # Tom Informativo já é o padrão, mantém como está
    
    return texto

def revisar_texto(texto, tom="Informativo"):
    """Revisão completa seguindo o manual"""
    
    original = texto
    
    # Aplicar os 4 passos do processo de edição
    texto = aplicar_4_passos(texto)
    
    # Aplicar o tom adequado
    texto = aplicar_tom(texto, tom)
    
    # Correções finais
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # Garantir maiúscula no início
    if texto and texto[0].islower():
        texto = texto[0].upper() + texto[1:]
    
    # Garantir ponto final
    if texto and not texto[-1] in '.!?':
        texto += '.'
    
    return texto

def criar_texto(assunto, tom, publico):
    """Cria conteúdo seguindo voz, tom e processo de edição"""
    
    # Base de textos por assunto (já seguindo os 4 passos)
    base_textos = {
        "iptu": f"{publico}, você pode pagar o IPTU pelo app todo mês. É rápido e você não precisa sair de casa.",
        "links": f"Preencha os dados e gere os links úteis. Assim, {publico} acessam as informações pelo app de forma prática.",
        "atendimento": f"{publico} pode falar conosco pelo telefone 156, pelo chat ou pelo app. Escolha o melhor para você.",
        "prazo": f"Fique atento aos prazos, {publico}. Consulte as datas no nosso site ou app. Não deixe para última hora.",
        "documento": f"{publico}, você pode solicitar seus documentos pelo app. É simples: baixe, acesse e peça.",
        "servico": f"{publico}, você pode resolver esse serviço online. Acesse o app ou site e faça agora mesmo.",
    }
    
    # Escolher texto base
    assunto_lower = assunto.lower()
    texto = base_textos["servico"]
    for chave in base_textos:
        if chave in assunto_lower:
            texto = base_textos[chave]
            break
    
    # Aplicar o tom selecionado
    texto = aplicar_tom(texto, tom)
    
    # Pequenos ajustes de fluidez
    texto = texto.replace("  ", " ")
    
    return texto

# ==================== INTERFACE ====================
st.markdown("### 📖 Revisor e Criador de Conteúdo")
st.markdown("Baseado no manual oficial de tom e voz do Governo de SP")

with st.expander("📘 Ver manual completo"):
    st.markdown(MANUAL_COMPLETO)

aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    texto_original = st.text_area(
        "Texto para revisar:", 
        height=120,
        placeholder="Ex: O cidadão deve efetuar o pagamento do IPTU através do aplicativo mensalmente."
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
            st.session_state.exemplo = "O cidadão deve efetuar o pagamento do IPTU através do aplicativo mensalmente."
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
        - **Processo:** os 4 passos de edição foram considerados
        """)

st.divider()
st.caption("📌 Manual oficial: cms.sp.gov.br/cms/tomevoz/sobre | Processo de edição baseado em Torrey Podmajersky (2019)")
