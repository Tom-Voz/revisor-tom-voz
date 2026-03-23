def aplicar_4_passos(texto):
    """Aplica os 4 passos do processo de edição do manual"""
    
    # PASSO 1: EXPANDIR (adicionar contexto quando necessário)
    if "IPTU" in texto and "Imposto" not in texto:
        texto = texto.replace("IPTU", "IPTU (o imposto do seu imóvel)")
    
    if "RG" in texto and "Registro Geral" not in texto:
        texto = texto.replace("RG", "RG (seu documento de identidade)")
    
    # PASSO 2: CONCISAR (remover redundâncias)
    redundancias = [
        (r'efetuar o pagamento', 'pagar'),
        (r'realizar o pagamento', 'pagar'),
        (r'fazer o pagamento', 'pagar'),
        (r'pode ser retirado', 'está disponível'),
        (r'por qualquer pessoa', 'você'),
        (r'com o protocolo', 'com o número do protocolo'),
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
        (r'qualquer pessoa', 'você'),
        (r'o RG', 'seu RG'),
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
        (r'dias úteis', 'dias úteis (de segunda a sexta)'),
        (r'retirado', 'retirado'),
    ]
    for busca, substitui in simplificacoes:
        texto = re.sub(busca, substitui, texto, flags=re.IGNORECASE)
    
    # Correções específicas para evitar frases estranhas
    texto = texto.replace("seu RG o RG", "seu RG")
    texto = texto.replace("seu RG pode ser retirado", "seu RG está disponível para retirada")
    texto = texto.replace("você com o número", "com o número")
    
    return texto
