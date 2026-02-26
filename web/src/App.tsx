import React from 'react';
import { TimerContainer } from './components/TimerContainer';

export function App(): React.ReactElement {
  return (
    <div className="min-h-screen w-screen bg-gray-900 overflow-hidden">
      <TimerContainer />
    </div>
  );
}

export default App;
