import React, { useState } from 'react';
import './App.css';

function App() {
  const [packageName, setPackageName] = useState('');
  const [version, setVersion] = useState('latest');
  const [dependencyTree, setDependencyTree] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = () => {
    setLoading(true);
    fetch(`/packages?package=${packageName}&version=${version}`)
      .then(response => response.text())
      .then(data => {
        setDependencyTree(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching dependency tree:', error);
        setLoading(false);
      });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>NPM Dependency Tree Viewer</h1>
      </header>
      <main>
        <div className="search-container">
          <input
            type="text"
            placeholder="Package name"
            value={packageName}
            onChange={e => setPackageName(e.target.value)}
          />
          <input
            type="text"
            placeholder="Version (e.g., latest, 1.0.0)"
            value={version}
            onChange={e => setVersion(e.target.value)}
          />
          <button onClick={handleSearch} disabled={loading}>
            {loading ? 'Loading...' : 'Search'}
          </button>
        </div>
        <div
          className="dependency-tree-container"
          dangerouslySetInnerHTML={{ __html: dependencyTree }}
        />
      </main>
    </div>
  );
}

export default App;