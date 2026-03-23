import streamlit as st
import re

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# Manual oficial extraído do site
MANUAL = """
Nossa voz:
- Simples: linguagem clara, sem termos técnicos desnecessários
- Resolutiva: focar em resolver problemas do cidadão
- Respeitosa: tratar todos com educação, sem informalidade excessiva

Processo de edição (4 passos):
1. Expandir: incluir contexto importante
2. Conciso: reduzir redundâncias
3. Dialógico: usar "você" como se estivesse conversando
4. Simplificar: substituir ambiguidades por termos conhecidos
"""

def revisar_texto(texto):
    """Aplica o processo de edição do manual"""
    
    # PASSO 1: Expandir com contexto (se necessário)
    if "IPTU" in texto and "prazo" not in texto.lower():
        texto = texto.replace("IPTU", "IPTU (Imposto sobre a Propriedade Predial e Territorial Urbana)")
    
    # PASSO 2: Tornar mais conciso
    texto = re.sub(r'efetuar o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'realizar o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'deverá ser feito', 'deve ser feito', texto, flags=re.IGNORECASE)
    texto = re.sub(r'no que se refere a', 'sobre', texto, flags=re.IGNORECASE)
    texto = re.sub(r'a partir de', 'com', texto, flags=re.IGNORECASE)
    
    # PASSO 3: Tornar dialógico (usar "você")
    texto = re.sub(r'o cidadão', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'a cidadã', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'os cidadãos', 'vocês', texto, flags=re.IGNORECASE)
    texto = re.sub(r'as cidadãs', 'vocês', texto, flags=re.IGNORECASE)
    texto = re.sub(r'contribuinte', 'você', texto, flags=re.IGNORECASE)
    
    # Adicionar tom dialógico
    if "pagar" in texto.lower():
        texto = texto.replace("pagar", "pagar (é rápido e fácil)")
    
    # PASSO 4: Simplificar
    simplificacoes = {
        r'preencha as informações necessárias': 'preencha os dados',
        r'para que seja possível gerar': 'para gerar',
        r'através do aplicativo': 'pelo app',
        r'colaboradores acessarem': 'você e sua equipe acessarem',
        r'mensalmente': 'todo mês',
        r'anualmente': 'todo ano',
    }
    
    for complexo, simples in simplificacoes.items():
        texto = re.sub(complexo, simples, texto, flags=re.IGNORECASE)
    
    # Melhorar legibilidade
    if len(texto) > 300:
        # Quebrar em parágrafos
        texto = texto.replace(". ", ".\n\n")
    
    return texto.strip()

def criar_texto(assunto, tom, publico):
    """Cria conteúdo seguindo o manual"""
    
    # Base do texto conforme assunto
    textos_base = {
        "iptu": f"Você pode pagar o IPTU todo mês de forma simples e rápida. Faça isso pelo app ou no site da prefeitura, sem sair de casa.",
        "links": f"Preencha os dados abaixo e gere os links úteis. Assim, {publico} acessam as informações pelo app de forma prática.",
        "atendimento": f"Precisa de ajuda? {publico} pode falar conosco pelo telefone, chat ou app. Estamos aqui para resolver seu problema.",
        "prazo": f"Fique atento aos prazos! {publico} pode consultar as datas no nosso site ou app. Não deixe para última hora.",
    }
    
    # Escolher texto base
    texto = textos_base.get("iptu")
    for chave in textos_base:
        if chave in assunto.lower():
            texto = textos_base[chave]
            break
    
    # Aplicar tom
    if tom == "Empático":
        texto += f" Sabemos que {publico.lower()} tem uma rotina corrida, por isso buscamos facilitar ao máximo."
    elif tom == "Motivador":
        texto += f" Vamos juntos! Com {publico.lower()} participando, construímos uma São Paulo melhor."
    elif tom == "Direto":
        texto = f"⚠️ Atenção: {texto}"
    
    # Garantir que usou "você" se o público for genérico
    if publico == "Cidadãos de São Paulo":
        texto = texto.replace(publico, "você")
    
    return texto

# Interface
st.write("### 📖 Manual de Tom e Voz carregado")
with st.expander("Ver manual completo"):
    st.markdown(MANUAL)

opcao = st.radio("Funcionalidade:", ["✏️ Revisar texto", "✨ Criar texto"], horizontal=True)

if opcao == "✏️ Revisar texto":
    st.subheader("Revisão de Conteúdo")
    st.markdown("Cole um texto e ele será revisado seguindo os **4 passos do manual**")
    
    texto_original = st.text_area("Texto para revisar:", height=150, 
                                   placeholder="Ex: O cidadão deve efetuar o pagamento do IPTU através do aplicativo mensalmente.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Revisar", type="primary", use_container_width=True):
            if texto_original:
                with st.spinner("Aplicando processo de edição..."):
                    texto_revisado = revisar_texto(texto_original)
                    
                    st.markdown("### 📄 Texto Original")
                    st.info(texto_original)
                    
                    st.markdown("### ✅ Texto Revisado")
                    st.success(texto_revisado)
                    
                    st.markdown("#### 📋 Passos aplicados:")
                    st.markdown("""
                    - ✅ **Expandir:** Adicionado contexto quando necessário
                    - ✅ **Conciso:** Simplificados termos burocráticos
                    - ✅ **Dialógico:** Usado "você" para conversar com o leitor
                    - ✅ **Simplificar:** Substituídos termos complexos
                    """)
            else:
                st.warning("Digite um texto para revisar.")
    
    with col2:
        if texto_original:
            if st.button("📋 Exemplo", use_container_width=True):
                st.session_state.exemplo = "O cidadão deve efetuar o pagamento do IPTU através do aplicativo mensalmente."
                st.rerun()

else:
    st.subheader("Criação de Conteúdo")
    st.markdown("Descreva o que você quer criar e escolha o tom adequado")
    
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto:", placeholder="Ex: IPTU, links úteis, atendimento, prazos")
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    publico = st.text_input("Público-alvo:", value="Cidadãos de São Paulo", 
                            placeholder="Ex: Contribuintes, servidores, moradores")
    
    if st.button("✨ Criar conteúdo", type="primary", use_container_width=True):
        if assunto:
            with st.spinner("Criando conteúdo seguindo o manual..."):
                texto_criado = criar_texto(assunto, tom, publico)
                
                st.markdown("### 📝 Conteúdo Criado")
                st.success(texto_criado)
                
                st.markdown("#### 🎯 Diretrizes aplicadas:")
                st.markdown(f"""
                - **Voz:** Simples, resolutiva e respeitosa
                - **Tom:** {tom}
                - **Público:** {publico}
                - **Linguagem:** Dialógica e acessível
                """)
        else:
            st.warning("Digite o assunto do conteúdo.")

# Rodapé
st.divider()
st.caption("📌 Baseado no manual oficial: https://cms.sp.gov.br/cms/tomevoz/sobre")
