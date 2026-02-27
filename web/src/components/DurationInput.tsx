import { useState } from 'react';

interface DurationInputProps {
  onSubmit: (seconds: number) => void;
  disabled: boolean;
}

/**
 * Numeric input for setting timer duration in seconds.
 * Quick-pick buttons for common durations.
 */
export default function DurationInput({ onSubmit, disabled }: DurationInputProps) {
  const [value, setValue] = useState('60');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const seconds = parseInt(value, 10);
    if (seconds > 0) {
      onSubmit(seconds);
    }
  };

  const quickPick = (seconds: number) => {
    setValue(String(seconds));
    onSubmit(seconds);
  };

  return (
    <div className="mb-6">
      <form onSubmit={handleSubmit} className="flex items-center gap-3 mb-3">
        <input
          type="number"
          min="1"
          max="3600"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          disabled={disabled}
          className="w-24 px-3 py-2 text-center text-xl font-mono bg-gray-800 text-white border border-gray-600 rounded focus:outline-none focus:border-retro-blue disabled:opacity-50"
          placeholder="60"
        />
        <span className="text-gray-400 text-sm">seconds</span>
        <button
          type="submit"
          disabled={disabled}
          className="px-4 py-2 bg-retro-green text-gray-900 font-bold rounded hover:bg-green-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          GO
        </button>
      </form>

      <div className="flex gap-2 justify-center">
        {[30, 60, 120, 300].map((s) => (
          <button
            key={s}
            onClick={() => quickPick(s)}
            disabled={disabled}
            className="px-3 py-1 text-xs font-mono bg-gray-700 text-gray-300 rounded hover:bg-gray-600 transition-colors disabled:opacity-50"
          >
            {s >= 60 ? `${s / 60}m` : `${s}s`}
          </button>
        ))}
      </div>
    </div>
  );
}
