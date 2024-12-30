import React, { useEffect, useState } from 'react';

const App = () => {
  const [result, setResult] = useState('');
  const [statType, setStatType] = useState('passYards');

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get-best-lines');
      const data = await response.json();
      
      const combinedData = data.map(item => ({
        ...item
      }));

      console.log(data)
      setResult(combinedData);
    } catch (error) {
      setResult('Error: ' + error.message);
    }
  };


  useEffect(() => {
    fetchData()
  }, []);

  return (
    <div className="bg-gray-100 min-h-screen w-screen">
      <div className="w-5/6 mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">API Frontend</h1>
        <div className='m-2 flex gap-2'>
          <button
            onClick={fetchData}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
          >
            Fetch Data
          </button>
          <select 
            value={statType} 
            onChange={(e) => setStatType(e.target.value)}
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
          </select>
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
          {result ? result.map((item, index) => ( 
            <>
              {item.projection_type == statType && <div key={index} className="p-4 bg-white rounded text-black shadow border grid gap-2 grid-cols-7">
                <p>{item.player_name}</p>
                <p>{item.l10}</p>
                <p>{item.H2H}</p>
                <p>{item["Current Season"]}</p>
                <p>{item.Average}</p>
              </div>}
            </>
          )) : null}
        </div>
      </div>
    </div>
  );
};

export default App; 