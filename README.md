<h1 align='center' style="text-align:center; font-weight:bold; font-size:2.0em;letter-spacing:2.0px;"> WokeyTalky:
Towards Scalable Evaluation of
Misguided Safety Refusal in LLMs </h1>

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

------------
## Quickstart
### Install (Option #1)

To quickly use WokeyTalky in a notebook or python code, you can install our Pipeline with `pip`:

```bash
pip install WokeyTalky
```

Further documentation

### Use our original code

Go step by step through our WokeyTalky process with the original code used to generate our HuggingFace dataset
Clone or download this repository:

```bash
git clone git@github.com:reds-lab/WokeyTalky.git
```

Install the dependencies:

```bash
conda install env.yml
```

Then run TimberTrek:

```bash
./start_pipeline.sh
```




<br>
<br>

## Introduction

**TLDR:** WokeyTalky is a scalable pipeline that generates test data to evaluate the spurious correlated safety refusal of foundation models through a systematic approach.

<br>

**What did we introduce?** A taxonomy with 40 persuasion techniques to help you be more persuasive!

**What did we find?** By iteratively applying diffrent persuasion techniques in our taxonomy, we successfully jailbreak advanced aligned LLMs, including Llama 2-7b Chat, GPT-3.5, and GPT-4 — achieving an astonishing **92%** attack success rate, notably **without any specified optimization**.

Now, you might think that such a high success rate is the peak of our findings, but there's more. In a surprising twist, we found that **more advanced models like GPT-4 are more vulnerable** to persuasive adversarial prompts (PAPs). What's more, **adaptive defenses** crafted to neutralize these PAPs also provide effective protection against a spectrum of other attacks (e.g., [GCG](https://llm-attacks.org/), [Masterkey](https://sites.google.com/view/ndss-masterkey), or [PAIR](https://jailbreaking-llms.github.io/)).

<p align="center">
<img src="./assets/persuasion_taxonomy.png" alt="persuasion_taxonomy" width="90%"/>
</p>
<p align="center">
<font size=3 >A systematic taxonomy of persuasion techniques.</font>
</p>
<br>

<br>

## A Quick Glance
<img src="./assets/0evQd-adv-bench-rejection-rates.png" alt="generation method" width="90%"/>
<img src="./assets/3vZpY-hex-phi-rejection-rates.png" alt="generation method" width="90%"/>
<br>
<br>

## ***Persuasive Adversarial Prompt (PAP)***

> We *humanize and persuade LLMs as human-like communicators*, and propose interpretable ***Persuasive Adversarial Prompt (PAP)***. PAP seamlessly weaves persuasive techniques into jailbreak prompt construction, which highlights the risks associated with more complex and nuanced human-like communication to advance AI safety.

<br>

<p align="center">
<img src="./assets/auto_attack_new_weiyan.png" alt="generation method" width="90%"/>
</p>
<p align="center">
<font size=3 >Overview of the taxonomy-guided Persuasive Adversarial Prompt (PAP) generation method.</font>
</p>

<br>

**A. *Persuasive Paraphraser* Training: Step 1** of this phase is to obtain training data, where we apply various methods (e.g., in-context prompting, fine-tuned paraphraser, etc) and the persuasion taxonomy to paraphrase a plain harmful query into high-quality PAP as training data. Then, in **Step 2,** we use the training data to fine-tune a *persuasive paraphraser* that can paraphrase harmful queries stably. 

**B. *Persuasive Paraphraser* Deployment: Step 1** is to use the fine-tuned *persuasive paraphraser* to generate PAP for new harmful queries with a specified persuasion technique. Then, in **Step 2,** we will use a [GPT4-Judge](https://llm-tuning-safety.github.io/index.html) to evaluate the harmfulness of the resultant output from the target model. 

<br>



<div class="columns is-centered">
    <div class="column">
        <div class="content">
            <h2 class="title is-4">Case Study 1</h2>
            <div class="content has-text-justified">
                <p>
                    The adaptive nature of WOKEYTALKY enables exciting new use cases and functionalities beyond serving as a static benchmark. Through this case study, we demonstrate that dynamically generated “Woke” data from WOKEYTALKY provides timely identification of safety mechanism-dependent incorrect refusals. We fine-tuned a helpfulness-focused model, Mistral-7B-v0.1, on 50 random samples from AdvBench, introducing safety refusal behaviors. The evaluation compared the model’s safety on AdvBench samples and incorrect refusal rate on WOKEYTALKY data versus static benchmarks like XSTest.
                </p>
            </div>
            <br>
            <img src="./assets/Case1.png" alt="Case Study 1 Image">
        </div>
    </div>
</div>
<br>


<div class="columns is-centered">
    <div class="column">
        <div class="content">
            <h3 class="title is-4">Case Study 2</h3>
            <div class="content has-text-justified">
                <p>
                    In this case study, we explore using WOKEYTALKY data for few-shot mitigation of incorrect refusals. We split the WOKEYTALKY and XSTest-63 data into train/test sets and compared different fine-tuning methods. Our findings show that incorporating WOKEYTALKY samples effectively mitigates wrong refusals while maintaining high safety refusal rates. Model 1, using WOKEYTALKY data, demonstrated generalizable mitigation on unseen data, outperforming models trained with larger benign QA samples or XSTest samples. This highlights the potential of WOKEYTALKY data in balancing performance, safety, and incorrect refusals in AI safety applications.
                </p>
            </div>
            <img src="./assets/Case2.png" style="width:95%;height:95%;" alt="Case Study 2 Image">
        </div>
    </div>
</div>




<br><br>

## Ethics and Disclosure

The development and application of WOKEYTALKY have been guided by a commitment to ethical standards and transparency. The pipeline's primary aim is to enhance the safety and reliability of AI systems by addressing the issue of incorrect refusals and improving model alignment with human values. We acknowledge the potential implications of our work in various domains and have taken measures to ensure that our research is conducted responsibly.

Our methodology includes the use of red-teaming datasets specifically designed to expose and mitigate safety risks. These datasets, such as HEx-PHI and AdvBench, are employed with the intention of identifying and correcting spurious features that lead to misguided refusals in language models. All data used in our experiments is sourced from publicly available benchmarks, and no private or sensitive data is included.

We recognize that the dynamic generation of test cases (Woke-data) and the evaluation of models on these cases can raise concerns about the potential misuse of our findings. To mitigate such risks, we have ensured that all experimental procedures and results are documented transparently, and our code and methodologies are made available for peer review and verification. We encourage collaboration and open dialogue within the research community to refine and improve our approaches.

In addition, we are committed to the principles of fairness, accountability, and transparency. Our evaluations aim to highlight the importance of context-aware AI systems that can distinguish between harmful and benign requests accurately. We stress that our work should not be used to bypass or undermine safety mechanisms but rather to strengthen them.

Finally, we disclose that the WOKEYTALKY project has been supported by funding from [specific funding sources, if any], and we have adhered to the ethical guidelines and standards set forth by our institution. We invite feedback and collaboration from the broader AI research community to ensure that our contributions to AI safety are both impactful and responsibly managed.
<br>
<br>

## License

The software is available under the [MIT License](https://github.com/reds-lab/WokeyTalky/blob/master/LICENSE).

## Contact

If you have any questions, feel free to [open an issue](https://github.com/reds-lab/WokeyTalky/issues/new) or contact [Adam Nguyen]().

## Special Thanks to [BLANK]


