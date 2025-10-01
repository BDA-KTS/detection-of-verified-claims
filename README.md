# SimBa: Lexical and Semantic Similarity Based Detection of Verified Claims

## Description

This method receives an input claim/sentence (called "query"), searches a registry of fact-checked claims and returns fact-checks for similar claims. More precisely, SimBa computes the queries' similarity with ~40.000 english fact-checked claims from ClaimsKG and returns a set of ranked claims, their relevance scores, veracity ratings and the corresponding fact-check sources.

This method facilitates fact-checking of arbitrary claims or statements (e.g. taken from online discourse and social media posts). It takes advantage of a unique and constantly updated repository of fact-checked claims mined from the web (ClaimsKG).

ClaimsKG is a structured knowledge base (KB) which serves as a registry of claims. The KB is updated at regular intervals. The latest release of ClaimsKG contains 74000 claims collected from 13 different fact-checking websites. For more details regarding ClaimsKG, please refer to the official webpage [https://data.gesis.org/claimskg/](https://data.gesis.org/claimskg/)

## Use Cases

1. **Veracity Verification**: Check whether a set of statements have already been fact-checked before. SimBa can be used on these statements to find existing fact-checks, including who performed the checks and when they were done.
2. **Check-Worthiness Analysis**: Find out which claims have been fact-checked before and which have not to gain information on perceived check-worthiness of statements
3. **Information Spread Analysis**: Find claims that are semantically similar to claims that have been previously fact-checked to analyze information spread

## Input Data

The required input consists of an input query file `data/<dataset>/queries.tsv`: a text file in .tsv format (tab-separated) containing one query per line. One query consists of an ID and a claim. For each of the claims, SimBa will retrieve the most similar fact-checked claims in ClaimsKG.

Example of [`data/sample/queries.tsv`](data/sample/queries.tsv):
```
1	Covid-19 vaccines increase the risk of dying from the new Covid-19 variants
```

Optional input data: If desired, a different corpus than ClaimsKG can be supplied as database (by exchanging [`data/claimsKG/corpus.tsv`](data/claimsKG/corpus.tsv)). The corpus file must be in tab-separated format (`.tsv`) and must contain the following columns:

| Column | Description |
|--------|-------------|
| qid | A unique identifier for the claim |
| text | The textual content of the claim |
| title | The title of the fact-checking review |
| url | A link to the fact-checking article |
| rating | The fact-checking assessment of the claim (e.g., true, false, half false, etc.) |

If available, a goldstandard file can be supplied which lists the optimal results. For example, SimBa can be evaluated directly on the CLEF CheckThat! data using the respective datasets and gold files.You can also use the same evaluation scripts to evaluate SimBa’s performance on your *own data*, provided you supply a goldstandard file (`gold.tsv`) in the same folder as your input claims file (e.g., `data/<dataset>/gold.tsv`).

## Output Data

The outputs are exported to two files, with one retrieved claim per row:

### 1. CheckThat! Output File: [`data/sample/pred_qrels.tsv`](data/sample/pred_qrels.tsv)

Contains the results in the tab-separated format of the [CheckThat! competition (detecting previously fact-checked claims)](https://ceur-ws.org/Vol-3180/paper-29.pdf) with the following columns (no header):

| Query ID | Q0 | Claim ID | Rank | Similarity Score | Method Name |
|----------|----|---------:|-----:|-----------------:|-------------|
| 1 | Q0 | http://data.gesis.org/claimskg/creative_work/4a27c731-c9a3-5ff6-81b3-cd46845d5ef9 | 1 | 51.24902489669692 | SimBa |

### 2. Client-Friendly Output File: [`data/sample/pred_client.tsv`](data/sample/pred_client.tsv)

Contains a more readable format with the following columns:

| Query | VClaim | ClaimReviewURL | Rating | Similarity |
|-------|--------|----------------|--------|------------|
| Covid-19 vaccines increase the risk of dying from the new Covid-19 variants | Vaccinated people are more susceptible to Covid-19 variants | https://factcheck.afp.com/http%253A%252F%252Fdoc.afp.com%252F9PB64D-1 | b'False' | 51.24902489669692 |
| Covid-19 vaccines increase the risk of dying from the new Covid-19 variants | Covid-19 vaccines will leave people exposed to deadly illness during the next cold and flu season and germ theory is a hoax | https://factcheck.afp.com/covid-19-shots-not-designed-increase-cold-flu-lethality | b'False' | 51.102840014017175 |
| Covid-19 vaccines increase the risk of dying from the new Covid-19 variants | Getting the first dose of Covid-19 vaccine increases risk of catching the novel coronavirus | https://factcheck.afp.com/misleading-facebook-posts-claim-covid-19-vaccine-increases-risk-catching-novel-coronavirus | b'Misleading' | 50.774385556493115 |
| Covid-19 vaccines increase the risk of dying from the new Covid-19 variants | People vaccinated against Covid-19 pose a health risk to others by shedding spike proteins | https://factcheck.afp.com/covid-19-vaccine-does-not-make-people-dangerous-others | b'False' | 49.87148066707767 |
| Covid-19 vaccines increase the risk of dying from the new Covid-19 variants | Mass vaccination will cause monster Covid-19 variants | https://factcheck.afp.com/mass-covid-19-vaccination-will-not-lead-out-control-variants | b'False' | 49.756611441979224 |

------------------------------------------------------------------------

## Hardware Requirements

The method requires higher hardware specifications for optimal performance. Below is the recommended machine configuration:

- **CPU**: 8-core x86 CPU (e.g., Intel Core i7/i9 or AMD Ryzen 7/9)
- **GPU**: NVIDIA GPU with at least 4GB VRAM (e.g., NVIDIA RTX 2000 or higher. Not compulsory but important for faster operations)
- **RAM**: 8 GB or more
- **Storage**: 256 GB SSD (for faster read/write operations) + 256 GB HDD (for additional storage)

**Note**: While the above specifications are recommended for optimal performance, SimBa can still run on more modest hardware (without GPU, 2 GB of RAM) when the existing version of ClaimsKG is used (see the `-c` option at [How to Use](#how-to-use)). It has been successfully tested on a virtual machine with limited resources, though processing times will be significantly longer.

## Environment Setup

This version of SimBa has been tested with **Python 3.11.13** on Windows. Using other Python versions and/or operating systems might require other package versions.

- If you have no Python installation, download it from the [official Python website](https://www.python.org/downloads/release/python-31113/). During installation, make sure to check the box that says "Add Python to PATH" to ensure that Python and pip (Python's package manager) are available in your terminal or command prompt. Verfiy your installation using `python --version`.
- Install dependencies using
  ```bash
  pip install -r requirements.txt
  ```

## How to Use

Once everything is installed, you can run the SimBa project. To do so, use the following command in the terminal:

To run the queries in [`data/sample/queries.tsv`](data/sample/queries.tsv) against unchanged ClaimsKG, run 

```bash
python main.py sample -c
```

To use your own corpus, exchange `sample` for the directory name of your dataset (see [Input Data](#input-data)). In this case, you can not use the [pre-computed embeddings](data/cache/claimsKG/). Generate new embeddings by not using the `-c` option the first time. Also the embeddings for the queries are stored and later re-used when `-c` is used. After you changed the queries, delete the stored embedding in `data/cache/<dataset>`.

The results are written to the folder of your dataset, see [Output Data](#output-data):  

## Technical Details

SimBa is fully unsupervised, i.e. it does not need any training data. It operates in two steps:

1. **Candidate Retrieval**: The semantically most similar claims are retrieved as candidates. Semantic similarity is computed using sentence embeddings.
2. **Re-Ranking**: A computationally more costly re-ranking step is applied to all candidates in order to find the best matches. Again, sentence embeddings combined with a lexical feature are used.

SimBa was evaluated on the [CLEF CheckThat! Lab Task 2 Claim Retrieval challenge](https://checkthat.gitlab.io/clef2022/) data and achieved the following scores:

| Dataset | Map@1 | Map@3 | Map@5 |
|---------|-------|-------|-------|
| 2020 2a English | 0.9425 | 0.9617 | 0.9617 |
| 2021 2a English | 0.9208 | 0.9431 | 0.9450 |
| 2021 2b English | 0.4114 | 0.4388 | 0.4414 |
| 2022 2a English | 0.9043 | 0.9258 | 0.9258 |
| 2022 2b English | 0.4462 | 0.4744 | 0.4805 |

## References

- Hövelmeyer, Alica, Katarina Boland, and Stefan Dietze. 2022. *SimBa at CheckThat! 2022: Lexical and Semantic Similarity-Based Detection of Verified Claims in an Unsupervised and Supervised Way.* In: CEUR Workshop Proceedings, Vol. 3180, pp. 511–531. [PDF](https://ceur-ws.org/Vol-3180/paper-40.pdf)

- Boland, Katarina, Hövelmeyer, Alica, Fafalios, Pavlos, Todorov, Konstantin, Mazhar, Usama, & Dietze, Stefan. 2023. *Robust and Efficient Claim Retrieval for Online Fact-Checking Applications.* Preprint. [DOI](https://doi.org/10.21203/rs.3.rs-3007151/v1)

## Contact Details

For further assistance or inquiries, please contact: katarina.boland@hhu.de

