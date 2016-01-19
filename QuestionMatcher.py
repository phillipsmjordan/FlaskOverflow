import string

from Models import Question

stopwordlist = ["i", "you", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all",
                "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst",
                "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway",
                "anywhere", "are", "around", "as", "at", "back", "be", "became", "because", "become", "becomes",
                "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between",
                "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con", "could",
                "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg",
                "eight", "either", "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every",
                "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire",
                "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full",
                "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here",
                "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how",
                "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its",
                "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me",
                "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must",
                "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody",
                "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one",
                "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own",
                "part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming",
                "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty",
                "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such",
                "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence",
                "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv",
                "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to",
                "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up",
                "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence",
                "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether",
                "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
                "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]


def get_match_scores(subject):
    subject = subject.lower()
    match_scores = list()
    existing_subjects = get_existing_subjects()
    for existing_subject in existing_subjects:
        match_score = 0
        for word in tokenize_and_remove_stopwords_puncuation(subject):
            if word in existing_subject.values()[0]:
                match_score += 1
        if match_score > 0:
            match = {existing_subject.keys()[0]: match_score}
            match_scores.append(match)
    return match_scores


def get_existing_subjects():
    existing_subjects = Question.query.with_entities(Question.id, Question.subject).all()
    tokenized_subjects = list()
    for subject_result in existing_subjects:
        tokenized_subjects.append({subject_result.id:tokenize_and_remove_stopwords_puncuation(subject_result.subject)})
    return tokenized_subjects


def tokenize_and_remove_stopwords_puncuation(phrase):
    exclude = set(string.punctuation)
    tokenized_word_list = list()
    for i in phrase.split():
        i = i.lower()
        i = ''.join(ch for ch in i if ch not in exclude)
        if i not in stopwordlist:
            tokenized_word_list.append(i)
    return tokenized_word_list
