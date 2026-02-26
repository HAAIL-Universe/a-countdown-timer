import { useState, useCallback } from "react";

export interface DurationInputProps {
  onSubmit: (seconds: number) => void;
  disabled: boolean;
}

export function DurationInput({ onSubmit, disabled }: DurationInputProps) {
  const [input, setInput] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      setInput(value);
      setError("");
    },
    []
  );

  const parseInput = (val: string): number | null => {
    if (!val.trim()) return null;

    const trimmed = val.trim();

    // Check for MM:SS format
    if (trimmed.includes(":")) {
      const parts = trimmed.split(":");
      if (parts.length === 2) {
        const minutes = parseInt(parts[0], 10);
        const seconds = parseInt(parts[1], 10);
        if (
          !isNaN(minutes) &&
          !isNaN(seconds) &&
          minutes >= 0 &&
          seconds >= 0 &&
          seconds < 60
        ) {
          return minutes * 60 + seconds;
        }
      }
      return null;
    }

    // Plain seconds
    const seconds = parseInt(trimmed, 10);
    if (!isNaN(seconds) && seconds > 0) {
      return seconds;
    }

    return null;
  };

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();

      const seconds = parseInput(input);

      if (seconds === null) {
        setError("Enter seconds or MM:SS format");
        return;
      }

      if (seconds === 0) {
        setError("Duration must be greater than 0");
        return;
      }

      setError("");
      onSubmit(seconds);
      setInput("");
    },
    [input, onSubmit]
  );

  return (
    <div className="flex flex-col items-center gap-4">
      <form onSubmit={handleSubmit} className="flex flex-col items-center gap-3">
        <div className="flex flex-col items-center gap-2">
          <label htmlFor="duration-input" className="text-sm font-semibold text-gray-200">
            Duration (seconds or MM:SS)
          </label>
          <input
            id="duration-input"
            type="text"
            inputMode="numeric"
            value={input}
            onChange={handleChange}
            disabled={disabled}
            placeholder="60 or 1:00"
            className="w-48 px-4 py-2 text-center text-lg font-mono border-2 border-gray-400 bg-gray-900 text-white placeholder-gray-500 rounded focus:outline-none focus:border-blue-400 disabled:opacity-50 disabled:cursor-not-allowed"
          />
        </div>

        {error && <p className="text-sm text-red-400">{error}</p>}

        <button
          type="submit"
          disabled={disabled}
          className="px-6 py-2 font-semibold text-white bg-green-600 rounded hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Start
        </button>
      </form>
    </div>
  );
}
