import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Layout } from './components/Layout';
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Tournaments } from './pages/Tournaments';
import { TournamentDetails } from './pages/TournamentDetails';
import { Leaderboard } from './pages/Leaderboard';
import { PlayerStats } from './pages/PlayerStats';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="tournaments" element={<Tournaments />} />
            <Route path="tournaments/:id" element={<TournamentDetails />} />
            <Route path="leaderboard" element={<Leaderboard />} />
            <Route path="stats" element={<PlayerStats />} />
            <Route path="stats/:userId" element={<PlayerStats />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
