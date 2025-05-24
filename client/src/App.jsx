import React, { useState } from 'react';


function App() {
  const [city, setCity] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const getItinerary = async () => {
    if (!city.trim()) return;
    
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const res = await fetch('http://127.0.0.1:5000/api/itinerary', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ city })
      });

      const data = await res.json();

      if (res.ok) {
        setResult(data);
      } else {
        setError(data.error || 'Something went wrong.');
      }
    } catch (err) {
      setError('Failed to fetch itinerary.');
    }

    setLoading(false);
  };

  return (
    <div style={{ maxWidth: '600px', margin: 'auto', padding: '2rem' }}>
      <h1 className='text-5xl font-extrabold text-center text-orange-400 mb-5 mt-4'>AI Travel Guide</h1>

      <input
        type="text"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        placeholder="Enter your city"
        className="border border-white text-white rounded p-2 w-full mt-4"
      />

      <div className='flex justify-center items-center mt-3'>
        <button
          onClick={getItinerary}
          disabled={loading}
          className=' bg-green-700 text-white rounded px-4 py-2 mt-4 hover:bg-green-900 transition duration-200'
        >
          {loading ? 'Generating...' : 'Generate Itinerary'}
        </button>
      </div>

      {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}

      {result && (
        <div className='flex justify-center'>
          <div className='text-white mt-15 flex flex-col justify-center'>
            <h1 className='mb-4 text-xl font-bold text-center'>Suggested Travel Plan For <span className='text-orange-400'>{result.destination}</span> according to AI</h1>
            <div className='flex flex-col items-center'>
              <p><strong>Ideal Days:</strong> {result.days}</p>
              <p><strong>Budget:</strong> Rs. {result.budget} </p>
              <p className='mt-5'><span className='text-blue-400 font-bold text-lg'>Suggested Activities:</span></p>
              <ul>
                {result.activities.map((activity, index) => (
                  <li key={index}>{index+1}. {activity}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
