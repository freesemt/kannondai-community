import React from 'react';
import Header from './components/Header';

const App: React.FC = () => {
    return (
        <div>
            <Header />
            <main>
                <h1>Welcome to the Jichikai Project</h1>
                <p>This is the main application for the Jichikai community.</p>
            </main>
        </div>
    );
};

export default App;