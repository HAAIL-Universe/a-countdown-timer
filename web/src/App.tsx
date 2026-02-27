import React from 'react';
import TimerContainer from './components/TimerContainer';

export const App: React.FC = () => {
  return (
    <div className="min-h-screen w-full bg-gray-900">
      <TimerContainer />
    </div>
  );
};

export default App;
