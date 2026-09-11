export default {
  async fetch(request, env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Plugin-Key',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: corsHeaders,
      });
    }

    if (request.method !== 'POST') {
      return json(
        { error: 'Método não permitido' },
        405,
        corsHeaders
      );
    }

    try {
      const body = await request.json();

      if (!body || !Array.isArray(body.textos)) {
        return json(
          {
            error: 'Formato inválido. Esperado: { "textos": [...] }'
          },
          400,
          corsHeaders
        );
      }

      if (body.textos.length === 0) {
        return json(
          { resultados: [] },
          200,
          corsHeaders
        );
      }

      const item = body.textos[0];

      if (!item || typeof item.texto !== 'string') {
        return json(
          {
            error: 'O primeiro item não contém um texto válido.'
          },
          400,
          corsHeaders
        );
      }

      const groqApiKey = env.GROQ_API_KEY;

      if (!groqApiKey) {
        return json(
          {
            error: 'GROQ_API_KEY não está disponível no Worker.'
          },
          500,
          corsHeaders
        );
      }

      const resposta = await fetch(
        'https://api.groq.com/openai/v1/chat/completions',
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${groqApiKey}`,
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

      const respostaTexto = await resposta.text();

      if (!resposta.ok) {
        return json(
          {
            error: `Erro da Groq (${resposta.status})`,
            detalhe: respostaTexto
          },
          502,
          corsHeaders
        );
      }

      let dados;

      try {
        dados = JSON.parse(respostaTexto);
      } catch {
        return json(
          {
            error: 'A Groq respondeu, mas a resposta não é JSON válido.',
            detalhe: respostaTexto
          },
          502,
          corsHeaders
        );
      }

      const conteudo =
        dados?.choices?.[0]?.message?.content;

      if (!conteudo) {
        return json(
          {
            error: 'A Groq não retornou conteúdo.',
            resposta: dados
          },
          502,
          corsHeaders
        );
      }

      return json(
        {
          ok: true,
          teste: true,
          id: item.id,
          respostaGroq: conteudo
        },
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
