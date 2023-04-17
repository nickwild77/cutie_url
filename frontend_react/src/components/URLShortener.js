import React, { useState } from 'react';
import axios from 'axios';

const URLShortener = () => {
  const [longURL, setLongURL] = useState('');
  const [shortURL, setShortURL] = useState('');

  const handleInputChange = (e) => {
    setLongURL(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Make a POST request to the Django REST API to create a short URL
      const response = await axios.post('/urls/', { long_url: longURL });
      setShortURL(response.data.short_url);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>URL Shortener</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" value={longURL} onChange={handleInputChange} />
        <button type="submit">Shorten URL</button>
      </form>
      {shortURL && (
        <p>
          Short URL: <a href={shortURL}>{shortURL}</a>
        </p>
      )}
    </div>
  );
};

export default URLShortener;
