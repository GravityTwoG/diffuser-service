const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const getRecentImages = async (imagesCount: number) => {
  const response = await fetch(
    `${BASE_URL}/images/recent?imagesCount=${imagesCount}`,
    {
      method: 'GET',
    }
  );

  if (!response.ok) {
    throw new Error('Failed to get recent images');
  }

  return response.json();
};

export const generateImages = async (prompt: string, imagesCount: number) => {
  const response = await fetch(`${BASE_URL}/images/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt, imagesCount }),
  });

  if (!response.ok) {
    throw new Error('Failed to generate images');
  }

  return response.json();
};

export const getGeneratedImages = async (generationId: string) => {
  const response = await fetch(
    `${BASE_URL}/images/generation/${generationId}`,
    {
      method: 'GET',
    }
  );

  if (!response.ok) {
    throw new Error('Failed to get generated images');
  }

  return response.json();
};
