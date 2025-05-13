// functions/tts-proxy.js

import fetch from 'node-fetch';

export const handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: 'Method Not Allowed',
    };
  }

  try {
    const requestBody = JSON.parse(event.body);

    const response = await fetch('https://eu-texttospeech.googleapis.com/v1beta1/text:synthesize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.GOOGLE_TTS_API_KEY}`,
      },
      body: JSON.stringify(requestBody),
    });

    const data = await response.json();

    return {
      statusCode: 200,
      body: JSON.stringify(data),
    };
  } catch (err) {
    console.error('TTS Proxy Error:', err);
    return {
      statusCode: 500,
      body: 'Internal Server Error',
    };
  }
};
