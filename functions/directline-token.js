import fetch from 'node-fetch';

export const handler = async (event) => {
  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      body: 'Method Not Allowed',
    };
  }

  try {
    const response = await fetch('https://directline.botframework.com/v3/directline/tokens/generate', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.DIRECT_LINE_SECRET}`,
      }
    });

    if (!response.ok) {
      throw new Error(`Token request failed: ${response.statusText}`);
    }

    const data = await response.json();

    return {
      statusCode: 200,
      body: JSON.stringify({ token: data.token }),
    };
  } catch (err) {
    console.error('Direct Line Token Error:', err);
    return {
      statusCode: 500,
      body: 'Failed to generate Direct Line token',
    };
  }
};
