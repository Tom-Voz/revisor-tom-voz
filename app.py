import streamlit as st
import requests
import sqlite3
import pandas as pd
from datetime import datetime

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
    conn = sqlite3.connect('revisoes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS revisoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto_original TEXT,
            texto_revisado TEXT,
            contexto TEXT,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_revisao(original, revisado, contexto=""):
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
    except:
        return False

def listar_revisoes():
    try:
        conn = sqlite3.connect('revisoes.db')
        df = pd.read_sql_query("SELECT * FROM revisoes ORDER BY data DESC", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

def get_insights():
    df = listar_revisoes()
    if df.empty:
        return None
    return {
        "total": len(df),
        "ultima_semana": len(df[df['data'] > (datetime.now().isoformat().split('T')[0])])
    }

# ==================== FUNÇÃO DE IA (GROQ) ====================
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ Configure a chave API GROQ_API_KEY em Settings → Secrets")
    st.stop()

API_URL = "https://api.groq.com/openai/v1/chat/completions"

def chamar_groq(prompt, contexto_extra=""):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    mensagem = MANUAL
    if contexto_extra:
        mensagem += f"\n\nInformação adicional: {contexto_extra}"
    
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
        return None
    except:
        return None

# ==================== VERIFICAÇÃO DE ADMIN ====================
# Use uma senha simples para acesso à aba de aprendizado
# Isso é mais simples que verificar e-mail

def verificar_admin():
    """Verifica se o usuário tem acesso admin via senha"""
    if "admin_autenticado" not in st.session_state:
        st.session_state.admin_autenticado = False
    
    if st.session_state.admin_autenticado:
        return True
    
    # Mostrar campo de senha
    with st.sidebar:
        st.markdown("---")
        senha = st.text_input("🔐 Acesso Admin", type="password", placeholder="Digite a senha")
        if senha == "admin123":  # <-- ALTERE ESTA SENHA
            st.session_state.admin_autenticado = True
            st.rerun()
    
    return False

# ==================== INTERFACE ====================
init_db()

# Verificar se API está funcionando (silencioso)
teste = chamar_groq("Diga OK")
if not teste:
    st.error("❌ Erro de conexão com a IA. Verifique sua chave API.")

# Criar abas
abas = ["✏️ Revisar Texto", "✨ Criar Texto"]

# Adicionar aba de aprendizado se for admin
if verificar_admin():
    abas.append("📊 Aprendizado")

tab1, tab2, *tab3 = st.tabs(abas)

# ==================== ABA 1: REVISAR ====================
with tab1:
    st.subheader("Revisão de Conteúdo")
    
    texto_original = st.text_area("Texto para revisar:", height=120)
    
    with st.expander("➕ Contexto adicional (opcional)"):
        contexto = st.text_area(
            "Informe o canal, público ou situação:",
            height=80,
            placeholder="Ex: Post para Instagram, público jovem, mensagem de erro no app..."
        )
    
    if st.button("Revisar", type="primary"):
        if texto_original:
            with st.spinner("Revisando com IA..."):
                prompt = f"Revise este texto seguindo as regras. Mantenha o sentido original. Responda APENAS com o texto revisado.\n\nTEXTO: {texto_original}"
                resultado = chamar_groq(prompt, contexto)
                
                if resultado:
                    col_orig, col_rev = st.columns(2)
                    with col_orig:
                        st.markdown("**📄 Original**")
                        st.info(texto_original)
                    with col_rev:
                        st.markdown("**✅ Revisado**")
                        st.success(resultado)
                    
                    salvar_revisao(texto_original, resultado, contexto)
                    st.caption("💾 Revisão salva para aprendizado")
                else:
                    st.error("Erro ao revisar. Tente novamente.")
        else:
            st.warning("Digite um texto para revisar")

# ==================== ABA 2: CRIAR ====================
with tab2:
    st.subheader("Criação de Conteúdo")
    
    col1, col2 = st.columns(2)
    with col1:
        assunto = st.text_input("Assunto:", placeholder="Ex: Prazo do IPTU")
    with col2:
        tom = st.selectbox("Tom:", ["Informativo", "Empático", "Motivador", "Direto"])
    
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
                    salvar_revisao(f"[CRIAÇÃO] Assunto: {assunto} | Tom: {tom}", resultado, contexto_criacao)
                else:
                    st.error("Erro ao criar. Tente novamente.")
        else:
            st.warning("Digite o assunto")

# ==================== ABA 3: APRENDIZADO (se existir) ====================
if len(tab3) > 0:
    with tab3[0]:
        st.subheader("📊 Aprendizado e Insights")
        
        insights = get_insights()
        if insights:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total de revisões salvas", insights["total"])
            with col2:
                st.metric("Revisões na última semana", insights["ultima_semana"])
        else:
            st.info("Nenhuma revisão salva ainda.")
        
        st.divider()
        
        st.write("**Últimas revisões salvas:**")
        df = listar_revisoes()
        if not df.empty:
            for _, row in df.head(10).iterrows():
                with st.expander(f"📝 Revisão de {row['data'][:16]}"):
                    st.write("**Original:**")
                    st.write(row['texto_original'][:300] + "..." if len(row['texto_original']) > 300 else row['texto_original'])
                    st.write("**Revisado:**")
                    st.write(row['texto_revisado'][:300] + "..." if len(row['texto_revisado']) > 300 else row['texto_revisado'])
                    if row['contexto']:
                        st.write(f"**Contexto:** {row['contexto'][:100]}")
        else:
            st.write("Nenhuma revisão salva ainda.")

st.divider()
st.caption("📌 IA: Groq (Llama 3.3 70B) | Acesso Admin no menu lateral")
