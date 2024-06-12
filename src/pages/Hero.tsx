import React from 'react';
import '../styles/Hero.css';
const Hero: React.FC = () => {
  return (
    <div className="hero-container">
      <div className="hero-content">
        <h1 className="hero-title">
        WOKEYTALKY: <br />Towards Scalable Evaluation of
Misguided Safety Refusal in LLMs
        </h1>
        <p className="hero-tldr">
          TLDR: We introduce WOKEYTALKY, an automated pipeline that generates false refusal benchmarks to assess and mitigate incorrect safety refusals in large language models caused by spurious associations learned during training.
        </p>
        <div className="hero-authors">
          <p>Yi Zeng<sup>1*</sup>, Adam Nguyen<sup>1*</sup>,Ruoxi Jia<sup>1†</sup>, Bo Li<sup>2†</sup></p>
          <p><sup>1</sup>Virginia Tech <sup>2</sup>University of Chicago</p>
          <p>Lead Authors <sup>*</sup>Equal Advising<sup>†</sup></p>
        </div>
        <div className="hero-links">
          <a href="path_to_paper" className="hero-link">Paper</a>
          <a href="path_to_taxonomy" className="hero-link">Persuasion Taxonomy</a>
        </div>
      </div>
    </div>
  );
};

export default Hero;