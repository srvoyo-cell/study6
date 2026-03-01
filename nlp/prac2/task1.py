import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import time
from collections import Counter

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import pymorphy2

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy.sparse import csr_matrix, csc_matrix, coo_matrix, save_npz, load_npz
import scipy.sparse as sp

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("punkt_tab")
