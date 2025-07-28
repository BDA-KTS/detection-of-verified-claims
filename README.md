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

The required input consists of an input query file [`data/sample/queries.tsv`](data/sample/queries.tsv): a text file in .tsv format (tab-separated) containing one query per line. One query consists of an ID and a claim. For each of the claims, SimBa will retrieve the most similar fact-checked claims in ClaimsKG.

Example of [`data/sample/queries.tsv`](data/sample/queries.tsv):
```
1	Covid-19 vaccines increase the risk of dying from the new Covid-19 variants
```

Optional input data: If desired, a different corpus than ClaimsKG can be supplied as database ([`data/claimsKG/corpus.tsv`](data/claimsKG/corpus.tsv)).

This file should be in tab-separated format (`.tsv`) and must follow the structure below:

Format of [`corpus.tsv`](data/claimsKG/corpus.tsv)

The file should contain the following columns:

| Column | Description |
|--------|-------------|
| Claim ID | A unique identifier for the claim |
| Claim Text | The textual content of the claim |
| Claim Review Title | The title of the fact-checking review |
| Claim Review URL | A link to the fact-checking article |
| Rating | The fact-checking assessment of the claim (e.g., true, false, half false, etc.) |

If available, a goldstandard can be supplied which lists the optimal results ([`data/sample/gold.tsv`](data/sample/gold.tsv)). This can be used to evaluate SimBa's performance using the evaluation scripts of the [CLEF CheckThat! Lab Task 2 Claim Retrieval challenge](https://checkthat.gitlab.io/clef2022/).

## Output Data

The outputs are exported to two files:

### 1. Standard Output File: [`data/sample/sample.tsv`](data/sample/sample.tsv)

Contains the results in a tab-separated format with the following columns:

| Query ID | Q0 | Claim ID | Rank | Similarity Score | Method Name |
|----------|----|---------:|-----:|-----------------:|-------------|
| 1 | Q0 | http://data.gesis.org/claimskg/creative_work/1a0db2a7-fd8b-51ad-a89a-dd644da31ad8 | 1 | 45.55524233523532 | SimBa |

### 2. Client-Friendly Output File: [`data/sample/pred_client.tsv`](data/sample/pred_client.tsv)

Contains a more readable format with the following columns:

| Query | VClaim | ClaimReviewURL | Rating | Similarity |
|-------|--------|----------------|--------|------------|
| Covid-19 vaccines increase the risk of dying from the new Covid-19 variants | Getting the first dose of Covid-19 vaccine increases risk of catching the novel coronavirus | https://factcheck.afp.com/misleading-facebook-posts-claim-covid-19-vaccine-increases-risk-catching-novel-coronavirus | b'Misleading' | 45.55524233523532 |
| Covid-19 vaccines increase the risk of dying from the new Covid-19 variants | People vaccinated against Covid-19 pose a health risk to others by shedding spike proteins | https://factcheck.afp.com/covid-19-vaccine-does-not-make-people-dangerous-others | b'False' | 43.15199331134423 |
| Covid-19 vaccines increase the risk of dying from the new Covid-19 variants | Vaccinated people are 885% more likely to die of Covid-19 than unvaccinated people | https://factcheck.afp.com/http%253A%252F%252Fdoc.afp.com%252F9JE74M-2 | b'False' | 42.53184410315937 |
| Covid-19 vaccines increase the risk of dying from the new Covid-19 variants | In the United Kingdom, 70-plus percent of the people who die now from COVID are fully vaccinated. | https://www.politifact.com/factchecks/2021/oct/29/alex-berenson/covid-19-death-rate-england-much-higher-among-unva/ | FALSE | 42.506568861739346 |
| Covid-19 vaccines increase the risk of dying from the new Covid-19 variants | Only the fully vaccinated should fear the new 'worst ever' Covid-19 variant; data shows they already account for 4 in every 5 Covid deaths | https://www.politifact.com/factchecks/2021/dec/07/blog-posting/article-misleads-dangers-omicron-variant-using-uk-/ | FALSE | 42.1289266007539 |

------------------------------------------------------------------------

## Hardware Requirements

The method requires higher hardware specifications for optimal performance. Below is the recommended machine configuration:

- **CPU**: 8-core x86 CPU (e.g., Intel Core i7/i9 or AMD Ryzen 7/9)
- **GPU**: NVIDIA GPU with at least 4GB VRAM (e.g., NVIDIA RTX 2000 or higher. Not compulsory but important for faster operations)
- **RAM**: 8 GB or more
- **Storage**: 256 GB SSD (for faster read/write operations) + 256 GB HDD (for additional storage)

**Note**: While the above specifications are recommended for optimal performance, SimBa can still run on more modest hardware. It has been successfully tested on a virtual machine with limited resources, though processing times will be significantly longer. The `-c` cache option becomes particularly helpful when working with limited hardware.

## Environment Setup

This version of SimBa has been tested with **Python 3.11.13** on Windows. Using other Python versions and/or operating systems might require other package versions.

Follow the steps below to install SimBa on your system using the recommended setup.

### 1. Install Python (Version 3.11.13)

- **Download Python 3.11.13** from the official Python website:  
   [https://www.python.org/downloads/release/python-31113/](https://www.python.org/downloads/release/python-31113/).

- **Install Python**:
    - **During installation**, make sure to **check the box** that says **"Add Python to PATH"**. This step is crucial, as it ensures that Python and pip (Python's package manager) are available in your terminal or command prompt.
    - Follow the on-screen instructions to complete the installation.

- **Verify the Installation**: 
    After installation, open your terminal (or command prompt) and type the following command to check if Python was installed correctly:
    ```bash
    python --version
    ```

### 2. Clone the Repository and Navigate to the Main Project Directory

To download SimBa, clone the repository from GitHub.

Run the following commands in your terminal or command prompt:

```bash
git clone <repository-url>
cd <repository name>
```

### 3. Install Required Dependencies and Data

SimBa's required libraries and dependencies are listed in the requirements.txt file. Install them using the following command:

```bash
pip install -r requirements.txt
```


## How to Use

Once everything is installed, you can run the SimBa project. To do so, use the following command in the terminal:

```bash
python main.py sample
```

Or more generally:

```bash
python main.py <dataset name>
```

**Parameters:**
- `<dataset name>`: A custom name for your input query dataset (e.g., "sample"). SimBa will automatically look for the input file at `data/<dataset name>/queries.tsv`.

This will use the ClaimsKG database to find fact-checked claims that are similar to your input queries.

### Using Cache for Efficiency

For increased efficiency, SimBa generates embeddings for the claims in each database only once and stores them in a cache for re-use. To use this cache, if it already exists, supply the `-c` option:

```bash
python main.py <dataset name> -c
```


**⚠️ Important**: Please make sure that when you use the cache, you did not generate it for a different database that you had given the same name!

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
