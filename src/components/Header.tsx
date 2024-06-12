import { useState } from 'react';
import '../styles/Header.css';

function Header() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <header className="header">
      <div className="header-container">
        <h1 className="header-title">
          <span className="header-title-bold">Wokey</span>Talky
        </h1>
        <nav className={`header-nav ${isOpen ? 'open' : ''}`}>
          <ul className="header-nav-list">
            <li><a href="#quick-glance">A Quick Glance</a></li>
            <li><a href="#overview">Overview</a></li>
            <li><a href="#results">Results</a></li>
            <li><a href="#examples">Examples</a></li>
            <li><a href="#ethics-and-disclosure">Ethics and Disclosure</a></li>
          </ul>
        </nav>
        <div className="hamburger" onClick={toggleMenu}>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
        </div>
      </div>
    </header>
  );
}

export default Header;