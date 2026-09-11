export default {
  async fetch(request, env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Plugin-Key',
    };

    // CORS
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

    // Verifica a chave
    const pluginKey = request.headers.get('X-Plugin-Key');

    if (!pluginKey) {
      return json(
        { error: 'X-Plugin-Key não foi enviada.' },
        401,
        corsHeaders
      );
    }

    if (pluginKey !== env.PLUGIN_KEY) {
      return json(
        { error: 'X-Plugin-Key inválida.' },
        401,
        corsHeaders
      );
    }

    try {
      const body = await request.json();

      return json(
        {
          ok: true,
          mensagem: 'Worker recebeu a requisição corretamente.',
          quantidadeTextos: Array.isArray(body?.textos)
            ? body.textos.length
            : null
        },
        200,
        corsHeaders
      );

    } catch (error) {
      console.error('ERRO AO LER JSON:', error);

      return json(
        {
          error: 'Não foi possível ler o JSON enviado pelo Figma.',
          detalhe: error?.message || String(error)
        },
        400,
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
