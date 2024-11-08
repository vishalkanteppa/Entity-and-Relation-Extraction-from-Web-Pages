
from copy import deepcopy
from relevance import RelevanceModel


class LocalSearch(object):
    """Implements a local search algorithm"""

    def __init__(self, mentions, cache):
        self.mentions = mentions
        self.cachedPages = cache

    def retrieveCachedPage(self, link):
        for mention in self.cachedPages.keys():
            for pageTup in self.cachedPages[mention]:
                if pageTup[0] == link:
                    return pageTup[1]

    def runLocalSearch(self, iterations):

        state = self.getInitialState()
        # print("Initial State Obtained!")
        # print(state)
        # print("Running Local Search for " + str(iterations) + " iterations...")

        for i in range(iterations):
            for mention in self.mentions:
  
                # print("Analyzing the mention " + str(mention))
                # print('------------------------------------')

                # Ignore mention if no linkable entity is found
                if mention.lower() in list(map(lambda x:x.lower(), self.cachedPages.keys())):
                # if mention in self.cachedPages.keys():

                    candidateLinks = [k[0] for k in self.cachedPages[mention]]
                    assignedLink = state[mention][0]

                    for candidateLink in candidateLinks:

                        # Obtain the LinkRelevances
                        assignedPage = self.retrieveCachedPage(assignedLink)
                        candidatePage = self.retrieveCachedPage(candidateLink)
                        currentLinkRelevance = RelevanceModel.linkRelevance(self.mentions, assignedPage)
                        candidateLinkRelevance = RelevanceModel.linkRelevance(self.mentions, candidatePage)
                        # Obtain a convex combination of the link relevances and the
                        # sum of the document relevances
                        candidatePsi = candidateLinkRelevance
                        currentPsi = currentLinkRelevance
     
                        # print("Current Psi Value " + str(currentPsi) + " For " + assignedLink)
                        # print("Candidate Link Psi Value " + str(candidatePsi) + " For " + candidateLink)

                        # If the candidate link's convex combination is greater than the current
                        # link's convex combination, we replace that assignment
                        if candidatePsi < currentPsi:
                            state[mention] = (candidateLink, candidateLinkRelevance)
                            # print("Replaced Link")
           
                else:
                    pass
                    # print('------')
                    # print(f'UNLINKABLE MENTION : {mention}')
            # print(str(i + 1) + "/" + str(iterations) + " iterations complete")
        return state

    def getInitialState(self):
        """
        This returns an complete initial assignment by assigning each
        mention a link with the highest relevance score between the link's
        content and the input text
        """
        
        
        initialState = {}
        for mention in self.mentions:
            relevance = self.getMaxRelevance(mention)

            # Ignore mention if no linkable entity is found
            if relevance is not None:
                link, score = relevance
                initialState[str(mention)] = (link, score)
        return initialState

    def getMaxRelevance(self, mention):
      
        """For every possible candidate link for a mention, obtain the link's
        relevance score to the mention's context and return the highest
        scoring link along with its relevance score"""
        

        relevances = []
        # existing_keys = list(map(lambda x:x.lower(), self.cachedPages.keys()))

        # Ignore mention if no linkable entity is found

        if  mention not in self.cachedPages.keys():
            return None

        candidateLinks = [k[0] for k in self.cachedPages[mention]]
        for candidateLink in candidateLinks:
            score = RelevanceModel.linkRelevance(self.mentions, candidateLink)
            relevances.append((candidateLink, score))

            
        # Returns the tuple with the highest relevance score in the array
        return max(relevances, key=lambda x:x[1])
