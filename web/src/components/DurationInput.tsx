import { useState, useCallback } from 'react';

export interface DurationInputProps {
  onSubmit: (seconds: number) => void;
  disabled: boolean;
}

export default function DurationInput({ onSubmit, disabled }: DurationInputProps) {
  const [input, setInput] = useState<string>('');

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  }, []);

  const handleSubmit = useCallback((e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const seconds = parseInt(input, 10);
    if (!isNaN(seconds) && seconds > 0) {
      onSubmit(seconds);
      setInput('');
    }
  }, [input, onSubmit]);

  return (
    <form onSubmit={handleSubmit} className="duration-input-form">
      <div className="duration-input-container">
        <input
          type="number"
          value={input}
          onChange={handleChange}
          placeholder="Enter duration (seconds)"
          disabled={disabled}
          min="1"
          className="duration-input"
          aria-label="Timer duration in seconds"
        />
        <button
          type="submit"
          disabled={disabled || !input || parseInt(input, 10) <= 0}
          className="duration-submit-btn"
        >
          Start
        </button>
      </div>
    </form>
  );
}
