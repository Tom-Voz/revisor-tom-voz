import streamlit as st
import re

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# Manual e regras
MANUAL = """
Voz do Governo de SP:
- Simples: linguagem clara, sem termos técnicos
- Resolutiva: foco em resolver problemas
- Respeitosa: tratar todos com educação
"""

def simplificar_texto(texto):
    """Função que aplica regras do manual ao texto"""
    
    # 1. Substituir linguagem formal
    texto = texto.replace("cidadão", "você")
    texto = texto.replace("o cidadão", "você")
    texto = texto.replace("a cidadã", "você")
    texto = texto.replace("os cidadãos", "vocês")
    texto = texto.replace("as cidadãs", "vocês")
    
    texto = texto.replace("deve efetuar", "pode fazer")
    texto = texto.replace("deverá", "pode")
    texto = texto.replace("deverão", "podem")
    
    texto = texto.replace("efetuar o pagamento", "pagar")
    texto = texto.replace("realizar o pagamento", "pagar")
    
    texto = texto.replace("preencha as informações", "preencha")
    texto = texto.replace("para gerar", "e gere")
    
    # 2. Tornar mais dialógico
    texto = texto.replace("colaboradores", "você e sua equipe")
    
    # 3. Simplificar frases longas
    if len(texto.split()) > 20 and "." in texto:
        # Se for muito longo, tenta quebrar
        partes = texto.split(". ")
        if len(partes) > 1:
            texto = ".\n\n".join(partes)
    
    # 4. Remover termos burocráticos
    termos_burocraticos = [
        ("a partir de", "com"),
        ("mediante", "com"),
        ("para que seja possível", "para"),
        ("no que se refere a", "sobre"),
    ]
    
    for termo, simplificado in termos_burocraticos:
        texto = texto.replace(termo, simplificado)
    
    return texto

def criar_texto(assunto, tom):
    """Cria um texto baseado no assunto e tom"""
    
    textos = {
        "iptu": "Você pode pagar o IPTU até o dia 10 de abril. Faça o pagamento pelo app ou no site da prefeitura.",
        "links": "Preencha os dados e gere os links úteis para sua equipe acessar pelo aplicativo.",
        "padrao": f"Você pode resolver seu assunto sobre {assunto} de forma simples e rápida. Acesse nossos canais digitais e tenha todas as informações que precisa."
    }
    
    for chave, texto_base in textos.items():
        if chave in assunto.lower():
            texto = texto_base
            break
    else:
        texto = textos["padrao"]
    
    if tom == "Empático":
        texto += " Estamos aqui para ajudar você!"
    elif tom == "Motivador":
        texto += " Vamos juntos construir uma São Paulo melhor!"
    
    return texto

# Interface
st.write("### 🟢 Sistema funcionando sem API")

opcao = st.radio("Escolha:", ["Revisar texto", "Criar texto"])

if opcao == "Revisar texto":
    texto_original = st.text_area("Texto para revisar:", height=150, 
                                   placeholder="Ex: O cidadão deve efetuar o pagamento do IPTU...")
    
    if st.button("Revisar", type="primary"):
        if texto_original:
            texto_revisado = simplificar_texto(texto_original)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📄 Original")
                st.write(texto_original)
            with col2:
                st.markdown("### ✅ Revisado")
                st.write(texto_revisado)
            
            st.success("Texto revisado seguindo o manual de tom e voz!")
        else:
            st.warning("Digite um texto para revisar.")

else:
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto:", placeholder="Ex: IPTU, links, atendimento")
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador"])
    
    if st.button("Criar", type="primary"):
        if assunto:
            texto_criado = criar_texto(assunto, tom)
            st.markdown("### ✨ Texto criado")
            st.write(texto_criado)
            st.info(f"Tom utilizado: {tom}")
        else:
            st.warning("Digite o assunto.")

# Explicação
with st.expander("📖 Como usar este sistema"):
    st.markdown("""
    **Revisar texto:** Cole um texto e o sistema aplicará automaticamente as regras do manual:
    - Substitui "cidadão" por "você"
    - Simplifica termos burocráticos
    - Torna a linguagem mais direta
    
    **Criar texto:** Digite um assunto e escolha o tom, e o sistema gera um texto seguindo as diretrizes.
    """)
