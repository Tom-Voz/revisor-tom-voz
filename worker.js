export default {
  async fetch(request, env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Plugin-Key',
    };

    // Permite o preflight do Figma
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: corsHeaders,
      });
    }

    // Aceita somente POST
    if (request.method !== 'POST') {
      return json(
        { error: 'Método não permitido' },
        405,
        corsHeaders
      );
    }

    // Verifica a chave enviada pelo plugin
const pluginKey = request.headers.get('X-Plugin-Key');

console.log('DIAGNOSTICO_AUTH', {
  recebeuHeader: !!pluginKey,
  tamanhoRecebido: pluginKey ? pluginKey.length : 0,
  existeEnv: !!env.PLUGIN_KEY,
  tamanhoEnv: env.PLUGIN_KEY ? env.PLUGIN_KEY.length : 0,
  tipoEnv: typeof env.PLUGIN_KEY
});

if (!pluginKey || pluginKey !== env.PLUGIN_KEY) {
  return json(
    {
      error: 'Chave do plugin inválida',
      diagnostico: {
        recebeuHeader: !!pluginKey,
        tamanhoRecebido: pluginKey ? pluginKey.length : 0,
        existeEnv: !!env.PLUGIN_KEY,
        tamanhoEnv: env.PLUGIN_KEY ? env.PLUGIN_KEY.length : 0,
        tipoEnv: typeof env.PLUGIN_KEY
      }
    },
    401,
    corsHeaders
  );
}

    // Verifica a chave da Groq
    if (!env.GROQ_API_KEY) {
      return json(
        {
          error: 'GROQ_API_KEY não configurada no Worker.'
        },
        500,
        corsHeaders
      );
    }

    try {
      const body = await request.json();

      // Verifica o formato enviado pelo plugin
      if (!body || !Array.isArray(body.textos)) {
        return json(
          {
            error: 'Formato inválido. Esperado: { "textos": [...] }'
          },
          400,
          corsHeaders
        );
      }

      const textos = body.textos;

      // Se não houver textos, retorna vazio
      if (textos.length === 0) {
        return json(
          { resultados: [] },
          200,
          corsHeaders
        );
      }

      const resultados = [];

      // Analisa cada texto enviado pelo plugin
      for (const item of textos) {
        if (!item || typeof item.texto !== 'string') {
          resultados.push({
            id: item?.id || null,
            apontamentos: [],
            erro: 'Item de texto inválido.'
          });

          continue;
        }

        const resposta = await fetch(
          'https://api.groq.com/openai/v1/chat/completions',
          {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${env.GROQ_API_KEY}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              model: 'openai/gpt-oss-120b',

              messages: [
                {
                  role: 'system',
                  content: `
Você é um revisor de textos do Governo do Estado de São Paulo.

Analise o texto considerando exclusivamente estes três critérios:

1. gramática
2. tom
3. clareza

Considere uma linguagem:
- simples;
- direta;
- clara;
- acessível;
- prestativa;
- confiável;
- adequada à comunicação de serviços públicos.

Não faça elogios.
Não invente problemas.
Não altere o sentido do texto.
Só apresente um apontamento quando houver algo que realmente possa ser melhorado.

Retorne SOMENTE JSON válido.

Formato obrigatório:

{
  "apontamentos": [
    {
      "criterio": "gramatica|tom|clareza",
      "trecho": "trecho exato do texto original",
      "explicacao": "explicação objetiva do problema",
      "sugestao": "texto sugerido",
      "severidade": "alta|media|baixa"
    }
  ]
}

Se não houver nenhum problema:

{
  "apontamentos": []
}

Não escreva markdown.
Não escreva comentários antes ou depois do JSON.
`
                },
                {
                  role: 'user',
                  content: item.texto
                }
              ],

              temperature: 0.3,
              max_tokens: 1000
            })
          }
        );

        // Erro retornado pela Groq
        if (!resposta.ok) {
          const erroGroq = await resposta.text();

          resultados.push({
            id: item.id,
            apontamentos: [],
            erro: `Erro da API Groq (${resposta.status}): ${erroGroq}`
          });

          continue;
        }

        const dados = await resposta.json();

        const conteudo =
          dados?.choices?.[0]?.message?.content;

        if (!conteudo) {
          resultados.push({
            id: item.id,
            apontamentos: [],
            erro: 'A API não retornou conteúdo.'
          });

          continue;
        }

        // Localiza o JSON retornado pela IA
        const match = conteudo.match(/\{[\s\S]*\}/);

        if (!match) {
          resultados.push({
            id: item.id,
            apontamentos: [],
            erro: 'A IA não retornou JSON válido.'
          });

          continue;
        }

        try {
          const parsed = JSON.parse(match[0]);

          resultados.push({
            id: item.id,
            apontamentos: Array.isArray(parsed.apontamentos)
              ? parsed.apontamentos
              : []
          });

        } catch (error) {
          resultados.push({
            id: item.id,
            apontamentos: [],
            erro: 'JSON retornado pela IA é inválido.'
          });
        }
      }

      // Resposta final para o plugin
      return json(
        { resultados },
        200,
        corsHeaders
      );

    } catch (error) {
      console.error('ERRO NO WORKER:', error);

      return json(
        {
          error: 'Erro interno no Worker.',
          detalhe: error?.message || String(error)
        },
        500,
        corsHeaders
      );
    }
  }
};


// Função para respostas JSON
function json(data, status, corsHeaders) {
  return new Response(
    JSON.stringify(data),
    {
      status,
      headers: {
        ...corsHeaders,
        'Content-Type': 'application/json'
      }
    }
  );
}
