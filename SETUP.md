# 🚀 QuantFolio — Complete Setup & Deployment Guide

---

## Part 1: Run the Project Locally (✅ You've done this!)

You've already run the Jupyter notebook. 

---

## Part 2: Run the Streamlit Dashboard

The Streamlit dashboard is a live interactive version of your notebook.

### Step 1: Install Streamlit
Open Anaconda Prompt:
```
pip install streamlit
```

### Step 2: Navigate to project folder
```
cd "C:\Users\Arshdeep Singh\Downloads\QuantFolio"
```

### Step 3: Launch it
```
streamlit run app.py
```

Your browser will open at `http://localhost:8501` with the live dashboard.
Press `Ctrl+C` in the terminal to stop it.

---

## Part 3: Generate the PowerPoint

### Step 1: Install Node.js
Download from https://nodejs.org/ (LTS version). Install with defaults.

### Step 2: Install pptxgenjs
```
npm install -g pptxgenjs
```

### Step 3: Update the numbers
Open `generate_pptx.js` in any text editor (Notepad works).
Find the `DATA = { ... }` section at the top.
Replace the `XX.X` placeholders with the real numbers from your notebook output.

For example, if your notebook showed:
```
Max Sharpe: Return=18.2%, Vol=22.1%, SR=0.529
```
Then update:
```javascript
maxSharpe: { ret: "18.2", vol: "22.1", sr: "0.529" },
```

### Step 4: Generate
```
node generate_pptx.js
```

### Step 5: Add chart screenshots
Open the generated `QuantFolio_Presentation.pptx` in PowerPoint.
Slides 5-8 have placeholder boxes — right-click → "Change Picture" and paste
screenshots from your notebook (the Efficient Frontier, Pie charts, Backtest, etc.)

**To take screenshots from Jupyter:** right-click any chart → "Save Image As"

---

## Part 4: Push to GitHub

### Step 1: Create a GitHub account
Go to https://github.com and sign up (free).

### Step 2: Install Git
Download from https://git-scm.com/downloads (accept defaults).

### Step 3: Configure Git (one time only)
Open Anaconda Prompt:
```
git config --global user.name "Arshdeep Singh"
git config --global user.email "your.email@example.com"
```

### Step 4: Create a GitHub repository
1. Go to https://github.com → click **"+"** (top right) → **"New repository"**
2. Name: `QuantFolio`
3. Description: `Portfolio Optimization & ML-Enhanced Asset Allocation — Real NSE Data`
4. Set to **Public**
5. Do NOT check "Add a README" (we have one)
6. Click **Create repository**

### Step 5: Push your code
In Anaconda Prompt:
```
cd "C:\Users\Arshdeep Singh\Downloads\QuantFolio"
git init
git add .
git commit -m "Initial commit: QuantFolio portfolio optimization with real NSE data"
git remote add origin https://github.com/YOUR_USERNAME/QuantFolio.git
git branch -M main
git push -u origin main
```

When asked for password, use a **Personal Access Token**:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Check **"repo"** scope
4. Generate → copy the token
5. Paste it as your password

### Step 6: Verify
Go to `https://github.com/YOUR_USERNAME/QuantFolio` — you should see your code and README.

---

## Part 5: Deploy Streamlit Dashboard (Free Live URL)

This gives you a URL like `quantfolio.streamlit.app` that anyone can visit.

### Step 1: Go to https://share.streamlit.io
Sign in with your GitHub account.

### Step 2: Deploy
1. Click **"New app"**
2. Repository: `YOUR_USERNAME/QuantFolio`
3. Branch: `main`
4. Main file: `app.py`
5. Click **"Deploy!"**

### Step 3: Wait 2-3 minutes
Once deployed, you get a live URL. Put this URL in your:
- GitHub README
- LinkedIn post
- CloudHire profile (Portfolio Link field)

---

## Part 6: Update CloudHire Profile

**Portfolio Link** → `https://github.com/YOUR_USERNAME/QuantFolio`

Or use the Streamlit URL: `https://quantfolio.streamlit.app` (or whatever it assigns)

---

## Part 7: Making Future Updates

```
git add .
git commit -m "Description of what you changed"
git push
```

Streamlit auto-deploys when you push — your live demo updates automatically.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `git` not recognized | Restart Anaconda Prompt after installing Git |
| `streamlit` not found | Run `pip install streamlit` |
| `node` not recognized | Restart Anaconda Prompt after installing Node.js |
| GitHub asks for password | Use Personal Access Token (Part 4, Step 5) |
| Streamlit Cloud fails | Make sure `requirements.txt` is in the root folder |
