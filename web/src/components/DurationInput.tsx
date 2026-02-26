import { useState, useCallback } from "react";

export interface DurationInputProps {
  onSubmit: (seconds: number) => void;
  disabled: boolean;
}

export default function DurationInput({ onSubmit, disabled }: DurationInputProps) {
  const [input, setInput] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInput(value);
    setError("");
  }, []);

  const handleSubmit = useCallback(
    (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();

      const trimmed = input.trim();
      if (!trimmed) {
        setError("Please enter a duration");
        return;
      }

      const seconds = parseInt(trimmed, 10);
      if (isNaN(seconds)) {
        setError("Duration must be a number");
        return;
      }

      if (seconds <= 0) {
        setError("Duration must be greater than 0");
        return;
      }

      if (seconds > 3600) {
        setError("Duration must be 3600 seconds or less");
        return;
      }

      onSubmit(seconds);
      setInput("");
      setError("");
    },
    [input, onSubmit]
  );

  return (
    <form onSubmit={handleSubmit} className="duration-input-form">
      <div className="duration-input-group">
        <label htmlFor="duration-seconds" className="duration-input-label">
          Duration (seconds)
        </label>
        <input
          id="duration-seconds"
          type="text"
          inputMode="numeric"
          placeholder="Enter seconds (1-3600)"
          value={input}
          onChange={handleChange}
          disabled={disabled}
          className="duration-input-field"
          aria-describedby={error ? "duration-error" : undefined}
        />
        {error && (
          <p id="duration-error" className="duration-input-error">
            {error}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={disabled || input.trim() === ""}
        className="duration-input-button"
      >
        Start
      </button>
    </form>
  );
}
