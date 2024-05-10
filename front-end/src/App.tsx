import React, { useEffect, useState } from 'react';
import './App.css';
import Phase from './Phase';
import ListAdder from './components/ListAdder';
import Voter from './components/Voter';
import Scorer from './components/Scorer';
import API from './components/API';
import Admin from './components/Admin';

function App() {
  const [currentGame, setCurrentGame] = useState<number>(1);
  const [phase, setPhase] = useState<Phase>(Phase.ADD_LIST);
  const [prompt, setPrompt] = useState<string>("");

  useEffect(() => {
    API.getCurrentGame().then(response => setCurrentGame(response.game));
  }, [])

  useEffect(() => {
    API.getPhase(currentGame).then(response => setPhase(Phase[response.phase as keyof typeof Phase]));
    API.getPrompt(currentGame).then(response => setPrompt(response.prompt));
  }, [currentGame]);

  const choosePhase = (phase: Phase) => {
    switch(phase) {
      case Phase.ADD_LIST:
        return <ListAdder />
      case Phase.VOTE:
        return <Voter />
      case Phase.SCORE:
        return <Scorer />
      case Phase.ADMIN:
        return <Admin setPhase={setPhase} />
    }
  };

  return (
    <div className="App">
      Song Game
      <br/>
      Game:
      {currentGame} - {prompt}
      <br/>
      Phase:
      {Phase[phase]}
      <br/>
      {choosePhase(phase)}
    </div>
  );
}

export default App;