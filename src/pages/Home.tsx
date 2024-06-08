// src/pages/Home.jsx

import React from 'react';
import {Outlet} from "react-router-dom";
function Home() {
  return (
    <div>
      <p></p>
      <Outlet/>
    </div>
  );
}

export default Home;