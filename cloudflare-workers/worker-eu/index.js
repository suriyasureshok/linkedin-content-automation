export default {
  async fetch(request, env) {

    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: corsHeaders,
      });
    }

    const url = new URL(request.url);

    /*
     * Health Endpoint
     */
    if (url.pathname === "/health") {

      return new Response(
        JSON.stringify({
          status: "healthy",
          worker: "worker-eu",
          region: "eu",
          timestamp: Date.now(),
        }),
        {
          headers: {
            ...corsHeaders,
            "Content-Type": "application/json",
          },
        }
      );
    }

    try {

      const apiKey =
        env.CONTENT_IDEAS_GEMINI_API_KEY;

      if (!apiKey) {

        return new Response(
          JSON.stringify({
            error: "API key missing",
          }),
          {
            status: 500,
            headers: corsHeaders,
          }
        );
      }

      const path = url.pathname;

      const geminiUrl =
        `https://generativelanguage.googleapis.com${path}?key=${apiKey}`;

      const bodyText =
        await request.text();

      console.log(
        JSON.stringify({
          worker: "worker-eu",
          region: "eu",
          path,
          timestamp: Date.now(),
        })
      );

      const geminiResponse =
        await fetch(
          geminiUrl,
          {
            method: request.method,
            headers: {
              "Content-Type":
                "application/json",
            },
            body: bodyText,
          }
        );

      const responseText =
        await geminiResponse.text();

      return new Response(
        responseText,
        {
          status:
            geminiResponse.status,
          headers: {
            ...corsHeaders,
            "Content-Type":
              "application/json",
          },
        }
      );

    } catch (error) {

      return new Response(
        JSON.stringify({
          error: error.message,
        }),
        {
          status: 500,
          headers: {
            ...corsHeaders,
            "Content-Type":
              "application/json",
          },
        }
      );
    }
  },
};