
# Lexical and Semantic Similarity Based Detection of Verified Claims (SimBa)

This method receives an input claim/sentence (called "query"), searches a registry of fact-checked claims and returns fact-checks for similar claims. 
More precisely, SimBa computes the queries' similarity with 74000 previously fact-checked claims from ClaimsKG and returns a set of ranked claims, their relevance scores, veracity ratings and the corresponding fact-check sources. 

This method facilitates fact-checking of arbitrary claims or statements (e.g. taken from online discourse and social media posts). It takes advantage of a unique and constantly updated repository of fact-checked claims mined from the web (ClaimsKG).

ClaimsKG is a structured knowledge base (KB) which serves as a registry of claims. The KB is updated at regular intervals. The latest release of ClaimsKG contains 74000 claims collected from 13 different fact-checking websites from the year 1996 to 2023. For more details regarding ClaimsKG, please refer to the official webpage https://data.gesis.org/claimskg/

## Keywords
verified claim retrieval, semantic similarity, detection of previously fact-checked claims

## Social Science Usecase
  1. Check the veracity of claims uttered online to analyze misinformation spread
  2. Find out which claims have been fact-checked before and which have not to gain information on perceived check-worthiness of statements
  3. Find claims that are semantically similar to claims that have been previously fact-checked to analyze information spread


# SimBa Project Installation and Setup Guide

This version of SimBa has been tested with **Python 3.11.6** on Windows. Using other Python versions and/or operating systems might require other package versions. 

Follow the steps below to install SimBa on your system using the recommended setup. 

## 1. **Install Python (Version 3.11.6)**

