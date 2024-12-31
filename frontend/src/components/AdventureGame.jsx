import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import Button from './ui/button';  // Correct import
import { Alert, AlertDescription } from './ui/alert';

const AdventureGame = () => {
  const [gameState, setGameState] = useState('start');
  const [stateData, setStateData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [gameHistory, setGameHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  const fetchState = async (state) => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:5000/api/game/state?state=${state}`);
      const data = await response.json();
      setStateData(data.stateData);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch game state');
      setLoading(false);
    }
  };

  const makeChoice = async (choice) => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/game/choice', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: gameState, choice }),
      });
      const data = await response.json();
      
      // Add current state to history
      setGameHistory(prev => [...prev, {
        state: gameState,
        text: stateData.text,
        choice: stateData.choices[choice].text
      }]);
      
      setGameState(data.state);
      setStateData(data.stateData);
      setLoading(false);
    } catch (err) {
      setError('Failed to process choice');
      setLoading(false);
    }
  };

  const restartGame = () => {
    setGameState('start');
    setGameHistory([]);
    fetchState('start');
  };

  useEffect(() => {
    fetchState(gameState);
  }, [gameState]);

  const getOutcomeEmoji = (outcome) => {
    switch (outcome) {
      case 'win':
        return '🎉';
      case 'lose':
        return '💀';
      default:
        return '📜';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Loading your adventure...</div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive" className="max-w-lg mx-auto mt-8">
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="max-w-lg mx-auto mt-8">
      <Card>
        <CardHeader>
          <CardTitle>{stateData.text}</CardTitle>
        </CardHeader>
        <CardContent>
          {Object.keys(stateData.choices).map((choiceKey) => (
            <Button key={choiceKey} onClick={() => makeChoice(choiceKey)}>
              {stateData.choices[choiceKey].text}
            </Button>
          ))}
          {stateData.is_ending && (
            <div className="mt-4">
              <span>{getOutcomeEmoji(stateData.outcome)}</span>
              <Button onClick={restartGame}>Restart Game</Button>
            </div>
          )}
        </CardContent>
      </Card>
      {showHistory && (
        <div className="mt-4">
          <h2>Game History</h2>
          <ul>
            {gameHistory.map((entry, index) => (
              <li key={index}>
                <strong>{entry.state}</strong>: {entry.text} (Choice: {entry.choice})
              </li>
            ))}
          </ul>
        </div>
      )}
      <Button onClick={() => setShowHistory(!showHistory)}>
        {showHistory ? 'Hide History' : 'Show History'}
      </Button>
    </div>
  );
};

export default AdventureGame;