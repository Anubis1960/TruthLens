# **TruthLens**  
*Empowering You to Navigate the Digital World with Confidence*

---

## **About TruthLens**  
TruthLens is a cutting-edge web application designed to help users stay informed by fact-checking news articles, images, and videos. Whether you're trying to verify the authenticity of a news story or determine if an image or video is AI-generated, TruthLens has got you covered. With its advanced machine learning models and intuitive interface, TruthLens ensures that you can trust the content you consume online.

---

## **Key Features**  

✨ **Fact-Checking News Articles**  
Classify news articles to determine their credibility and accuracy. Stay ahead of misinformation with our robust classification system.

📸 **AI-Generated Media Detection**  
Detect whether images or videos have been generated or manipulated by AI. TruthLens uses state-of-the-art models to analyze media and provide accurate results.

🤖 **Intelligent Chatbot**  
Interact with our AI-powered chatbot, built on DeepSeek R1 1.5 and powered by Ollama. Get answers to your questions and gain deeper insights into the content you're analyzing.

📊 **Website Trust Scores**  
Every website scanned by TruthLens is assigned a trust score, helping you gauge the reliability of the source at a glance.

---

## **Installation Guide**

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/Anubis1960/ITFest2025.git
```

### **Step 2:  Install Dependencies**
```bash
# Backend dependencies
pip install -r Server/requirements.txt

# Frontend dependencies
cd FrontEnd
npm install
```
### **Step 3. Train the Classifier Models**
Run the provided .ipynb files to train and generate the machine learning models used for classification and detection. Below are the datasets used for training: 
- Image Classification Models
    - Dataset https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images
    (This dataset contains real and AI-generated synthetic images for training the image classifier.)
- News Classification Model
    - Dataset: https://github.com/several27/FakeNewsCorpus?tab=readme-ov-file
    (This dataset contains labeled news articles for training the news classifier.)

### **Step 4: Configure Environment Variables**
Create a .env file in the /Server directory and add the following:
- API keys for external services (AAI, Google OAuth2)
- File paths for Firebase configuration
- Flask secret key
- Path to the classification models

## **Usage**
```
cd .\FrontEnd\ | ng serve
cd ..\Server\ | py main.py
```