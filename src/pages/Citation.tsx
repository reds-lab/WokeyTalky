import React, { useState } from 'react';
import "../styles/Citation.css";

const Citation: React.FC = () => {
  const [copied, setCopied] = useState(false);

  const citation = `@misc{zeng2024johnny,
  title={How Johnny Can Persuade LLMs to Jailbreak Them: Rethinking Persuasion to Challenge AI Safety by Humanizing LLMs},
  author={Zeng, Yi and Lin, Hongpeng and Zhang, Jingwen and Yang, Diyi and Jia, Ruoxi and Shi, Weiyan},
  year={2024},
  eprint={2401.06373},
  archivePrefix={arXiv},
  primaryClass={cs.CL}
}`;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(citation);
    setCopied(true);
    setTimeout(() => {
      setCopied(false);
    }, 2000);
  };

  return (
    <div className="citation">
      <p>BibTeX</p>
      <p>If you find our project useful, please consider citing:</p>
      <pre>
        <code>{citation}</code>
      </pre>
      <button onClick={copyToClipboard}>
        {copied ? 'Copied!' : 'Copy Citation'}
      </button>
    </div>
  );
};

export default Citation;