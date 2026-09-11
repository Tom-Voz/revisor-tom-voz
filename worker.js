export default {
  async fetch(request, env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Plugin-Key',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    if (request.method !== 'POST') {
      console.log('Método não permitido:', request.method);
      return new Response(JSON.stringify({ error: 'Método não permitido' }), {
        status: 405,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    const pluginKey = request.headers.get('X-Plugin-Key');
    console.log('Plugin key recebida:', pluginKey ? 'sim' : 'não');
    
    if (pluginKey !== 'bvzx8wlwv73yefetx656uzky') {
      console.log('Plugin key inválida');
      return new Response(JSON.stringify({ error: 'Chave do plugin inválida' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    if (!env.GROQ_API_KEY) {
      console.log('GROQ_API_KEY não configurada');
      return new Response(JSON.stringify({ 
        error: 'GROQ_API_KEY não configurada no Worker.' 
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    console.log('GROQ_API_KEY configurada, prosseguindo...');

    try {
      const rawBody = await request.text();
      console.log('Tamanho do body recebido:', rawBody.length);
      
      if (!rawBody || rawBody.length === 0) {
        throw new Error('Body da requisição está vazio');
      }

      const body = JSON.parse(rawBody);
      const textos = body.textos || [];
      console.log('Quantidade de textos recebidos:', textos.length);

      if (textos.length === 0) {
        return new Response(JSON.stringify({ resultados: [] }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      const resultados = [];

      for (const item of textos) {
        console.log('Processando texto id:', item.id, 'tamanho:', item.texto?.length || 0);
        
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
                content: `Você é um revisor de texto do Governo de São Paulo. Analise o texto e retorne APENAS um JSON válido no formato: {"apontamentos": [{"criterio": "gramatica|tom|clareza", "trecho": "texto original", "explicacao": "motivo", "sugestao": "texto reescrito", "severidade": "alta|media|baixa"}]}. Se não houver apontamentos, retorne {"apontamentos": []}.`
              },
              { role: 'user', content: item.texto }
            ],
            temperature: 0.3,
            max_tokens: 1000
          })
        });

        console.log('Resposta da Groq status:', resposta.status);

        if (!resposta.ok) {
          const erroGroq = await resposta.text();
          console.log('Erro da Groq:', erroGroq);
          resultados.push({ 
            id: item.id, 
            apontamentos: [], 
            erro: `Erro da API Groq (${resposta.status}): ${erroGroq}` 
          });
          continue;
        }

        const dados = await resposta.json();
        const conteudo = dados.choices[0].message.content;
        const match = conteudo.match(/\{[\s\S]*\}/);
        
        if (match) {
          try {
            const parsed = JSON.parse(match[0]);
            resultados.push({ id: item.id, apontamentos: parsed.apontamentos || [] });
          } catch (e) {
            console.log('JSON inválido da IA:', e.message);
            resultados.push({ id: item.id, apontamentos: [], erro: 'A IA não retornou um JSON válido.' });
          }
        } else {
          resultados.push({ id: item.id, apontamentos: [] });
        }
      }

      console.log('Processamento concluído, resultados:', resultados.length);
      
      return new Response(JSON.stringify({ resultados }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });

    } catch (err) {
      console.log('Erro capturado no try/catch:', err.message);
      console.log('Stack:', err.stack);
      
      return new Response(JSON.stringify({ 
        error: `Erro interno no Worker: ${err.message}`,
        stack: err.stack 
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};
