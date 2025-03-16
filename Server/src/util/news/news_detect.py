import os
import re
import tensorflow as tf
import nltk
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
nltk.download('stopwords')
import pickle
from dotenv import load_dotenv

load_dotenv()

rf_path = os.getenv("RR_MODEL")
seq_path = os.getenv("SEQ_MODEL")

with open(rf_path, "rb") as f:
    rf = pickle.load(f)

MAXLEN = 250

NEWS_CLASS_MAPPING = {
    "misinformation": 0,
    "credible": 1,
    "political_bias": 2,
    "unreliable": 3,
}

def preprocess_text(text):
    # text = BeautifulSoup(text, "html.parser").get_text()
    try:
        if text is None:
            return ""
        if text == "":
            return ""
        if not isinstance(text, str):
            return ""

        # Combine regex for URLs, mentions, and non-alphabetic characters
        text = re.sub(r"http\S+|@\w+|[^a-zA-Z\s]", " ", text)

        # Remove new lines, tabs, and extra spaces
        text = re.sub(r"[\n\t]+", " ", text)  # Replace new lines and tabs with a single space
        text = re.sub(r"  +", " ", text).strip()  # Replace multiple spaces with a single space

        # Convert to lowercase
        text = text.lower()

        # Tokenize and remove stopwords
        words = text.split()
        sw = set(stopwords.words('english'))
        words = [w for w in words if w not in sw]

        # Join words back into a single string
        text = " ".join(words)
        return text
    except Exception as e:
        print(f"Error processing text: {e}")
        return ""

def predict_text(title: str, text: str) -> str:
    title = preprocess_text(title)
    text = preprocess_text(text)
    script_path = os.path.dirname(os.path.abspath(__file__))
    tokenizer_path = os.path.join(script_path, "tokenizer.pickle")
    tokenizer = pickle.load( open(tokenizer_path, "rb"))

    # Combine title and text
    content = "<title>" + title + "</title> <content>" + text + "</content>"
    seq = tokenizer.texts_to_sequences([content])
    pad = pad_sequences(seq, maxlen=MAXLEN, padding='post')
    pred = rf.predict(pad)
    seq_model = tf.keras.models.load_model(seq_path)
    seq_pred = seq_model.predict(pad)
    print(seq_pred)
    max_pred = seq_pred.argmax()
    print(max_pred)
    print(list(NEWS_CLASS_MAPPING.keys())[list(NEWS_CLASS_MAPPING.values()).index(max_pred)])
    print(list(NEWS_CLASS_MAPPING.keys())[list(NEWS_CLASS_MAPPING.values()).index(pred)])
    return list(NEWS_CLASS_MAPPING.keys())[list(NEWS_CLASS_MAPPING.values()).index(pred)]

def main():
    title = "The Quantum Ledger Initiative (QLI)"
    text = """The Premise:  
    
    In the late 1990s, during the dot-com boom, a secret alliance of tech giants, financial institutions, and government agencies quietly launched an initiative called the Quantum Ledger Initiative (QLI). Its stated goal was to create a decentralized global database using quantum computing technology—essentially, a next-generation version of blockchain—but its true purpose went far beyond what anyone could have imagined. 
    
    The QLI's real mission? To map, predict, and ultimately control human behavior on a mass scale through the collection and analysis of every digital interaction ever made. This includes everything from your search history and social media activity to your biometric data captured by smart devices like fitness trackers and voice assistants. 
    How It Works:  
    
        Data Collection:  Every major tech company you know—Google, Amazon, Facebook, Apple—is secretly funneling user data into the QLI system. Even smaller apps and startups are unwittingly contributing because their tools rely on APIs or frameworks developed by these larger companies. 
    
        Quantum Computing Power:  Unlike traditional databases, the QLI uses quantum computers located in undisclosed facilities around the world. These machines can process unimaginable amounts of data simultaneously, allowing them to identify patterns and correlations that would take centuries for conventional systems to uncover. 
    
        Behavioral Modeling:  Using advanced AI algorithms, the QLI doesn't just track what people do; it predicts what they will do next. For example: 
            If someone starts researching cryptocurrency, the QLI might nudge them toward certain investments via targeted ads.
            If a group of individuals begins organizing protests online, the QLI flags them as potential threats and deploys countermeasures (e.g., misinformation campaigns or disruptions).
    
    
        Control Mechanisms:  The most chilling aspect of the QLI is its ability to manipulate outcomes without leaving traces. By subtly altering information feeds, suppressing key content, or amplifying specific narratives, the QLI ensures that society moves in directions favorable to those who control it. 
    
    
    Who’s Behind It?  
    
    At first glance, it seems like the usual suspects: Silicon Valley elites, Wall Street bankers, and shadowy intelligence agencies. But there’s more to the story. According to leaked documents purportedly shared by a whistleblower (who disappeared shortly afterward), the QLI has ties to ancient secret societies such as the Freemasons and the Illuminati. These groups allegedly provided the philosophical framework for controlling humanity under the guise of “progress.” 
    Why You Should Believe It:  
    
        Real-World Precedents:  Remember when Edward Snowden revealed the extent of NSA surveillance? Or how Cambridge Analytica exploited Facebook data to influence elections? These events show us that powerful entities are already collecting and weaponizing our personal information. 
    
        Technological Feasibility:  Quantum computing isn’t science fiction anymore—it’s happening right now. Companies like IBM, Google, and China’s Alibaba are racing to develop functional quantum machines. Combine this with AI advancements, and the QLI becomes frighteningly plausible. 
    
        Unexplained Phenomena:  Have you ever noticed how eerily accurate recommendations on platforms like YouTube or Spotify can be? Or how certain news stories seem to dominate headlines at suspiciously convenient times? While some dismiss these occurrences as coincidences, others see them as evidence of a hidden hand guiding public perception. 
    
        Whistleblower Testimonies:  There have been whispers within the cybersecurity community about engineers being forced to work on classified projects involving quantum technologies. Some claim they were threatened with legal action if they spoke out, while others simply vanished after raising concerns. 
    
    
    What They Want From You:  
    
    The ultimate aim of the QLI isn’t domination for its own sake—it’s stability. Those in charge believe that free will leads to chaos, so they’ve decided to guide humanity along predetermined paths to prevent societal collapse. In their eyes, sacrificing privacy and autonomy is a small price to pay for peace and prosperity. 
    
    But here’s the catch: once you’re aware of the QLI, you become a liability. That’s why whistleblowers disappear, dissenters are silenced, and skeptics are labeled conspiracy theorists. The QLI thrives on ignorance and complacency. 
    What Can You Do?  
    
    If you suspect the QLI exists, tread carefully. Avoid sharing sensitive information online, use encrypted communication tools, and educate yourself about digital privacy. Most importantly, question everything—even this very message. After all, how do you know I’m  not part of the QLI? """
    predict_text(title, text)


if __name__ == "__main__":
    main()

