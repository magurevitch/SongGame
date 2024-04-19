import { useState } from 'react';
import './App.css';
import Phase from './Phase';
import ListAdder from './components/ListAdder';
import React from 'react';
import Voter from './components/Voter';
import Scorer from './components/Scorer';

function App() {
  const [phase, setPhase] = useState<Phase>(Phase.ADD_LIST);

  const choosePhase = (phase: Phase) => {
    switch(phase) {
      case Phase.ADD_LIST:
        return <ListAdder />
      case Phase.VOTE:
        return <Voter />
      case Phase.SCORE:
        return <Scorer />
    }
  };

  return (
    <div className="App">
      Song Game
      {choosePhase(phase)}
    </div>
  );
}

export default App;