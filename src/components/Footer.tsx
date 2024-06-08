import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Footer.css';

function Footer() {
  return (
    <footer className="footer">
        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} ReDS Lab. All rights reserved.</p>
        </div>
    </footer>
  );
}

export default Footer;