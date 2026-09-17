# ♻️ VerdeSight AI

### AI-Powered Waste Intelligence for a Sustainable Future

**VerdeSight AI** is an AI-powered waste intelligence platform that uses a trained deep-learning model to classify waste images and provide recycling, sustainability, and environmental guidance.

The project combines **Computer Vision, Agentic AI concepts, RAG-based knowledge, and sustainability intelligence** into a single Streamlit application.

## ✨ Key Features

* 🤖 **Multi-Class Waste Classification**
  Classifies waste into 9 categories:

  * Cardboard
  * E-Waste
  * General Waste
  * Glass
  * Metal
  * Organic
  * Paper
  * Plastic
  * Textile

* 🎯 **Confidence & Top Predictions**
  Displays the model's confidence and top predicted categories.

* 🧠 **Agentic AI Verification**
  Reviews the classifier's prediction using confidence, prediction separation, and knowledge-based checks.

* 📚 **RAG-Based Waste Knowledge**
  Provides grounded information about waste categories, segregation, recycling, and disposal.

* ♻️ **Recycling Guidance**
  Suggests practical recycling, composting, reuse, and segregation actions.

* 🌍 **Environmental Impact Insights**
  Connects waste-management actions with sustainability and environmental benefits.

* 🌱 **Sustainability & SDG Connection**
  Links responsible waste management with relevant UN Sustainable Development Goals.

* 🎨 **Professional Streamlit Interface**
  Includes multiple visual themes and a clean sustainability-focused UI.

## 🧠 AI Architecture

```text
Waste Image
    ↓
Deep Learning Classifier
    ↓
Prediction + Confidence + Top-3
    ↓
Agentic Verification
    ↓
RAG / Waste Knowledge
    ↓
Recycling & Action Guidance
    ↓
Environmental Impact
    ↓
Sustainability Insights
```

## 📊 Model Performance

The waste classifier achieved:

**92.25% validation accuracy**

This result is based on a held-out validation set and should not be interpreted as guaranteed real-world accuracy.

## 🛠️ Tech Stack

* Python
* Streamlit
* TensorFlow / Keras
* MobileNetV2
* NumPy
* Pandas
* Pillow
* Local RAG / Knowledge Base
* Agentic AI workflow

## 📂 Project Structure

```text
VerdeSight AI
│
├── app.py
├── train_model.py
├── model_logic.py
├── rag_engine.py
├── granite_ai.py
├── agents.py
├── impact_engine.py
├── sustainability.py
├── theme_engine.py
├── requirements.txt
│
├── dataset/
│
└── models/
    ├── waste_classifier.keras
    └── class_names.json
```

## ⚙️ Run Locally

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## 🚀 Deployment

The application is designed for deployment using **Streamlit Community Cloud**.

The trained model file is required for classification.

For large model files, use **Git LFS** or another suitable model-storage solution depending on the deployment platform.

**Live Demo** : https://verdesight-ai-lhngtduszdvgzne3apjvw6.streamlit.app/

## 🔮 Future Scope

* Improved real-world classification accuracy
* Object detection for multiple waste items
* Hyper-local recycling recommendations
* User impact tracking
* Feedback-based model improvement
* Offline/edge AI support
* Advanced IBM Granite integration
* Mobile/PWA version

## ⚠️ Limitations

The classifier works best with clear images containing a single waste item. Predictions may be affected by lighting, background, image quality, or visually similar materials.

Agentic verification provides an additional review layer but does not replace the underlying ML prediction.

## 👩‍💻 Author

**Mili Srivastava**
B.Tech CSE (AI & ML)

GitHub: [@milisrivastav13](https://github.com/milisrivastav13)

---

♻️ **VerdeSight AI — Turning waste intelligence into sustainable action.**
