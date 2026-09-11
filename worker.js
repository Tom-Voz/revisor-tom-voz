export default {
  async fetch(request, env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Plugin-Key',
    };

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: corsHeaders,
      });
    }

    // Apenas POST
    if (request.method !== 'POST') {
      return json(
        { error: 'Método não permitido' },
        405,
        corsHeaders
      );
    }

    // Validação da chave
    const pluginKey = request.headers.get('X-Plugin-Key');

    if (!pluginKey || pluginKey !== env.PLUGIN_KEY) {
      return json(
        { error: 'Chave do plugin inválida' },
        401,
        corsHeaders
      );
    }

    // Secret da Groq
    const groqApiKey = env.GROQ_API_KEY;

    if (!groqApiKey) {
      return json(
        {
          error:
            'GROQ_API_KEY não configurada no Worker.'
        },
        500,
        corsHeaders
      );
    }

    try {
      const body = await request.json();

      if (!body || !Array.isArray(body.textos)) {
        return json(
          {
            error:
              'Formato inválido. Esperado: { "textos": [...] }'
          },
          400,
          corsHeaders
        );
      }

      const textos = body.textos;

      if (textos.length === 0) {
        return json(
          { resultados: [] },
          200,
          corsHeaders
        );
      }

      const resultados = [];

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
              Authorization: `Bearer ${groqApiKey}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              model: 'openai/gpt-oss-120b',
              messages: [
                {
                  role: 'system',
                  content: `
Você é um revisor de texto do Governo de São Paulo.

Analise o texto considerando:
- gramática;
- tom;
- clareza.

Retorne APENAS JSON válido neste formato:

{
  "apontamentos": [
    {
      "criterio": "gramatica|tom|clareza",
      "trecho": "texto original",
      "explicacao": "motivo",
      "sugestao": "texto reescrito",
      "severidade": "alta|media|baixa"
    }
  ]
}

Se não houver apontamentos, retorne:

{
  "apontamentos": []
}
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

        const match = conteudo.match(/\{[\s\S]*\}/);

        if (!match) {
          resultados.push({
            id: item.id,
            apontamentos: [],
            erro: 'A IA não retornou JSON.'
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
