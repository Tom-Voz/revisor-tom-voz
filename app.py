import streamlit as st
import google.generativeai as genai

# Configurar a página
st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# Manual de tom e voz extraído do site
MANUAL = """
Voz do Governo de SP:
- Simples: usar linguagem clara, sem termos técnicos desnecessários
- Resolutiva: focar em resolver problemas e dar respostas práticas
- Respeitosa: tratar todas as pessoas com educação, sem informalidade excessiva
- Transparente: ser honesto e direto

Tom (varia conforme situação):
- Informativo: objetivo, com dados claros
- Empático: acolhedor, especialmente em situações difíceis
- Motivador: para engajar em eventos ou programas
- Direto: para mensagens de erro ou avisos importantes

Regras práticas:
- Use "você" para se dirigir ao leitor
- Prefira frases curtas
- Evite siglas sem explicação
- Seja inclusivo (linguagem neutra quando possível)
"""

# Configurar a chave API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Erro: Chave API não configurada. Configure nos secrets do Streamlit.")
    st.stop()

# Abas para as duas funcionalidades
aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    st.subheader("Revisão de Conteúdo")
    st.markdown("Cole um texto e ele será revisado seguindo o tom e voz do Governo de SP.")
    
    texto_original = st.text_area("Texto para revisar:", height=200)
    
    if st.button("Revisar Texto", type="primary"):
        if texto_original:
            with st.spinner("Revisando..."):
                prompt = f"""
                Você é um revisor de conteúdo do Governo de São Paulo.
                
                MANUAL DE TOM E VOZ:
                {MANUAL}
                
                PROCESSO DE REVISÃO:
                1. Expanda o texto com informações contextuais importantes
                2. Torne mais conciso (elimine redundâncias)
                3. Deixe mais dialógico (use "você", como se estivesse conversando)
                4. Simplifique a linguagem (termos mais comuns, frases mais curtas)
                
                TEXTO ORIGINAL:
                {texto_original}
                
                Responda APENAS com o texto revisado, sem explicações.
                """
                response = model.generate_content(prompt)
                st.markdown("### 📄 Texto Revisado")
                st.write(response.text)
        else:
            st.warning("Digite um texto para revisar.")

with aba2:
    st.subheader("Criação de Conteúdo")
    st.markdown("Descreva o que você quer criar e o tom desejado.")
    
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto do conteúdo:", placeholder="Ex: Prazo para pagamento de IPTU")
    with col2:
        tom = st.selectbox("Tom desejado:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    publico = st.text_input("Público-alvo:", placeholder="Ex: Contribuintes de São Paulo")
    detalhes = st.text_area("Detalhes adicionais:", height=100, placeholder="Informações importantes que devem ser incluídas...")
    
    if st.button("Criar Conteúdo", type="primary"):
        if assunto:
            with st.spinner("Criando..."):
                prompt = f"""
                Você é um redator do Governo de São Paulo.
                
                MANUAL DE TOM E VOZ:
                {MANUAL}
                
                Crie um conteúdo seguindo estas especificações:
                - Assunto: {assunto}
                - Tom: {tom}
                - Público-alvo: {publico}
                - Detalhes: {detalhes}
                
                Regras:
                - Use linguagem simples e acessível
                - Mantenha o tom {tom.lower()} durante todo o texto
                - Inclua um título curto
                - Texto deve ter entre 100 e 300 palavras
                
                Responda APENAS com o conteúdo criado, sem explicações.
                """
                response = model.generate_content(prompt)
                st.markdown("### ✨ Conteúdo Criado")
                st.write(response.text)
        else:
            st.warning("Digite o assunto do conteúdo.")
