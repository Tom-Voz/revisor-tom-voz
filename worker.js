export default {
  async fetch(request) {
    return new Response(
      JSON.stringify({
        ok: true,
        mensagem: "Worker funcionando"
      }),
      {
        status: 200,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      }
    );
  }
};
