import { useState, useCallback } from "react";

interface DurationInputProps {
  onSubmit: (seconds: number) => void;
  disabled: boolean;
}

export const DurationInput = ({ onSubmit, disabled }: DurationInputProps) => {
  const [input, setInput] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInput(value);
    setError("");
  }, []);

  const handleSubmit = useCallback((e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const trimmed = input.trim();
    if (!trimmed) {
      setError("Enter a duration in seconds");
      return;
    }

    const seconds = parseInt(trimmed, 10);
    if (isNaN(seconds)) {
      setError("Must be a valid number");
      return;
    }

    if (seconds <= 0) {
      setError("Duration must be greater than 0");
      return;
    }

    onSubmit(seconds);
    setInput("");
    setError("");
  }, [input, onSubmit]);

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col gap-4 w-full max-w-sm mx-auto"
    >
      <div className="flex flex-col gap-2">
        <label
          htmlFor="duration-input"
          className="text-sm font-semibold text-gray-300"
        >
          Duration (seconds)
        </label>
        <input
          id="duration-input"
          type="number"
          min="1"
          max="3600"
          placeholder="Enter duration..."
          value={input}
          onChange={handleChange}
          disabled={disabled}
          className="px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        />
      </div>

      {error && <p className="text-sm text-red-400">{error}</p>}

      <button
        type="submit"
        disabled={disabled}
        className="px-4 py-2 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Start
      </button>
    </form>
  );
};

export default DurationInput;
