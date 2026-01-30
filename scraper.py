import re
import sys
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup

STOP_WORDS = {
    "a", "able", "about", "above", "abst", "accordance", "according",
    "accordingly", "across", "act", "actually", "added", "adj", "affected",
    "affecting", "affects", "after", "afterwards", "again", "against", "ah",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "an", "and", "announce", "another", "any",
    "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways",
    "anywhere", "apparently", "approximately", "are", "aren", "arent", "arise",
    "around", "as", "aside", "ask", "asking", "at", "auth", "available", "away",
    "awfully", "b", "back", "be", "became", "because", "become", "becomes",
    "becoming", "been", "before", "beforehand", "begin", "beginning",
    "beginnings", "begins", "behind", "being", "believe", "below", "beside",
    "besides", "between", "beyond", "biol", "both", "brief", "briefly", "but",
    "by", "c", "ca", "came", "can", "cannot", "can't", "cause", "causes",
    "certain", "certainly", "co", "com", "come", "comes", "contain",
    "containing", "contains", "could", "couldnt", "d", "date", "did", "didn't",
    "different", "do", "does", "doesn't", "doing", "done", "don't", "down",
    "downwards", "due", "during", "e", "each", "ed", "edu", "effect", "eg",
    "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough",
    "especially", "et", "et-al", "etc", "even", "ever", "every", "everybody",
    "everyone", "everything", "everywhere", "ex", "except", "f", "far", "few",
    "ff", "fifth", "first", "five", "fix", "followed", "following", "follows",
    "for", "former", "formerly", "forth", "found", "four", "from", "further",
    "furthermore", "g", "gave", "get", "gets", "getting", "give", "given",
    "gives", "giving", "go", "goes", "gone", "got", "gotten", "h", "had",
    "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he",
    "hed", "hence", "her", "here", "hereafter", "hereby", "herein", "heres",
    "hereupon", "hers", "herself", "hes", "hi", "hid", "him", "himself", "his",
    "hither", "home", "how", "howbeit", "however", "hundred", "i", "id", "ie",
    "if", "i'll", "im", "immediate", "immediately", "importance", "important",
    "in", "inc", "indeed", "index", "information", "instead", "into",
    "invention", "inward", "is", "isn't", "it", "itd", "it'll", "its", "itself",
    "i've", "j", "just", "k", "keep", "keeps", "kept", "kg", "km", "know",
    "known", "knows", "l", "largely", "last", "lately", "later", "latter",
    "latterly", "least", "less", "lest", "let", "lets", "like", "liked",
    "likely", "line", "little", "'ll", "look", "looking", "looks", "ltd", "m",
    "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean",
    "means", "meantime", "meanwhile", "merely", "mg", "might", "million",
    "miss", "ml", "more", "moreover", "most", "mostly", "mr", "mrs", "much",
    "mug", "must", "my", "myself", "n", "na", "name", "namely", "nay", "nd",
    "near", "nearly", "necessarily", "necessary", "need", "needs", "neither",
    "never", "nevertheless", "new", "next", "nine", "ninety", "no", "nobody",
    "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not",
    "noted", "nothing", "now", "nowhere", "o", "obtain", "obtained",
    "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "omitted",
    "on", "once", "one", "ones", "only", "onto", "or", "ord", "other", "others",
    "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over",
    "overall", "owing", "own", "p", "page", "pages", "part", "particular",
    "particularly", "past", "per", "perhaps", "placed", "please", "plus",
    "poorly", "possible", "possibly", "potentially", "pp", "predominantly",
    "present", "previously", "primarily", "probably", "promptly", "proud",
    "provides", "put", "q", "que", "quickly", "quite", "qv", "r", "ran",
    "rather", "rd", "re", "readily", "really", "recent", "recently", "ref",
    "refs", "regarding", "regardless", "regards", "related", "relatively",
    "research", "respectively", "resulted", "resulting", "results", "right",
    "run", "s", "said", "same", "saw", "say", "saying", "says", "sec",
    "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen",
    "self", "selves", "sent", "seven", "several", "shall", "she", "shed",
    "she'll", "shes", "should", "shouldn't", "show", "showed", "shown",
    "showns", "shows", "significant", "significantly", "similar", "similarly",
    "since", "six", "slightly", "so", "some", "somebody", "somehow", "someone",
    "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere",
    "soon", "sorry", "specifically", "specified", "specify", "specifying",
    "still", "stop", "strongly", "sub", "substantially", "successfully",
    "such", "sufficiently", "suggest", "sup", "sure", "t", "take", "taken",
    "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx",
    "that", "that'll", "thats", "that've", "the", "their", "theirs", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "thered", "therefore", "therein", "there'll", "thereof", "therere",
    "theres", "thereto", "thereupon", "there've", "these", "they", "theyd",
    "they'll", "theyre", "they've", "think", "this", "those", "thou", "though",
    "thoughh", "thousand", "throug", "through", "throughout", "thru", "thus",
    "til", "tip", "to", "together", "too", "took", "toward", "towards",
    "tried", "tries", "truly", "try", "trying", "ts", "twice", "two", "u",
    "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until",
    "unto", "up", "upon", "ups", "us", "use", "used", "useful", "usefully",
    "usefulness", "uses", "using", "usually", "v", "value", "various", "'ve",
    "very", "via", "viz", "vol", "vols", "vs", "w", "want", "wants", "was",
    "wasnt", "way", "we", "wed", "welcome", "we'll", "went", "were", "werent",
    "we've", "what", "whatever", "what'll", "whats", "when", "whence",
    "whenever", "where", "whereafter", "whereas", "whereby", "wherein",
    "wheres", "whereupon", "wherever", "whether", "which", "while", "whim",
    "whither", "who", "whod", "whoever", "whole", "who'll", "whom",
    "whomever", "whos", "whose", "why", "widely", "willing", "wish", "with",
    "within", "without", "wont", "words", "world", "would", "wouldnt", "www",
    "x", "y", "yes", "yet", "you", "youd", "you'll", "your", "youre", "yours",
    "yourself", "yourselves", "you've", "z", "zero"
}

def computeWordFrequencies(tokenList: list[str]) -> dict[str, int]:
    """
    Takes a list of tokens and returns a dictionary of each Token and 
    its frequency in the token list.
    
    :param tokenList: list of Token objects
    :type tokenList: list[Token]
    :return: dictionary of (Token: frequency)
    :rtype: dict[Token, int]
    """
    tokenDict = {}
    for token in tokenList:
        if token in tokenDict:
            tokenDict[token] += 1
        else:
            tokenDict[token] = 1
    return tokenDict


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    links = set()

    soup = BeautifulSoup(resp.raw_response.content, "lxml")

    for spam in soup(["script", "style"]):
        spam.decompose()

    content = soup.get_text()
    words = re.findall(r'\b[a-zA-Z]{2,}\b', content.lower())
    filtered_words = [word for word in words if word not in STOP_WORDS]
    word_frequencies = computeWordFrequencies(filtered_words)


    for a_tag in soup.find_all('a', href=True):
        parsed = urlparse(a_tag.get('href'))
        parsed = parsed._replace(fragment="")
        unfragmented = urlunparse(parsed)
        links.add(unfragmented)
    
    with open("crawled_pages.txt", "a", encoding="utf-8") as f:
        f.write(f"{url}\n")
        f.write(f"Word frequencies:\n")
        for word, freq in sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{word}: {freq}\n")
        f.write("\n\n")

    return list(links)

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
