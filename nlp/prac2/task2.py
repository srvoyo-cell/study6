import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
try:
    import pymorphy2
except Exception:
    pymorphy2 = None


class TextPreprocessor:
    def __init__(self, language="russian", use_lemmatization=True):
        self.language = language
        self.use_lemmatization = use_lemmatization
        self.stop_words = self._load_stopwords(language)
        if use_lemmatization and pymorphy2 is not None:
            self.lemmatizer = pymorphy2.MorphAnalyzer()
        else:
            self.use_lemmatization = False
            self.stemmer = SnowballStemmer(language)

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"https?://\S+|www\.\S+", " ", text)
        text = re.sub(r"\S+@\S+", " ", text)
        text = re.sub(r"\d+", " ", text)
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"[^а-яёa-z\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def tokenize(self, text):
        try:
            return word_tokenize(text, language="russian")
        except LookupError:
            return re.findall(r"[а-яёa-z]+", text.lower())

    def normalize_token(self, token):
        if self.use_lemmatization:
            return self.lemmatizer.parse(token)[0].normal_form
        return self.stemmer.stem(token)

    def preprocess(self, text):
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        processed = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                processed.append(self.normalize_token(token))
        return processed

    def preprocess_for_vectorizer(self, text):
        return " ".join(self.preprocess(text))

    @staticmethod
    def _load_stopwords(language):
        try:
            return set(stopwords.words(language))
        except LookupError:
            return {
                "и", "в", "во", "не", "что", "он", "на", "я", "с", "со", "как",
                "а", "то", "все", "она", "так", "его", "но", "да", "ты", "к",
                "у", "же", "вы", "за", "бы", "по", "только", "ее", "мне",
                "было", "вот", "от", "меня", "еще", "нет", "о", "из", "ему",
                "теперь", "когда", "даже", "ну", "вдруг", "ли", "если", "уже",
                "или", "ни", "быть", "был", "него", "до", "вас", "нибудь",
                "опять", "уж", "вам", "ведь", "там", "потом", "себя", "ничего",
                "ей", "может", "они", "тут", "где", "есть", "надо", "ней",
                "для", "мы", "тебя", "их", "чем", "была", "сам", "чтоб",
                "без", "будто", "чего", "раз", "тоже", "себе", "под", "будет",
                "ж", "тогда", "кто", "этот", "того", "потому", "этого",
                "какой", "совсем", "ним", "здесь", "этом", "один", "почти",
                "мой", "тем", "чтобы", "нее", "сейчас", "были", "куда",
                "зачем", "всех", "никогда", "можно", "при", "наконец", "два",
                "об", "другой", "хоть", "после", "над", "больше", "тот",
                "через", "эти", "нас", "про", "всего", "них", "какая",
                "много", "разве", "три", "эту", "моя", "впрочем", "хорошо",
                "свою", "этой", "перед", "иногда", "лучше", "чуть", "том",
                "нельзя", "такой", "им", "более", "всегда", "конечно", "всю",
                "между",
            }


if __name__ == "__main__":
    preprocessor = TextPreprocessor(use_lemmatization=True)
    sample_text = (
        "Это пример текста! Он содержит различные слова, включая числа 123 и знаки "
        "пунктуации."
    )
    processed = preprocessor.preprocess(sample_text)
    print(f"Исходный текст: {sample_text}")
    print(f"После предобработки: {processed}")
