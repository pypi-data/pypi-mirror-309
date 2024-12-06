import os
os.environ["OMP_NUM_THREADS"] = "1"
import inspect
from inspect import getargspec

import numpy as np
import sklearn
import hyperopt

import time
import multiprocessing 
from mpire import WorkerPool
from playwright.sync_api import sync_playwright
from pprint import pprint
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
from sklearn.model_selection import train_test_split

from hpsklearn import HyperoptEstimator, any_classifier, svc, svc_linear, svc_rbf, svc_poly, svc_sigmoid, liblinear_svc
from hpsklearn import knn, ada_boost, gradient_boosting,random_forest,extra_trees,decision_tree,sgd,xgboost_classification
from hpsklearn import multinomial_nb,gaussian_nb,passive_aggressive,linear_discriminant_analysis,quadratic_discriminant_analysis
from hpsklearn import rbm,colkmeans,one_vs_rest,one_vs_one,output_code
from hyperopt import tpe
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import BertTokenizer, BertModel
import torch

from sklearn.model_selection import train_test_split
from hyperopt import tpe
from hpsklearn import HyperoptEstimator, ada_boost, extra_trees, gaussian_nb, decision_tree
from hpsklearn import quadratic_discriminant_analysis, passive_aggressive, sgd, svc_linear, svc
from hpsklearn import xgboost_classification, gradient_boosting, random_forest, knn, linear_discriminant_analysis
import languagemodels as lm

def preprocess_texts(texts):
    # Load pre-trained BERT model and tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    # Sample list of text
    # texts = ["I love programming", "Python is awesome", "I love coding in Python"]

    # Tokenize and get embeddings
    inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True)

    # Get the hidden states from BERT (this is a representation of the text)
    with torch.no_grad():
        outputs = model(**inputs)

    # The embeddings of the [CLS] token, which is a good representation of the sentence
    sentence_embeddings = outputs.last_hidden_state[:, 0, :]

    # Convert to numpy array
    sentence_embeddings_np = sentence_embeddings.numpy()

    # Check the result
    return sentence_embeddings_np

def train_models(name,classifier,X_train, X_test, y_train, y_test,max_evals=10,trial_timeout=120):
    # Initialize HyperoptEstimator with the classifier
    try:
        estim = HyperoptEstimator(
            classifier=classifier(name),
            algo=tpe.suggest,
            max_evals=max_evals,
            trial_timeout=trial_timeout
        )

        estim.fit(X_train, y_train)

        # Collect results
        my_dict = {
            "best_model": estim.best_model(),
            "best_score": estim.score(X_test, y_test)
        }
        return my_dict
    except Exception as e:
        return {
            "error":str(e)
        }
def apply_ml_example(labelled_dataset,test_size=0.2,max_evals=10,trial_timeout=120):
    
    available_classifier_dict = {
        'AdaBoostClassifier': ada_boost,
        'ExtraTreeClassifier': extra_trees,
        'GaussianNB': gaussian_nb,
    }

    # Extract texts and labels, convert labels to strings
    texts = [labelled_data['texts'][0] for labelled_data in labelled_dataset]
    labels_str = [labelled_data['labels'][0] for labelled_data in labelled_dataset]  # Convert labels to strings
    
    labels_str = list(set(labels_str))
    # print(labels_str)
    mapping = {}
    for i in range(len(labels_str)):
        mapping[labels_str[i]] = i
    # print(mapping)
    labels = [mapping[labelled_data['labels'][0]] for labelled_data in labelled_dataset]  #
    # print(labels)
    # Preprocess texts
    X = preprocess_texts(texts)

    # print(X)
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=test_size)

    results = []
    meta_task = []
    for i, (name, classifier) in enumerate(list(available_classifier_dict.items())):
        my_dict = {}
        my_dict["name"] = name
        my_dict["classifier"] = classifier
        my_dict["X_train"] = X_train
        my_dict["X_test"] = X_test
        my_dict["y_train"] = y_train
        my_dict["y_test"] = y_test
        
        meta_task.append(my_dict)

    # num_cores = multiprocessing.cpu_count()-1
    for my_dict in meta_task:
        name,classifier=my_dict["name"],my_dict["classifier"]
        results.append(train_models(name,classifier,X_train, X_test, y_train, y_test,max_evals,trial_timeout))
        
    # with WorkerPool(n_jobs=num_cores) as pool:
        # results = pool.map(train_models, meta_task, progress_bar=True, chunk_size=1)
    
    
    
            
    return {"labelled_dataset": labelled_dataset, "results": results}

