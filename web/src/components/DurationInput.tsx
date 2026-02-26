import { useState, useCallback } from 'react';

export interface DurationInputProps {
  onSubmit: (seconds: number) => void;
  disabled: boolean;
}

export function DurationInput({ onSubmit, disabled }: DurationInputProps) {
  const [input, setInput] = useState('');
  const [error, setError] = useState('');

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInput(value);
    setError('');
  }, []);

  const handleSubmit = useCallback(() => {
    const trimmed = input.trim();

    if (!trimmed) {
      setError('Please enter a duration');
      return;
    }

    const seconds = parseInt(trimmed, 10);

    if (isNaN(seconds)) {
      setError('Duration must be a number');
      return;
    }

    if (seconds <= 0) {
      setError('Duration must be greater than 0');
      return;
    }

    onSubmit(seconds);
    setInput('');
    setError('');
  }, [input, onSubmit]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  }, [handleSubmit]);

  return (
    <div className="flex flex-col gap-4">
      <div className="flex gap-2">
        <input
          type="number"
          value={input}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder="Enter duration (seconds)"
          className="flex-1 px-4 py-2 border border-gray-300 rounded bg-white text-gray-900 placeholder-gray-500 disabled:bg-gray-100 disabled:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          min="1"
          max="3600"
        />
        <button
          onClick={handleSubmit}
          disabled={disabled}
          className="px-6 py-2 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          Start
        </button>
      </div>
      {error && <p className="text-red-600 text-sm">{error}</p>}
    </div>
  );
}

export default DurationInput;
