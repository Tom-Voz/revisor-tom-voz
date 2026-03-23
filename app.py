import streamlit as st
import requests
import json
import sqlite3
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Revisor de Tom e Voz", page_icon="📝")
st.title("📝 Revisor e Criador de Conteúdo")
st.caption("Seguindo o manual de tom e voz do Governo de SP")

# ==================== MANUAL DE TOM E VOZ ====================
MANUAL = """
Você é um especialista em comunicação do Governo de São Paulo.

Nossa voz:
- Simples: linguagem clara, frases curtas, só o necessário
- Prestativa: proativa, resolve problemas, acolhedora
- Confiável: informações corretas, sem ambiguidades

Regras:
- Use "você" em vez de "o cidadão"
- Use "pagar" em vez de "efetuar pagamento"
- Use "pelo" em vez de "através de"
- Use "todo mês" em vez de "mensalmente"
- Frases curtas e diretas
- Seja acolhedor quando apropriado
"""

# ==================== CONFIGURAÇÃO DO BANCO DE DADOS ====================
def init_db():
    """Inicializa o banco de dados SQLite"""
    conn = sqlite3.connect('revisoes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS revisoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto_original TEXT,
            texto_revisado TEXT,
            contexto TEXT,
            data TEXT,
            aprovada INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def salvar_revisao(original, revisado, contexto=""):
    """Salva uma revisão no banco de dados"""
    try:
        conn = sqlite3.connect('revisoes.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO revisoes (texto_original, texto_revisado, contexto, data)
            VALUES (?, ?, ?, ?)
        ''', (original, revisado, contexto, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

def listar_revisoes():
    """Lista as revisões salvas"""
    try:
        conn = sqlite3.connect('revisoes.db')
        df = pd.read_sql_query("SELECT * FROM revisoes ORDER BY data DESC", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

def get_insights():
    """Gera insights a partir das revisões salvas"""
    df = listar_revisoes()
    if df.empty:
        return None
    
    # Contar revisões
    total = len(df)
    ultima_semana = len(df[df['data'] > (datetime.now().isoformat().split('T')[0])])
    
    # Padrões simples
    palavras_comuns = []
    for texto in df['texto_original'].head(20):
        palavras_comuns.extend(texto.lower().split()[:5])
    
    return {
        "total": total,
        "ultima_semana": ultima_semana,
        "palavras_comuns": palavras_comuns[:10]
    }

# ==================== FUNÇÃO DE IA (GROQ) ====================
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("Configure a chave API GROQ_API_KEY em Settings → Secrets")
    st.stop()

API_URL = "https://api.groq.com/openai/v1/chat/completions"

def chamar_groq(prompt, contexto_extra=""):
    """Chama a API do Groq com contexto extra"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Montar mensagem com contexto
    mensagem = MANUAL
    if contexto_extra:
        mensagem += f"\n\nInformação adicional sobre o canal/público: {contexto_extra}"
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": mensagem},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            resultado = response.json()
            return resultado["choices"][0]["message"]["content"]
        else:
            return None
    except Exception as e:
        return None

# ==================== INTERFACE ====================
# Inicializar banco de dados
init_db()

# Remover diagnóstico - mostrar apenas status sucinto
st.success("✅ Sistema pronto")

aba1, aba2, aba3 = st.tabs(["✏️ Revisar Texto", "✨ Criar Texto", "📊 Aprendizado"])

with aba1:
    st.subheader("Revisão de Conteúdo")
    
    texto_original = st.text_area("Texto para revisar:", height=120)
    
    # Campo de contexto extra
    with st.expander("➕ Contexto adicional (opcional)"):
        contexto = st.text_area(
            "Informe o canal, público ou situação:",
            height=80,
            placeholder="Ex: Post para Instagram, público jovem, mensagem de erro no app..."
        )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Revisar", type="primary"):
            if texto_original:
                with st.spinner("Revisando com IA..."):
                    prompt = f"Revise este texto seguindo as regras. Mantenha o sentido original. Responda APENAS com o texto revisado.\n\nTEXTO: {texto_original}"
                    resultado = chamar_groq(prompt, contexto)
                    
                    if resultado:
                        st.markdown("**📄 Original**")
                        st.info(texto_original)
                        
                        st.markdown("**✅ Revisado**")
                        st.success(resultado)
                        
                        # Salvar revisão para aprendizado
                        if salvar_revisao(texto_original, resultado, contexto):
                            st.caption("💾 Revisão salva para aprendizado")
                    else:
                        st.error("Erro ao revisar. Tente novamente.")
            else:
                st.warning("Digite um texto para revisar")

with aba2:
    st.subheader("Criação de Conteúdo")
    
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto:", placeholder="Ex: Prazo do IPTU")
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
    # Campo de contexto extra
    with st.expander("➕ Contexto adicional (opcional)"):
        contexto_criacao = st.text_area(
            "Informe o canal, público ou situação:",
            height=80,
            placeholder="Ex: Post para Instagram, WhatsApp, público jovem..."
        )
    
    if st.button("Criar", type="primary"):
        if assunto:
            with st.spinner("Criando com IA..."):
                prompt = f"Crie um texto sobre: {assunto}. Tom: {tom}. Público: Cidadãos de São Paulo. Responda APENAS com o texto criado."
                resultado = chamar_groq(prompt, contexto_criacao)
                
                if resultado:
                    st.markdown("**✨ Texto criado**")
                    st.success(resultado)
                    
                    # Salvar criação como revisão também
                    salvar_revisao(f"[CRIAÇÃO] Assunto: {assunto} | Tom: {tom}", resultado, contexto_criacao)
                else:
                    st.error("Erro ao criar. Tente novamente.")
        else:
            st.warning("Digite o assunto")

with aba3:
    st.subheader("📊 Aprendizado e Insights")
    
    # Mostrar insights
    insights = get_insights()
    if insights:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de revisões salvas", insights["total"])
        with col2:
            st.metric("Revisões na última semana", insights["ultima_semana"])
        
        if insights["palavras_comuns"]:
            st.write("**Palavras mais frequentes nos textos:**")
            st.write(", ".join(set(insights["palavras_comuns"])))
    else:
        st.info("Nenhuma revisão salva ainda. Use a ferramenta de revisão e os textos serão armazenados aqui.")
    
    st.divider()
    
    # Mostrar últimas revisões
    st.write("**Últimas revisões salvas:**")
    df = listar_revisoes()
    if not df.empty:
        # Mostrar apenas as 5 últimas
        for _, row in df.head(5).iterrows():
            with st.expander(f"📝 Revisão de {row['data'][:16]}"):
                st.write("**Original:**")
                st.write(row['texto_original'][:200] + "..." if len(row['texto_original']) > 200 else row['texto_original'])
                st.write("**Revisado:**")
                st.write(row['texto_revisado'][:200] + "..." if len(row['texto_revisado']) > 200 else row['texto_revisado'])
                if row['contexto']:
                    st.write(f"**Contexto:** {row['contexto'][:100]}")
    else:
        st.write("Nenhuma revisão salva ainda.")

st.divider()
st.caption("📌 IA: Groq (Llama 3.3 70B) | Revisões salvas para aprendizado contínuo")