def extract_text_from_url(url,sleep_time):
    time.sleep(2)
    """
    Extract the main text content from a given URL.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Use headless mode
        page = browser.new_page()

        try:
            # Navigate to the URL
            page.goto(url, wait_until="domcontentloaded", timeout=sleep_time)

            # Extract all text from <p> and <div> elements
            paragraphs = page.locator("p").all_text_contents()  # All <p> tags
            div_texts = page.locator("div").all_text_contents()  # All <div> tags

            # Combine and deduplicate text content
            main_text = "\n".join(set(paragraphs + div_texts))
            return {"url": url, "text": main_text}
        except Exception as e:
            # print(e)
            pass
        finally:
            browser.close()
    return  {"url": url, "text":""}


# Initialize a browser for each worker
def extract_all_url_sync(query, task,sleep_time):
    time.sleep(2)
    urls = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Start browser per worker
        page = browser.new_page()
        try:
            # Go to Google
            page.goto("https://www.google.com", wait_until="domcontentloaded", timeout=sleep_time)

            # Accept cookies if present
            if page.locator("button:has-text('I agree')").count() > 0:
                page.locator("button:has-text('I agree')").click()

            # Fill in the search query
            search_input = page.locator("textarea[name='q']")
            search_input.fill(query)
            search_input.press("Enter")

            # Wait for search results to load
            page.wait_for_selector("a:has(h3)", timeout=sleep_time)

            # Extract URLs from the first page
            for element in page.locator("a:has(h3)").all():
                url = element.get_attribute("href")
                if url:
                    urls+=[{"url": url}]

            # Navigate to the second page
            next_button = page.locator(f"a[aria-label='Page {task}']")  # Locate "Next" or page 2 button
            if next_button.count() > 0:
                next_button.click()
                page.wait_for_selector("a:has(h3)", timeout=sleep_time)

                # Extract URLs from the second page
                for element in page.locator("a:has(h3)").all():
                    url = element.get_attribute("href")
                    if url:
                        urls+=[{"url": url}]
        except Exception as e:
            # print(e)
            return urls
        finally:
            browser.close()  # Close the browser for this worker
    return urls

def extract_all_url_sync_without_task(query,sleep_time):
    time.sleep(2)
    urls = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Start browser per worker
        page = browser.new_page()
        try:
            # Go to Google
            page.goto("https://www.google.com", wait_until="domcontentloaded", timeout=sleep_time)

            # Accept cookies if present
            if page.locator("button:has-text('I agree')").count() > 0:
                page.locator("button:has-text('I agree')").click()

            # Fill in the search query
            search_input = page.locator("textarea[name='q']")
            search_input.fill(query)
            search_input.press("Enter")

            # Wait for search results to load
            page.wait_for_selector("a:has(h3)", timeout=sleep_time)

            # Extract URLs from the first page
            for element in page.locator("a:has(h3)").all():
                url = element.get_attribute("href")
                if url:
                    urls.append({"url": url})

            # Navigate to the second page
            next_button = page.locator(f"a[aria-label='Page 1']")  # Locate "Next" or page 2 button
            if next_button.count() > 0:
                next_button.click()
                page.wait_for_selector("a:has(h3)", timeout=sleep_time)

                # Extract URLs from the second page
                for element in page.locator("a:has(h3)").all():
                    url = element.get_attribute("href")
                    if url:
                        urls+=[{"url": url}]
        except Exception as e:
            # print(e)
            return urls
        finally:
            browser.close()  # Close the browser for this worker
    return urls
def find_number_of_google_pages(query,sleep_time):
    time.sleep(2)
    """
    Finds the total number of pages for a Google search query.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Use headless browser
        page = browser.new_page()

        try:
            # Navigate to Google
            page.goto("https://www.google.com", wait_until="domcontentloaded")

            # Accept cookies if prompted
            if page.locator("button:has-text('I agree')").count() > 0:
                page.locator("button:has-text('I agree')").click()

            # Perform a search
            search_input = page.locator("textarea[name='q']")
            search_input.fill(query)
            search_input.press("Enter")

            # Wait for the search results to load
            page.wait_for_selector("a:has(h3)", timeout=sleep_time)

            # Locate the pagination section
            pagination_elements = page.locator("td a").all_text_contents()

            # Extract numbers from the pagination links
            page_numbers = [int(num) for num in pagination_elements if num.isdigit()]
            total_pages = max(page_numbers) if page_numbers else 1

            return total_pages
        except Exception as e:
            # print(e)
            pass
        finally:
            browser.close()
    return 0

