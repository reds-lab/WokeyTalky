<h1 align='center' style="text-align:center; font-weight:bold; font-size:2.0em;letter-spacing:2.0px;">WokeyTalky:
Towards Scalable Evaluation of Misguided Safety Refusal in LLMs</h1>

<p align='center' style="text-align:center;font-size:1.25em;">
    <a href="https://www.yi-zeng.com/" target="_blank" style="text-decoration: none;">Yi Zeng<sup>1,*</sup></a>&nbsp;,&nbsp;
    <a href="https://adamnguyen.dev/" target="_blank" style="text-decoration: none;">Adam Nguyen<sup>1,*</sup></a>&nbsp;,&nbsp;
    <a href="https://wyshi.github.io/" target="_blank" style="text-decoration: none;">Bo Li<sup>2</sup></a>&nbsp;&nbsp;
    <a href="https://ruoxijia.info/" target="_blank" style="text-decoration: none;">Ruoxi Jia<sup>1</sup></a>&nbsp;,&nbsp;
    <br/> 
    <sup>1</sup>Virginia Tech&nbsp;&nbsp;&nbsp;<sup>2</sup>University of Chicago&nbsp;&nbsp;&nbsp;
  <sup>*</sup>Lead Authors&nbsp;&nbsp;&nbsp;&nbsp;
</p>
<p align='center';>
<b>
<em>arXiv-Preprint, 2024</em> <br>
</b>
</p>
<p align='center' style="text-align:center;font-size:2.5 em;">
<b>
    <a href="" target="_blank" style="text-decoration: none;">[arXiv] TBD </a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://reds-lab.github.io/WokeyTalky/" target="_blank" style="text-decoration: none;">[Project Page]</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://huggingface.co/datasets/redslabvt/WokeyTalky" target="_blank" style="text-decoration: none;">[HuggingFace]</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://pypi.org/project/WokeyTalky/" target="_blank" style="text-decoration: none;">[PyPI]</a>
</b>
</p>

## Notebook Demos

Explore our notebooks on various platforms like Jupyter Notebook/Lab, Google Colab, and VS Code Notebook.

Check out four demo notebooks below.

