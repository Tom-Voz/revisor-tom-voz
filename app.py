import streamlit as st
import re

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

MANUAL = """
Nossa voz:
- Simples: linguagem clara, sem termos técnicos
- Resolutiva: foco em resolver problemas
- Respeitosa: tratar todos com educação

Nosso tom:
- Varia conforme situação (informativo, empático, motivador, direto)
"""

def revisar_texto(texto):
    """Revisão natural seguindo o manual"""
    
    # 1. Substituir "cidadão" por "você" (torna dialógico)
    texto = re.sub(r'\b(o cidadão|a cidadã|os cidadãos|as cidadãs)\b', 'você', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bcontribuinte\b', 'você', texto, flags=re.IGNORECASE)
    
    # 2. Simplificar verbos burocráticos
    texto = re.sub(r'efetuar o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'realizar o pagamento', 'pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'dar entrada', 'solicitar', texto, flags=re.IGNORECASE)
    
    # 3. Simplificar preposições e termos
    texto = re.sub(r'através de', 'pelo', texto, flags=re.IGNORECASE)
    texto = re.sub(r'no que se refere a', 'sobre', texto, flags=re.IGNORECASE)
    texto = re.sub(r'de forma (mensal|anual|diária)', r'todo \1', texto, flags=re.IGNORECASE)
    texto = re.sub(r'mensalmente', 'todo mês', texto, flags=re.IGNORECASE)
    texto = re.sub(r'anualmente', 'todo ano', texto, flags=re.IGNORECASE)
    
    # 4. Melhorar a fluidez
    texto = re.sub(r'deve pagar', 'pode pagar', texto, flags=re.IGNORECASE)
    texto = re.sub(r'é necessário que', '', texto, flags=re.IGNORECASE)
    
    # 5. Ajustar espaços extras
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # 6. Garantir que terminou com ponto
    if not texto.endswith('.'):
        texto += '.'
    
    return texto

def criar_texto(assunto, tom, publico):
    """Cria conteúdo natural seguindo o manual"""
    
    # Mapeamento de textos por assunto
    if 'iptu' in assunto.lower():
        if tom == "Empático":
            texto = f"Sabemos que sua rotina é corrida. Por isso, você pode pagar o IPTU pelo app, sem sair de casa. É rápido e seguro."
        elif tom == "Direto":
            texto = f"Atenção: o prazo para pagar o IPTU está chegando. Use o app e evite multas."
        else:  # Informativo ou Motivador
            texto = f"Você pode pagar o IPTU todo mês pelo aplicativo. É simples: baixe o app, acesse com seu CPF e faça o pagamento."
    
    elif 'link' in assunto.lower() or 'úteis' in assunto.lower():
        texto = f"Preencha os dados abaixo para gerar os links úteis. Assim, {publico.lower()} acessam as informações pelo app de forma prática."
    
    elif 'atendimento' in assunto.lower():
        texto = f"Precisa de ajuda? {publico} pode falar conosco pelo telefone 156, pelo chat no site ou pelo aplicativo. Estamos aqui para resolver seu problema."
    
    elif 'prazo' in assunto.lower():
        texto = f"Fique atento aos prazos! Consulte as datas no nosso site ou app. Assim você não perde nenhum prazo importante."
    
    else:
        texto = f"{publico}, você pode resolver suas pendências de forma simples. Acesse nossos canais digitais e tenha todas as informações que precisa."
    
    # Ajustes finais conforme o tom
    if tom == "Motivador" and "IPTU" not in assunto:
        texto += " Vamos juntos construir uma São Paulo melhor!"
    elif tom == "Empático" and "IPTU" not in assunto:
        texto += " Conte com a gente para ajudar você."
    
    return texto

# Interface
st.write("### 📖 Manual carregado")

opcao = st.radio("Funcionalidade:", ["✏️ Revisar texto", "✨ Criar texto"], horizontal=True)

if opcao == "✏️ Revisar texto":
    st.subheader("Revisão de Conteúdo")
    
    texto_original = st.text_area("Texto para revisar:", height=120, 
                                   placeholder="Ex: O cidadão deve efetuar o pagamento do IPTU através do aplicativo mensalmente.")
    
    if st.button("Revisar texto", type="primary"):
        if texto_original:
            texto_revisado = revisar_texto(texto_original)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original**")
                st.info(texto_original)
            with col2:
                st.markdown("**Revisado**")
                st.success(texto_revisado)
        else:
            st.warning("Digite um texto para revisar.")

else:
    st.subheader("Criação de Conteúdo")
    
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto:", placeholder="Ex: IPTU, links úteis, atendimento")
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    publico = st.text_input("Público-alvo:", value="Cidadãos")
    
    if st.button("Criar conteúdo", type="primary"):
        if assunto:
            texto_criado = criar_texto(assunto, tom, publico)
            st.markdown("**Conteúdo criado**")
            st.success(texto_criado)
        else:
            st.warning("Digite o assunto.")
