import { useState, useCallback } from 'react';

interface DurationInputProps {
  onSubmit: (seconds: number) => void;
  disabled: boolean;
}

export default function DurationInput({ onSubmit, disabled }: DurationInputProps) {
  const [input, setInput] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = useCallback((e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');

    const duration = parseInt(input, 10);

    if (isNaN(duration) || duration <= 0) {
      setError('Please enter a positive number');
      return;
    }

    onSubmit(duration);
    setInput('');
  }, [input, onSubmit]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
    setError('');
  }, []);

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-md">
      <div className="flex flex-col gap-3">
        <label htmlFor="duration-input" className="text-sm font-medium text-gray-300">
          Duration (seconds)
        </label>
        <div className="flex gap-2">
          <input
            id="duration-input"
            type="number"
            value={input}
            onChange={handleChange}
            disabled={disabled}
            placeholder="e.g., 300"
            className="flex-1 px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700 focus:outline-none focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            min="1"
          />
          <button
            type="submit"
            disabled={disabled || !input}
            className="px-6 py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Start
          </button>
        </div>
        {error && (
          <p className="text-sm text-red-400">{error}</p>
        )}
      </div>
    </form>
  );
}