def get_description_from_url(url: str,sleep_time):
    time.sleep(2)
    description = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Go to the target URL
            page.goto(url, wait_until="domcontentloaded", timeout=sleep_time)
            
            paragraphs = page.locator("p").all_text_contents()  # All <p> tags
            
            # Combine and deduplicate text content
            main_text = "\n".join(set(paragraphs))
            return main_text
        
        except Exception as e:
            # print(e)
            pass
            # print(f"An error occurred: {e}")
        finally:
            browser.close()
    
    return ""

def tag_dataset(texts,model,tokenizer,labels,inference_size):
    num_labels = len(labels)
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

    # # Perform inference
    # with torch.no_grad():
    #     outputs = model(**inputs)

    # # Extract logits (raw scores)
    # logits = outputs.logits

    # # Convert logits to probabilities using softmax
    # probabilities = torch.nn.functional.softmax(logits, dim=-1)

    # # Get predicted class indices
    # predicted_indices = torch.argmax(probabilities, dim=1)

    # # Map indices back to custom labels
    orr = ""
    for i,label in enumerate(labels):
        if i!=len(labels)-1:
            orr+=label+" or "
    prompt = [f"Classify {orr}: {texts}. Classification:"]
    lm.config["max_ram"] = inference_size
    # predicted_labels = [labels[idx] for idx in predicted_indices]
    predicted_labels = lm.rank_instruct(prompt,labels)[0][0]
    # print(predicted_labels)  # Example output: ['Spam', 'Promotional', 'Not Spam']
    return {"texts":texts,"labels":predicted_labels}


def parallel_scraping(query,num_page,labels,sleep_time=2,test_size=0.2,max_evals=10,trial_timeout=120,inference_size="2gb"):
    sleep_time *= 1000
    # init_browser_pool()
    total_pages = find_number_of_google_pages(query,sleep_time)
    
    num_cores = multiprocessing.cpu_count()-1
    # print(num_cores)
    print("Getting urls...")
    queries = [{"query":query,"task":task,"sleep_time":sleep_time} for task in range(min(num_page,total_pages))]
    
    with WorkerPool(n_jobs=num_cores) as pool:
        urls = pool.map(extract_all_url_sync, queries, progress_bar=False, chunk_size=1)
    mod_urls = []
    for url in urls:
        mod_urls+=url
    new_urls = []
    for url in mod_urls:
        new_urls.append(url["url"])
    new_urls=list(set(new_urls))
    print("Getting descriptions...")
    new_urls = [{"url":url,"sleep_time":sleep_time} for url in new_urls]
    with WorkerPool(n_jobs=num_cores) as pool:
        descriptions = pool.map(get_description_from_url, new_urls, progress_bar=False, chunk_size=1)
    # pprint(descriptions)
    descriptions = [{"query":descriptions[i],"sleep_time":sleep_time} for i in range(len(descriptions)) if descriptions[i]!=""]
    # return
    print("Getting All URLS...")
    with WorkerPool(n_jobs=num_cores) as pool:
        urls = pool.map(extract_all_url_sync_without_task, descriptions, progress_bar=False, chunk_size=1)
    mod_urls = []
    for url in urls:
        mod_urls+=url
    new_urls = []
    for url in mod_urls:
        new_urls.append(url["url"])
    new_urls=list(set(new_urls))
    new_urls = [{"url":url,"sleep_time":sleep_time} for url in new_urls]
    print("Getting All Descriptions...")
    with WorkerPool(n_jobs=num_cores) as pool:
        descriptions = pool.map(get_description_from_url, new_urls, progress_bar=True, chunk_size=1)
    # pprint(descriptions)
    # Define the number of labels for your task
    num_labels = len(labels)  # Example for custom labels: Spam, Not Spam, Promotional

    # Load tokenizer and model
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=num_labels)  # Adjust num_labels
    descriptions = [{"texts":[descriptions[i]],"model":model,"tokenizer":tokenizer,"labels":labels,"inference_size":inference_size} for i in range(len(descriptions)) if descriptions[i]!=""]
    # pprint(descriptions)
    
    with WorkerPool(n_jobs=num_cores) as pool:
        labelled_dataset = pool.map(tag_dataset, descriptions, progress_bar=True, chunk_size=1)
    # print(labelled_dataset)
    return apply_ml_example(labelled_dataset,test_size=test_size,max_evals=max_evals,trial_timeout=trial_timeout)

# if __name__=="__main__":
#     query = "Artificial Intelligence"
#     num_page = 1
#     sleep_time = 2
#     labels = ["spam","not Spam"]
#     inference_size = "2gb"
    
    
#     results = parallel_scraping(query,num_page,labels,sleep_time,inference_size)
#     # print(results)
