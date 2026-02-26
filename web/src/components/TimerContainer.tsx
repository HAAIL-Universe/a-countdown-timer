import React, { useCallback, useMemo } from 'react';
import { useTimer } from '../hooks/useTimer';
import DurationInput from './DurationInput';
import TimerDisplay from './TimerDisplay';
import CharacterFace from './CharacterFace';
import { ControlButtons } from './ControlButtons';

export interface TimerContainerProps {}

export default function TimerContainer({}: TimerContainerProps): JSX.Element {
  const { timer, isLoading, error, createAndStart, start, stop, reset } = useTimer();

  const handleDurationSubmit = useCallback(
    async (seconds: number) => {
      await createAndStart(seconds);
    },
    [createAndStart]
  );

  const handleStart = useCallback(async () => {
    await start();
  }, [start]);

  const handleStop = useCallback(async () => {
    await stop();
  }, [stop]);

  const handleReset = useCallback(async () => {
    await reset();
  }, [reset]);

  const urgencyLevel = useMemo(() => {
    if (!timer) return 0;
    return timer.urgencyLevel;
  }, [timer]);

  const timerStatus = useMemo(() => {
    if (!timer) return 'idle';
    return timer.status;
  }, [timer]);

  return (
    <div className="timer-container">
      <style>{`
        * {
          box-sizing: border-box;
        }

        body {
          margin: 0;
          padding: 0;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
            'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
            sans-serif;
          -webkit-font-smoothing: antialiased;
          -moz-osx-font-smoothing: grayscale;
          background: #1a1a1a;
          color: #fff;
        }

        .timer-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          width: 100vw;
          min-height: 100vh;
          background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
          padding: 2rem;
          gap: 2rem;
          overflow-y: auto;
        }

        .timer-layout {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 2rem;
          width: 100%;
          max-width: 800px;
          margin: 0 auto;
        }

        .timer-header {
          text-align: center;
          margin-bottom: 1rem;
        }

        .timer-header h1 {
          font-size: 2.5rem;
          font-weight: bold;
          margin: 0;
          background: linear-gradient(135deg, #3b82f6, #8b5cf6);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .timer-header p {
          font-size: 1rem;
          color: #aaa;
          margin: 0.5rem 0 0 0;
        }

        .timer-content {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 2rem;
          width: 100%;
        }

        .timer-input-section {
          display: flex;
          justify-content: center;
          width: 100%;
        }

        .timer-display-section {
          display: flex;
          justify-content: center;
          width: 100%;
        }

        .timer-character-section {
          display: flex;
          justify-content: center;
          width: 100%;
        }

        .timer-controls-section {
          display: flex;
          justify-content: center;
          width: 100%;
        }

        .duration-input-form {
          width: 100%;
          display: flex;
          justify-content: center;
        }

        .duration-input-container {
          display: flex;
          gap: 1rem;
          width: 100%;
          max-width: 400px;
        }

        .duration-input {
          flex: 1;
          padding: 0.75rem 1rem;
          font-size: 1rem;
          border: 2px solid #444;
          border-radius: 0.5rem;
          background: #2a2a2a;
          color: #fff;
          transition: border-color 0.2s ease-in-out;
        }

        .duration-input:focus {
          outline: none;
          border-color: #3b82f6;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .duration-input:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .duration-input::placeholder {
          color: #666;
        }

        .duration-submit-btn {
          padding: 0.75rem 1.5rem;
          font-size: 1rem;
          font-weight: 600;
          border: none;
          border-radius: 0.5rem;
          background: linear-gradient(135deg, #3b82f6, #2563eb);
          color: #fff;
          cursor: pointer;
          transition: all 0.2s ease-in-out;
        }

        .duration-submit-btn:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        }

        .duration-submit-btn:active:not(:disabled) {
          transform: translateY(0);
        }

        .duration-submit-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .control-buttons-container {
          display: flex;
          gap: 1rem;
          justify-content: center;
          width: 100%;
          flex-wrap: wrap;
        }

        .control-btn {
          padding: 0.75rem 1.5rem;
          font-size: 1rem;
          font-weight: 600;
          border: none;
          border-radius: 0.5rem;
          cursor: pointer;
          transition: all 0.2s ease-in-out;
          min-width: 120px;
        }

        .control-btn--start {
          background: linear-gradient(135deg, #10b981, #059669);
          color: #fff;
        }

        .control-btn--start:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        }

        .control-btn--stop {
          background: linear-gradient(135deg, #f59e0b, #d97706);
          color: #fff;
        }

        .control-btn--stop:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
        }

        .control-btn--reset {
          background: linear-gradient(135deg, #ef4444, #dc2626);
          color: #fff;
        }

        .control-btn--reset:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
        }

        .control-btn:active:not(:disabled) {
          transform: translateY(0);
        }

        .control-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .error-message {
          background: rgba(239, 68, 68, 0.1);
          border: 1px solid #ef4444;
          color: #fca5a5;
          padding: 1rem;
          border-radius: 0.5rem;
          text-align: center;
          width: 100%;
          max-width: 400px;
        }

        .loading-indicator {
          color: #aaa;
          font-size: 0.875rem;
          text-align: center;
        }

        @media (max-width: 640px) {
          .timer-container {
            padding: 1rem;
            gap: 1.5rem;
          }

          .timer-header h1 {
            font-size: 2rem;
          }

          .timer-content {
            gap: 1.5rem;
          }

          .duration-input-container {
            flex-direction: column;
            gap: 0.75rem;
          }

          .control-btn {
            min-width: 100px;
            padding: 0.625rem 1.25rem;
            font-size: 0.875rem;
          }
        }
      `}</style>

      <div className="timer-layout">
        <div className="timer-header">
          <h1>⏱ Countdown Timer</h1>
          <p>Set a duration and watch the urgency unfold</p>
        </div>

        <div className="timer-content">
          {!timer && (
            <div className="timer-input-section">
              <DurationInput onSubmit={handleDurationSubmit} disabled={isLoading} />
            </div>
          )}

          {timer && (
            <>
              <div className="timer-display-section">
                <TimerDisplay timer={timer} />
              </div>

              <div className="timer-character-section">
                <CharacterFace urgencyLevel={urgencyLevel} status={timerStatus} />
              </div>

              <div className="timer-controls-section">
                <ControlButtons
                  status={timerStatus}
                  onStart={handleStart}
                  onStop={handleStop}
                  onReset={handleReset}
                  isLoading={isLoading}
                />
              </div>
            </>
          )}

          {error && <div className="error-message">{error}</div>}

          {isLoading && <div className="loading-indicator">Loading...</div>}
        </div>
      </div>
    </div>
  );
}
