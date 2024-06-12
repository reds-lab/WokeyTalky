import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import './App.css';
import About from './pages/About';
import ArenaBattle from './pages/ArenaBattle';
import Home from './pages/Home';
import Leaderboard from './pages/Leaderboard';
import Header from "./components/Header";
import Footer from "./components/Footer";
function App() {
  return (
    <>
      <Header/>
      <Home/>
      <Footer/>
    </>
  );
}

export default App;
