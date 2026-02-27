import { useState, useCallback } from "react";

export interface DurationInputProps {
  onSubmit: (seconds: number) => void;
  disabled: boolean;
}

export default function DurationInput({ onSubmit, disabled }: DurationInputProps) {
  const [input, setInput] = useState("");
  const [error, setError] = useState("");

  const parseSeconds = useCallback((value: string): number | null => {
    const trimmed = value.trim();
    if (!trimmed) return null;

    // Try parsing as pure seconds
    const asSeconds = parseInt(trimmed, 10);
    if (!isNaN(asSeconds) && asSeconds > 0 && asSeconds < 86400) {
      return asSeconds;
    }

    // Try parsing as MM:SS format
    if (trimmed.includes(":")) {
      const [mmStr, ssStr] = trimmed.split(":").slice(0, 2);
      const mm = parseInt(mmStr, 10);
      const ss = parseInt(ssStr || "0", 10);
      if (!isNaN(mm) && !isNaN(ss) && mm >= 0 && ss >= 0 && ss < 60) {
        const total = mm * 60 + ss;
        if (total > 0 && total < 86400) return total;
      }
    }

    return null;
  }, []);

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.currentTarget.value;
      setInput(value);
      setError("");
    },
    []
  );

  const handleSubmit = useCallback(
    (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();

      const seconds = parseSeconds(input);
      if (seconds === null) {
        setError("Enter a valid duration (e.g., 300 or 5:00)");
        return;
      }

      onSubmit(seconds);
      setInput("");
      setError("");
    },
    [input, parseSeconds, onSubmit]
  );

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Enter") {
        handleSubmit(e as unknown as React.FormEvent<HTMLFormElement>);
      }
    },
    [handleSubmit]
  );

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-sm">
      <div className="flex flex-col gap-2">
        <label htmlFor="duration-input" className="text-sm font-semibold text-gray-300">
          Duration (seconds or MM:SS)
        </label>
        <input
          id="duration-input"
          type="text"
          value={input}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder="e.g., 300 or 5:00"
          className="px-4 py-2 bg-gray-800 text-white border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed font-mono text-lg"
          aria-label="Duration input"
        />
        {error && <span className="text-sm text-red-400">{error}</span>}
      </div>

      <button
        type="submit"
        disabled={disabled}
        className="px-6 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors"
        aria-label="Start timer"
      >
        Start
      </button>
    </form>
  );
}
