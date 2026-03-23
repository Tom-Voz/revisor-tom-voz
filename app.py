import streamlit as st
import re

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# Dicionário de substituições inteligentes
SUBSTITUICOES = [
    # Sujeitos
    (r'\bo cidadão\b', 'você'),
    (r'\ba cidadã\b', 'você'),
    (r'\bos cidadãos\b', 'vocês'),
    (r'\bas cidadãs\b', 'vocês'),
    (r'\bcontribuinte\b', 'você'),
    (r'\bos contribuintes\b', 'vocês'),
    
    # Verbos
    (r'efetuar o pagamento', 'pagar'),
    (r'realizar o pagamento', 'pagar'),
    (r'fazer o pagamento', 'pagar'),
    (r'dar entrada', 'solicitar'),
    (r'deverá ser feito', 'deve ser feito'),
    (r'é necessário que', ''),
    
    # Preposições
    (r'através de', 'pelo'),
    (r'por meio de', 'pelo'),
    (r'no que se refere a', 'sobre'),
    (r'a partir de', 'a partir de'),
    
    # Advérbios
    (r'mensalmente', 'todo mês'),
    (r'anualmente', 'todo ano'),
    (r'semanalmente', 'toda semana'),
    (r'diariamente', 'todo dia'),
]

def revisar_texto(texto):
    """Revisa o texto com regras inteligentes"""
    texto_original = texto
    
    # Aplicar todas as substituições
    for busca, substituicao in SUBSTITUICOES:
        texto = re.sub(busca, substituicao, texto, flags=re.IGNORECASE)
    
    # Casos especiais que precisam de contexto
    if "pagar" in texto.lower() and "IPTU" in texto:
        texto = texto.replace("pagar", "pagar o IPTU")
    
    # Limpar espaços duplicados
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # Remover artigos duplicados
    texto = re.sub(r'pagar o o IPTU', 'pagar o IPTU', texto)
    texto = re.sub(r'pagar do IPTU', 'pagar o IPTU', texto)
    
    # Garantir pontuação correta
    if not texto.endswith(('.', '!', '?')):
        texto += '.'
    
    return texto

def criar_texto(assunto, tom, publico):
    """Cria textos naturais baseados no assunto"""
    
    textos = {
        "iptu": {
            "informativo": f"{publico}, você pode pagar o IPTU pelo app todo mês. É rápido e seguro.",
            "empatico": f"Sabemos que sua rotina é corrida. Por isso, você pode pagar o IPTU pelo app, sem sair de casa.",
            "motivador": f"Faça sua parte com facilidade! Pague o IPTU pelo app e ajude a construir uma São Paulo melhor.",
            "direto": f"Atenção: pague o IPTU pelo app. Evite multas e fique em dia."
        },
        "link": {
            "informativo": f"Preencha os dados abaixo e gere os links úteis. Assim, {publico.lower()} acessam as informações pelo app.",
            "empatico": f"Quer facilitar o dia a dia da sua equipe? Preencha os dados e gere os links úteis para o app.",
            "motivador": f"Vamos facilitar! Gere os links úteis e ajude {publico.lower()} a acessar as informações rapidamente.",
            "direto": f"Preencha os dados. Gere os links. {publico} acessam pelo app."
        },
        "atendimento": {
            "informativo": f"{publico} pode falar com a gente pelo telefone 156, chat ou app. Escolha o melhor para você.",
            "empatico": f"Precisa de ajuda? Estamos aqui. Ligue 156, use o chat ou o app. Qualquer dúvida, conte conosco.",
            "motivador": f"Atendimento fácil e rápido! Fale conosco pelo 156, chat ou app. Estamos prontos para ajudar você.",
            "direto": f"Atendimento: Ligue 156, acesse o chat ou o app. Escolha o canal mais rápido."
        }
    }
    
    # Identificar assunto
    assunto_lower = assunto.lower()
    categoria = "iptu"  # padrão
    
    if "link" in assunto_lower or "útil" in assunto_lower:
        categoria = "link"
    elif "atendimento" in assunto_lower or "contato" in assunto_lower or "ajuda" in assunto_lower:
        categoria = "atendimento"
    
    # Buscar tom
    tom_key = tom.lower()
    if tom_key not in ["informativo", "empatico", "motivador", "direto"]:
        tom_key = "informativo"
    
    # Retornar texto
    texto_base = textos.get(categoria, textos["iptu"]).get(tom_key, textos["iptu"]["informativo"])
    
    # Substituir placeholders
    texto_base = texto_base.replace("{publico}", publico)
    
    return texto_base

# Interface
st.markdown("### 📖 Sistema de Revisão e Criação de Conteúdo")
st.markdown("Baseado no manual oficial de tom e voz do Governo de SP")

aba1, aba2 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto"])

with aba1:
    st.markdown("Cole um texto e o sistema vai aplicar as regras do manual:")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        exemplo = st.checkbox("Usar exemplo")
    
    texto_input = ""
    if exemplo:
        texto_input = "O cidadão deve efetuar o pagamento do IPTU através do aplicativo mensalmente."
    
    texto_original = st.text_area("Texto original:", value=texto_input, height=120)
    
    if st.button("Revisar Texto", type="primary"):
        if texto_original:
            texto_revisado = revisar_texto(texto_original)
            
            col_orig, col_rev = st.columns(2)
            with col_orig:
                st.markdown("**📄 Original**")
                st.info(texto_original)
            with col_rev:
                st.markdown("**✅ Revisado**")
                st.success(texto_revisado)
            
            st.markdown("**Regras aplicadas:**")
            st.markdown("""
            - ✅ "cidadão" → "você" (torna dialógico)
            - ✅ "efetuar o pagamento" → "pagar" (simplifica)
            - ✅ "através de" → "pelo" (simplifica)
            - ✅ "mensalmente" → "todo mês" (linguagem simples)
            """)
        else:
            st.warning("Digite ou cole um texto para revisar.")

with aba2:
    st.markdown("Descreva o que você quer criar:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        assunto = st.selectbox("Assunto:", ["IPTU", "Links úteis", "Atendimento", "Outro"])
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    with col3:
        publico = st.selectbox("Público:", ["Cidadãos", "Servidores", "Empresas", "Visitantes"])
    
    if assunto == "Outro":
        assunto_outro = st.text_input("Descreva o assunto:")
    else:
        assunto_outro = assunto
    
    if st.button("Criar Texto", type="primary"):
        if assunto_outro:
            texto_criado = criar_texto(assunto_outro, tom, publico)
            st.markdown("**✨ Texto criado**")
            st.success(texto_criado)
            
            st.markdown(f"**Diretrizes:** Voz simples, resolutiva e respeitosa | Tom: {tom} | Público: {publico}")
        else:
            st.warning("Digite o assunto do texto.")

st.divider()
st.caption("📌 Baseado no manual oficial: cms.sp.gov.br/cms/tomevoz/sobre")
