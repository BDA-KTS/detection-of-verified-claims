import os
import shutil
import subprocess
from pathlib import Path
import argparse
import nltk
nltk.download("stopwords")
nltk.download('punkt')
import spacy
from spacy.cli import download
download("en_core_web_sm")


def run(dataset_name, database_name="claimsKG", use_cache=False):
    # Input query file for SimBa as independent repo
    data_name_queries = f"data/{dataset_name}/queries.tsv"

    # Verified candidate claims file for SimBa as independent repo
    data_name_targets = f"data/{database_name}/corpus.tsv"

    # Path to this script's directory
    directory_path = os.path.dirname(__file__)

    # Run candidate retrieval
    retrieval_command = [
        "python",
        os.path.join(directory_path, "src/candidate_retrieval/retrieval.py"),
        data_name_queries,
        data_name_targets,
        dataset_name,
        dataset_name,
        "braycurtis",
        "50",
        "-sentence_embedding_models", "all-mpnet-base-v2"
    ]

    if not use_cache:
        caching_directory = os.path.join("data", "cache", dataset_name)
        if os.path.exists(caching_directory):
            shutil.rmtree(caching_directory)
       

    subprocess.call(retrieval_command)

    # Run re-ranking
    subprocess.call([
        "python",
        os.path.join(directory_path, "src/re_ranking/re_ranking.py"),
        data_name_queries,
        data_name_targets,
        dataset_name,
        dataset_name,
        "braycurtis",
        "5",
        "-sentence_embedding_models",
        "all-mpnet-base-v2",
        "sentence-transformers/sentence-t5-base",
        "princeton-nlp/unsup-simcse-roberta-base",
        "-lexical_similarity_measures", "similar_words_ratio"
    ])

    # Gold qrel labels file for SimBa as independent repo
    data_name_gold = f"data/{dataset_name}/gold.tsv"

    # Evaluation (optional, uncomment if needed)
    """
    Uncomment this block to evaluate the results if you have the evaluation script ready.
    
    print("Evaluation Scores for dataset " + dataset_name)
    subprocess.call([
        "python", os.path.join(directory_path, "evaluation/scorer/main.py"),
        data_name_gold,
        "data/" + dataset_name + "/pred_qrels.tsv"
    ])
    """


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run candidate retrieval and re-ranking for a specified dataset.")
    parser.add_argument("dataset_name", default="sample", help="The name of the dataset (folder in 'data') containing 'queries.tsv'.")
    parser.add_argument(
        "--database_name",
        default="claimsKG",
        help="The name of the database (folder in 'data') containing 'corpus.tsv'. Defaults to 'claimsKG'."
    )
    parser.add_argument(
        "-c", "--use_cache",
        action="store_true",
        help="Use cache if it exists; otherwise, re-generate the cache. Defaults to re-generating."
    )

    args = parser.parse_args()

    run(args.dataset_name, args.database_name, args.use_cache)
