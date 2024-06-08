import React from 'react';
import '../styles/About.css';

function About() {
  return (
    <div className="about-container">
      <h2>About Us</h2>
      <p>
        [Your Project Name] is an open-source research project developed by [Your Team/Organization].
        Our mission is to [brief description of your project's mission or goal].
        We open-source our [relevant projects or datasets] on GitHub and invite everyone to join us!
      </p>

      <h3>Our Team</h3>
      <ul>
        <li>[Team Member 1 (Role)], [Team Member 2 (Role)], [Team Member 3 (Role)], ...</li>
      </ul>

      <h3>Past Contributors</h3>
      <ul>
        <li>[Contributor 1], [Contributor 2], ...</li>
      </ul>

      <h3>Learn More</h3>
      <ul>
        <li>[Relevant papers, blog posts, datasets, or policies related to your project]</li>
      </ul>

      <h3>Contact Us</h3>
      <ul>
        <li>Follow us on [Social Media Platforms] or email us at [Your Email Address]</li>
        <li>File issues or contribute on GitHub</li>
        <li>Download our datasets and models on [Relevant Platforms]</li>
      </ul>

      <h3>Acknowledgments</h3>
      <p>
        We thank [Relevant Organizations, Teams, or Individuals] for their support and contributions to our project.
        We also appreciate the generous sponsorship from [Sponsors or Funding Organizations].
        Learn more about partnership opportunities [here or provide a relevant link].
      </p>

      <div className="acknowledgment-logos">
        <img src="logo1.png" alt="Logo 1" />
        <img src="logo2.png" alt="Logo 2" />
        {/* Add more logos as needed */}
      </div>
    </div>
  );
}

export default About;