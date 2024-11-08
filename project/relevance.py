from sklearn.feature_extraction.text import TfidfVectorizer

class RelevanceModel(object):
    """
    Given a link, a keyword, and a current state, how do we figure out if that link is the best fit for that keyword effectively using the context given to us? In our implementation, there is a crucial consideration: we must be able to somehow use previous assigned keywords as factors in our score. This means that given the content of a wikipedia link, we must use the current keyword and the keywords around it to gauge how good of a match that link is to our current keyword.
    This class implements multiple approaches described from literature and
    explained in detail in the report
    """

    @classmethod
    def linkRelevance(self, inputKeywords, page):
        
        inputText = ' '.join(str(v) for v in inputKeywords)
        linkText = page
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([inputText, linkText])
        return ((tfidf * tfidf.T).A)[0,1]

    @classmethod
    def documentRelevance(self, page1, page2):
        linkText1 = page1
        linkText2 = page2
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([linkText1, linkText2])
        return ((tfidf * tfidf.T).A)[0,1]