1. **Download Python 3.11.6** from the official Python website:  
   [https://www.python.org/downloads/release/python-3116/](https://www.python.org/downloads/release/python-3116/).

2. **Install Python**:
   - **During installation**, make sure to **check the box** that says **"Add Python to PATH"**. This step is crucial, as it ensures that Python and pip (Python's package manager) are available in your terminal or command prompt.
   - Follow the on-screen instructions to complete the installation.

3. **Verify the Installation**:
   After installation, open your terminal (or command prompt) and type the following command to check if Python was installed correctly:
   ```bash
   python --version


### 2. **Clone the Repository and Navigate to the Main Project Directory**
 To download SimBa, clone the repository from GitHub.

 Run the following commands in your terminal or command prompt: 
       
       git clone <repository-url>

       cd <repository name>
    

### 3. **Install Required Dependencies and Data**
 SimBa's required libraries and dependencies are listed in the requirements.txt file. Install them using the following command:
      
      pip install -r requirements.txt

To download data required by the NLTK library, start the Python interpreter
```
    python
```

then use nltk's download method:

```
    import nltk
    nltk.download(‘stopwords’)
    nltk.download(‘punkt’)
```
Afterwards, exit the interpreter:
```
exit()
```


# How to Use
Once everything is installed, you can run the SimBa project. To do so, use the following command in the terminal:

      python main.py <dataset name>


dataset name: A custom name for your input query dataset. 
This will use the ClaimsKG database to find fact-checked claims that are similar to your input queries.  

For increased efficency, SimBa generates embeddings for the claims in each database only once and stores them in a cache for re-use. To use this cache, if it already exists, supply the -c option:

      python main.py <dataset name> -c


If you want to use a different database than ClaimsKG as corpus, run

      python main.py <dataset name> <corpus name>
    

corpus name: A custom name for your database. 

Again, you can use the -c option to use the cache, in case a cache for a database with the same corpus name already exists. Please make sure that when you use the cache, you did not generate it for a different database that you had given the same name!




## Repository Structure

### Data Locations
- **Input Data**: Place your query file in `claimlinking_simba/data/<dataset name>/queries.tsv`.
- **Cache Files**: Cache files are stored in `claimlinking_simba/data/cache/<dataset name>`.
- **Corpus**: Place your custom corpus file in `claimlinking_simba/data/<corpus name>/corpus.tsv`.
- **Output Data**:
  - Standard output files: `claimlinking_simba/data/<dataset name>/pred_client.tsv`, `claimlinking_simba/data/<dataset name>/pred_qrels.tsv`.

### Scripts
- **Main Script**: The entry point is `main.py`, located at the root.
- **Additional Scripts**: The core logic resides in the `src/` directory.

---

## File Descriptions

- **main.py**  
  The primary script to execute the SimBa project. Acts as the entry point for running the pipeline.

- **data/sample/queries.tsv**  
  A sample dataset in TSV format that contains an input query for testing the system.

- **data/claimsKG/corpus.tsv**  
  The default dataset (ClaimsKG corpus) containing the fact-checked claims.

- **data/sample/pred_qrels.tsv** 
  The output file generated by running SimBa for the sample queries. Contains the five most similar claims in the dataset per input query in the [CLEF CheckThat! Lab Task 2 Claim Retrieval challenge](https://checkthat.gitlab.io/clef2022/) format.

- **data/sample/pred_client.tsv**  
  A client-friendly output file generated by running SimBa for the sample queries, providing detailed results in a more human-readable format.

- **requirements.txt**  
  A list of Python dependencies required to run the project. 
  
---

  



## Input Data 


### Required
The required input consists of an input query file ("queries.tsv"): 
a text file in .tsv format (tab-separated) containing one query per line. One query consists of an ID and a claim. For each of the claims, SimBa will retrieve the most similar fact-checked claims in ClaimsKG.

### Optional
If desired, a different corpus than ClaimsKG can be supplied as database ("corpus.tsv").
 
This file should be in tab-separated format (`.tsv`) and must follow the structure below:  

### Format of `corpus.tsv`  
The file should contain the following columns:  

- **Claim ID** – A unique identifier for the claim.  
- **Claim Text** – The textual content of the claim.  
- **Claim Review Title** – The title of the fact-checking review.  
- **Claim Review URL** – A link to the fact-checking article.  
- **Rating** – The fact-checking assessment of the claim (e.g., true, false, half false, etc.).

If available, a goldstandard can be supplied which lists the optimal results ("gold.tsv"). This can be used to evaluate SimBa's performance using the evaluation scripts of the [CLEF CheckThat! Lab Task 2 Claim Retrieval challenge](https://checkthat.gitlab.io/clef2022/).

## Sample Input
queries.tsv
```
25603      Singer and actress Cher died in December 2022 or January 2023.
```


## Output Data
The outputs are exported to two files:

1. **Standard Output File**: `sample.tsv`
   - Contains the results in a tab-separated format with the following columns:
     ```
     Query ID     Q0    Claim ID    Rank  Similarity Score  Method Name
     ```
     Example:
     ```
     25603        Q0    59543 1     31.600123964723423      SimBa
     ```

2. **Client-Friendly Output File**: `pred_client.tsv`
   - Contains a more readable format with the following columns:
     - Query
     - Verified Claim (vclaim)
     - Claim Review URL
     - Rating (True/False/Other)
     - Similarity Score

## Sample Output (`pred_client.tsv`)

The following table shows an example of the output:

| Query                                                      | VClaim                                                    | ClaimReviewURL                                              | Rating           | Similarity       |
|------------------------------------------------------------|-----------------------------------------------------------|------------------------------------------------------------|------------------|------------------|
| Singer and actress Cher died in December 2022 or January 2023. | Singer and actress Cher died in December 2022 or January 2023. | https://www.snopes.com/fact-check/cher-death-hoax | false            | 72.06526780919123 |
| Singer and actress Cher died in December 2022 or January 2023. | Chevy Chase died of a heart attack on 4 January 2016.      | https://www.snopes.com/fact-check/chevy-chase-death-hoax | false            | 39.27806597312666 |
| Singer and actress Cher died in December 2022 or January 2023. | Musicians Robert Plant and Cher plan to wed at Westminster Abbey in July 2016. | https://www.snopes.com/fact-check/cher-plant-marriage-plans | false            | 36.72969772403427 |
| Singer and actress Cher died in December 2022 or January 2023. | Video shows microburst over Karachi in July 2022           | https://factcheck.afp.com/doc.afp.com.32EN4W3      | false            | 31.600123964723423 |
| Singer and actress Cher died in December 2022 or January 2023. | Hillary Clinton admitted she had an urge to run again in January 2020. | https://www.truthorfiction.com/did-hillary-clinton-say-she-had-an-urge-to-run-again-in-january-2020 | decontextualized | 31.38685337133225 |

--- 
    



## Architecture

SimBa is fully unsupervised, i.e. it does not need any training data. 
It operates in two steps:

1. Candidate Retrieval
2. Re-Ranking

In the first step, the semantically most similar claims are retrieved as candidates. Semantic similarity is computed using sentence embeddings. 
In a second step, a computationally more costly re-ranking step is applied to all candidates in order to find the best matches. Again, sentence embeddings combined with a lexical feature are used. 

SimBa was evaluated on the [CLEF CheckThat! Lab Task 2 Claim Retrieval challenge](https://checkthat.gitlab.io/clef2022/) data and achieved the following scores: 

| Datast  | Map@1 | Map@3     | Map@5 |  
|---|---|-----------|---|
| 2020 2a English  | 0.9425  |  0.9617   |  0.9617
| 2021 2a English  | 0.9208  | 0.9431    |  0.9450     
| 2021 2b English  | 0.4114  | 0.4388    |  0.4414 
| 2022 2a English  | 0.9043  | 0.9258    |  0.9258 
| 2022 2b English  | 0.4462  | 0.4744    |  0.4805

For more details about this method, please refer to the following publications: 

Hövelmeyer, Alica, Katarina Boland, and Stefan Dietze. 2022. "SimBa at CheckThat! 2022: Lexical and Semantic Similarity-Based Detection of Verified Claims in an Unsupervised and Supervised Way." In CLEF Working Notes 2022, Proceedings of the Working Notes of CLEF 2022- Conference and Labs of the Evaluation Forum, edited by Guglielmo Faggioli, Nicola Ferro, Allan Hanbury, and Martin Potthast, CEUR Workshop Proceedings 3180, 511-531. Aachen: RWTH Aachen. https://ceur-ws.org/Vol-3180/paper-40.pdf. 

Boland, Katarina, Hövelmeyer, Alica, Fafalios, Pavlos, Todorov, Konstantin, Mazhar, Usama, & Dietze, Stefan (2023). Robust and efficient claim retrieval for online fact-checking applications. Pre-print. https://doi.org/10.21203/rs.3.rs-3007151/v1


## Contact
For further assistance or inquiries, please contact: katarina.boland@hhu.de






