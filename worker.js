export default {
  async fetch(request, env) {
    // CORS para o Figma
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Plugin-Key',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'Método não permitido' }), {
        status: 405,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    // Verificar chave do plugin
    const pluginKey = request.headers.get('X-Plugin-Key');
    if (pluginKey !== 'bvzx8wlwv73yefetx656uzky') {
      return new Response(JSON.stringify({ error: 'Chave inválida' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    try {
      const body = await request.json();
      const textos = body.textos || [];

      const resultados = [];

      for (const item of textos) {
        const resposta = await fetch('https://api.groq.com/openai/v1/chat/completions', {
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
                content: `Você é um revisor de texto do Governo de São Paulo. Analise o texto e retorne APENAS um JSON válido no formato:
{"apontamentos": [{"criterio": "gramatica|tom|clareza", "trecho": "texto original", "explicacao": "motivo", "sugestao": "texto reescrito", "severidade": "alta|media|baixa"}]}
Se não houver apontamentos, retorne {"apontamentos": []}.`
              },
              { role: 'user', content: item.texto }
            ],
            temperature: 0.3,
            max_tokens: 1000
          })
        });

        if (!resposta.ok) {
          const erro = await resposta.text();
          resultados.push({ id: item.id, apontamentos: [], erro: `Groq ${resposta.status}: ${erro}` });
          continue;
        }

        const dados = await resposta.json();
        const conteudo = dados.choices[0].message.content;

        // Extrair JSON da resposta (a IA pode incluir texto antes/depois)
        const match = conteudo.match(/\{[\s\S]*\}/);
        if (match) {
          try {
            const parsed = JSON.parse(match[0]);
            resultados.push({ id: item.id, apontamentos: parsed.apontamentos || [] });
          } catch (e) {
            resultados.push({ id: item.id, apontamentos: [], erro: 'JSON inválido da IA' });
          }
        } else {
          resultados.push({ id: item.id, apontamentos: [] });
        }
      }

      return new Response(JSON.stringify({ resultados }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });

    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};
