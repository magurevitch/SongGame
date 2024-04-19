import React, { useEffect, useState } from 'react';
import './App.css';
import Phase from './Phase';
import ListAdder from './components/ListAdder';
import Voter from './components/Voter';
import Scorer from './components/Scorer';
import API from './components/API';

function App() {
  const [phase, setPhase] = useState<Phase>(Phase.ADD_LIST);

  useEffect(() => {
    API.getPhase().then(response => setPhase(response.phase))
  }, [])

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
      Phase: 
      {phase}
      Content: 
      {choosePhase(phase)}
    </div>
  );
}

export default App;