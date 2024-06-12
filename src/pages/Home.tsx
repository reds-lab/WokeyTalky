import React from 'react';
import QuickGlance from './QuickGlance';
import Overview from './Overview';
import Results from './Results';
import Examples from './Examples';
import EthicsAndDisclosure from './Ethics';
import Hero from './Hero';
import Citation from './Citation';
const Home: React.FC = () => {
  return (
    <>
      <Hero/>
      <QuickGlance />
      <Overview />
      <Results />
      <Examples />
      <EthicsAndDisclosure />
      <Citation/>
    </>
  );
};

export default Home;