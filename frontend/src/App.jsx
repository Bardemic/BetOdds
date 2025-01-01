import React, { useEffect, useState } from 'react';

const App = () => {
  const [resultNFL, setResultNFL] = useState([]);
  const [resultNBA, setResultNBA] = useState([]);
  const [activeResult, setActiveResult] = useState('NFL');
  const [statTypeNFL, setStatTypeNFL] = useState('passYards');
  const [statTypeNBA, setStatTypeNBA] = useState('pointsAssists');
  const [time, setTime] = useState('');


  const fetchData = async () => {
    try {
      const response_nfl = await fetch(`${import.meta.env.VITE_BACKEND_URL}/get-best-lines-nfl`);
      const response_nba = await fetch(`${import.meta.env.VITE_BACKEND_URL}/get-best-lines-nba`);
      const response_time = await fetch(`${import.meta.env.VITE_BACKEND_URL}/get-last-updated`);
      const dataNFL = await response_nfl.json();
      const dataNBA = await response_nba.json();
      const response_time_data = await response_time.json();

      setTime(response_time_data);
      
      const combinedDataNFL = dataNFL.map(item => ({
        ...item
      }));

      const combinedDataNBA = dataNBA.map(item => ({
        ...item
      }));

      setResultNFL(combinedDataNFL);
      setResultNBA(combinedDataNBA);
    } catch (error) {
      setResultNBA('Error: ' + error.message);
      setResultNFL('Error: ' + error.message);
    }
  };


  useEffect(() => {
    fetchData()
  }, []);

  return (
    <div className="bg-gray-100 min-h-screen w-screen">
      <div className="w-5/6 mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">BetOdds</h1>
        <div className='m-2 flex items-center gap-2'>
          <button
            onClick={() => (activeResult == "NFL" ? setActiveResult("NBA") : setActiveResult("NFL"))}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
          >
            {activeResult}
          </button>
          {
          activeResult == "NFL" ? 
            <select 
            value={statTypeNFL} 
            onChange={(e) => setStatTypeNFL(e.target.value)}
            className="bg-white text-gray-800 font-semibold py-2 px-4 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="passYards">Pass Yds</option>
            <option value="rushYards">Rush Yds</option>
            <option value="recYards">Rec Yds</option>
            <option value="receptions">Receptions</option>
            <option value="anytimeTD">Anytime TD</option>
            <option value="passTD">Pass TD</option>
            <option value="passCompletions">Pass Completions</option>
            <option value="passAttempts">Pass Att</option>
            <option value="passLng">Longest Pass</option>
            <option value="passInt">Interceptions</option>
            <option value="passAndRushYards">P+R Yards</option>
            <option value="rushAttempts">Rush Att</option>
            <option value="rushLng">Longest Rush</option>
            <option value="rushAndRecYards">R+R Yards</option>
            <option value="recLng">Longest Reception</option>
            <option value="targets">Targets</option>
            <option value="kickingPoints">Kicking Pts</option>
            <option value="kickingFG">Field Goals</option>
            <option value="kickingPAT">Point After TD</option>
            <option value="tackles">Tackles</option>
            <option value="tacklesAndAssists">Tackles + Ast</option>
            <option value="assists">Ast</option>
            <option value="idk">Sacks (nAn)</option>
          </select> :
          <select 
          value={statTypeNBA} 
          onChange={(e) => setStatTypeNBA(e.target.value)}
          className="bg-white text-gray-800 font-semibold py-2 px-4 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="pointsAssists">Pts+Asts</option>
            <option value="assists">Assists</option>
            <option value="blocks">Blocked Shots</option>
            <option value="pointsRebounds">Pts+Rebs</option>
            <option value="pointsReboundsAssists">Pts+Rebs+Asts</option>
            <option value="stealsAndBlocks">Blks+Stls</option>
            <option value="points">Points</option>
            <option value="rebounds">Rebounds</option>
            <option value="reboundsAssists">Rebs+Asts</option>
            <option value="steals">Steals</option>
            <option value="fg3PtMade">3-PT Made</option>
            <option value="turnovers">Turnovers</option>
          </select>
          }
          <p className='text-black'>{time.month} {String(time.day).padStart(2, '0')}, {time.year} at {String(time.hour).padStart(2, '0')}:{String(time.minute).padStart(2, '0')}:{String(time.second).padStart(2, '0')} UTC</p>
        </div>
        <div className='p-4 bg-white rounded text-black shadow border grid gap-2 grid-cols-7'>
          <p>Name</p>
          <p>L10</p>
          <p>H2H</p>
          <p>2024</p>
          <p>Avg.</p>
          <p>Under</p>
          <p>Over</p>

        </div>
        <div className='flex flex-col'>
          {activeResult ? (activeResult == "NFL" ? resultNFL : resultNBA).map((item, index) => {
          if(item.projection_type == (activeResult == "NFL" ? statTypeNFL : statTypeNBA)) return ( 
            <div key={index} className="p-4 bg-white rounded text-black shadow border grid gap-2 grid-cols-7">
              <p>{item.player_name}</p>
              <p>{item.l10}</p>
              <p>{item.H2H}</p>
              <p>{item["Current Season"]}</p>
              <p>{item.Average.toFixed(3)}</p>
              <p>{item.under}</p>
              <p>{item.over}</p>
            </div>
          )}) : null}
        </div>
      </div>
    </div>
  );
};

export default App; 