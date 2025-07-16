// File: frontend/src/components/PropertyInput.tsx
'use client';

import { useState } from 'react';
import ComparablesDisplay from './ComparablesDisplay';
import { Comparable } from '@/types/Comparable';

export default function PropertyInput() {
  const [address, setAddress] = useState('');
  const [comparables, setComparables] = useState<Comparable[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);
    setComparables(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/get_comparables', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to fetch comparables.');
      }

      const data = await response.json();
      setComparables(data.best_comparables);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-xl">
      <form onSubmit={handleSubmit} className="flex flex-col items-center">
        <input
          type="text"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          placeholder="e.g., 123 Main St, Chicago, IL"
          className="w-full p-3 border border-gray-300 rounded-md shadow-sm text-black focus:ring-2 focus:ring-blue-500"
          required
        />
        <button
          type="submit"
          disabled={isLoading}
          className="mt-4 w-full md:w-auto px-6 py-3 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
        >
          {isLoading ? 'Searching...' : 'Find Comparables'}
        </button>
      </form>

      {error && <p className="mt-4 text-red-600 text-center">{error}</p>}

      {comparables && <ComparablesDisplay comparables={comparables} />}
    </div>
  );
}