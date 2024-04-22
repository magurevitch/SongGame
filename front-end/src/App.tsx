import React, { useEffect, useState } from 'react';
import './App.css';
import Phase from './Phase';
import ListAdder from './components/ListAdder';
import Voter from './components/Voter';
import Scorer from './components/Scorer';
import API from './components/API';

function App() {
  const [phase, setPhase] = useState<Phase>(Phase.ADD_LIST);
  const [currentGame, setCurrentGame] = useState<number>(1);

  useEffect(() => {
    API.getCurrentGame().then(response => setCurrentGame(response.game));
  }, [])

  useEffect(() => {
    API.getPhase(currentGame).then(response => setPhase(Phase[response.phase as keyof typeof Phase]));
  }, [currentGame]);

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
      Game:
      {currentGame}
      Phase: 
      {Phase[phase]}
      {choosePhase(phase)}
    </div>
  );
}

export default App;