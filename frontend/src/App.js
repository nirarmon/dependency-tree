import React, { useState } from 'react';
import { Tree } from "react-arborist";
import './App.css';

// The Node component is the render prop for the Tree.
// It receives the node object and can use its state to render the UI.
const Node = ({ node, style, dragHandle }) => {
  return (
    <div style={style} ref={dragHandle} onClick={() => node.toggle()}>
      <span>
        {node.isLeaf ? "📄" : node.isOpen ? "📂" : "📁"}
      </span>
      &nbsp;
      <span>{node.data.name}</span>
    </div>
  );
};

// Recursive function to add a unique ID to each node in the tree,
// which is a requirement for the react-arborist library.
let idCounter = 0;
function addId(node) {
  node.id = (idCounter++).toString();
  if (node.children) {
    node.children.forEach(addId);
  }
}

function App() {
  const [packageName, setPackageName] = useState('');
  const [version, setVersion] = useState('latest');
  const [dependencyTree, setDependencyTree] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = () => {
    setLoading(true);
    setError(null);
    setDependencyTree(null);

    fetch(`/packages?package=${packageName}&version=${version}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        if (data && data.name) {
          idCounter = 0; // Reset counter for each new tree
          addId(data);
          setDependencyTree(data);
        } else {
          setDependencyTree(null);
        }
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching dependency tree:', error);
        setError('Failed to fetch dependency tree. Check the package name and version.');
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
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
        <div className="dependency-tree-container">
          {loading && <p>Loading...</p>}
          {error && <p className="error">{error}</p>}
          {dependencyTree && (
            <Tree
              initialData={[dependencyTree]}
              width={800}
              height={1000}
              indent={24}
              rowHeight={32}
            >
              {Node}
            </Tree>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