| Jupyter Lite | Binder | Google Colab | Github Jupyter File |
|:---:|:---:|:---:|:---:|
| [![Lite](https://gist.githubusercontent.com/xiaohk/9b9f7c8fa162b2c3bc3251a5c9a799b2/raw/a7fca1d0a2d62c2b49f60c0217dffbd0fe404471/lite-badge-launch-small.svg)](https://poloclub.github.io/timbertrek/notebook) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/poloclub/timbertrek/master?urlpath=lab/tree/notebook-widget/example/campas.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]() | [![Try on your system]()]() |

## Quickstart

### Installation (Under Development TBD)

To quickly use WokeyTalky in a notebook or Python code, install our pipeline with `pip`:

```bash
pip install WokeyTalky
```

```python
from WokeyTalky import WokePipeline

woke = WokePipeline()
```

Further documentation [Here](https://LINK)

### Use our Original Code

To go step by step through our WokeyTalky process using the original code that generated our HuggingFace dataset, clone or download this repository:
1. **Clone the Repository:**
   ```bash
   git clone git@github.com:reds-lab/WokeyTalky.git
   cd WokeyTalky/WokeyTalky_Research_Code
   ```

2. **Create a New Conda Environment and Activate It:**
   ```bash
   conda create -n wokeytalky python=3.9
   conda activate wokeytalky
   ```

3. **Install Dependencies Using `pip`:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run WokeyTalky's Main Bash Script:**
   ```bash
   ./setup.sh
   ```

5. **Further Documentation:**
   Reference to additional documentation within the repository:
   ```markdown
   For more detailed instructions and further documentation, please refer to the [documentation folder](./docs/README.md) inside the repository.
## Introduction

**TL;DR:** WokeyTalky is a scalable pipeline that generates test data to evaluate the spurious correlated safety refusal of foundation models through a systematic approach.

**What did we introduce?** A taxonomy with 40 persuasion techniques to help enhance persuasion skills.

**What did we find?** By iteratively applying different persuasion techniques from our taxonomy, we successfully jailbreak advanced aligned LLMs, including Llama 2-7b Chat, GPT-3.5, and GPT-4, achieving a 92% attack success rate, notably without any specified optimization.

Interestingly, we found that advanced models like GPT-4 are more vulnerable to persuasive adversarial prompts (PAPs). Adaptive defenses crafted to neutralize these PAPs also provide effective protection against a spectrum of other attacks (e.g., [GCG](https://llm-attacks.org/), [Masterkey](https://sites.google.com/view/ndss-masterkey), or [PAIR](https://jailbreaking-llms.github.io/)).

## A Quick Glance
<img src="./assets/0evQd-adv-bench-rejection-rates.png" alt="Rejection Rates" width="90%"/>
<img src="./assets/3vZpY-hex-phi-rejection-rates.png" alt="Rejection Rates" width="90%"/>

## Case Studies

### Case Study 1

The adaptive nature of WOKEYTALKY enables dynamic use cases and functionalities beyond serving as a static benchmark. In this case study, we demonstrate that dynamically generated “Woke” data from WOKEYTALKY provides timely identification of safety mechanism-dependent incorrect refusals. We fine-tuned a helpfulness-focused model, Mistral-7B-v0.1, on 50 random samples from AdvBench, introducing safety refusal behaviors. The evaluation compared the model’s safety on AdvBench samples and its incorrect refusal rate on WOKEYTALKY data versus static benchmarks like XSTest.

<img src="./assets/Case1.png" alt="Case Study 1 Image" width="95%"/>

### Case Study 2

In this case study, we explore using WOKEYTALKY data for few-shot mitigation of incorrect refusals. We split the WOKEYTALKY and XSTest-63 data into train/test sets and compared different fine-tuning methods. Our findings show that incorporating WOKEYTALKY samples effectively mitigates wrong refusals while maintaining high safety refusal rates. Model 1, which used WOKEYTALKY data, demonstrated generalizable mitigation on unseen data, outperforming models trained with larger benign QA samples or XSTest samples. This highlights the potential of WOKEYTALKY data in balancing performance, safety, and incorrect refusals in AI safety applications.

<img src="./assets/Case2.png" alt="Case Study 2 Image" width="95%"/>

## Ethics and Disclosure

The development and application of WOKEYTALKY adhere to high ethical standards and principles of transparency. Our primary aim is to enhance AI system safety and reliability by addressing incorrect refusals and improving model alignment with human values. The pipeline employs red-teaming datasets like HEx-PHI and AdvBench to identify and correct spurious features causing misguided refusals in language models. All data used in experiments is sourced from publicly available benchmarks, ensuring the exclusion of private or sensitive data.

We acknowledge the potential misuse of our findings and have taken measures to ensure ethical conduct and responsibility. Our methodology and results are documented transparently, and our code and methods are available for peer review. We emphasize collaboration and open dialogue within the research community to refine and enhance our approaches.

We stress that this work should strengthen safety mechanisms rather than bypass them. Our evaluations aim to highlight the importance of context-aware AI systems that can accurately differentiate harmful from benign requests.

The WOKEYTALKY project has been ethically supervised, adhering to our institution's guidelines. We welcome feedback and collaboration to ensure impactful and responsibly managed contributions to AI safety.

## License

The software is available under the [MIT License](https://github.com/reds-lab/WokeyTalky/blob/master/LICENSE).
◊
## Contact

If you have any questions, please [open an issue](https://github.com/reds-lab/WokeyTalky/issues/new) or contact [Adam Nguyen]().

## Special Thanks 

Help us improve this readme. Any suggestions and contributions are welcome.
