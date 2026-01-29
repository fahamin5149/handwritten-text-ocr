# Deploying to Streamlit Cloud

## 🚀 Quick Deployment Guide

Your app is now configured to work seamlessly on **Streamlit Cloud**. Here's how to set up the Gemini API key:

---

## Step 1: Configure Secrets on Streamlit Cloud

### Option A: Through the Streamlit Cloud Dashboard

1. Go to [share.streamlit.io](https://share.streamlit.io) and log in
2. Find your deployed app in the dashboard
3. Click on **"⚙️ Settings"** (three dots menu)
4. Select **"Secrets"**
5. Add your secret in TOML format:

```toml
GEMINI_API_KEY = "AIza...your_actual_key_here"
```

6. Click **"Save"**
7. Your app will automatically restart with the new secret

### Option B: During Initial Deployment

1. When deploying your app for the first time
2. In the deployment wizard, look for **"Advanced settings"**
3. Find the **"Secrets"** section
4. Paste your API key in TOML format:

```toml
GEMINI_API_KEY = "AIza...your_actual_key_here"
```

5. Complete the deployment

---

## Step 2: Verify It Works

After adding the secret:

1. Visit your deployed app URL
2. Upload an image
3. Select **"Google Gemini"** as the OCR engine
4. Click **"Convert to Word"**
5. ✅ If it works, you're all set!

---

## 🔐 How the Code Handles API Keys

Your app now automatically detects where it's running:

```python
# Priority order:
1. Streamlit Secrets (st.secrets['GEMINI_API_KEY']) → Used on Streamlit Cloud
2. Environment Variables (os.getenv('GEMINI_API_KEY')) → Used locally with .env
```

### For Local Development
Use the `.env` file in your project root:
```bash
GEMINI_API_KEY=your_key_here
```

### For Streamlit Cloud
Use Streamlit Secrets (configured through the dashboard as shown above)

---

## 🛡️ Security Best Practices

✅ **DO:**
- Use Streamlit Secrets for cloud deployment
- Use `.env` file for local development
- Add `.env` and `secrets.toml` to `.gitignore` (already done)

❌ **DON'T:**
- Commit API keys to GitHub
- Share your `.env` file
- Hardcode API keys in your code

---

## 📝 `.gitignore` Configuration

Make sure these lines are in your `.gitignore`:

```gitignore
# Environment variables
.env
.env.local

# Streamlit secrets
.streamlit/secrets.toml
```

---

## 🐛 Troubleshooting

### "Gemini API key not found or not configured"

**On Streamlit Cloud:**
- Check that you've added the secret correctly
- Make sure the key name is exactly `GEMINI_API_KEY`
- Verify the TOML format is correct (no quotes around the key name)
- Restart the app after adding secrets

**Locally:**
- Ensure `.env` file exists in project root
- Check the key is spelled correctly: `GEMINI_API_KEY`
- Restart your Streamlit app after editing `.env`

### Model Not Found Error (404)

The model name has been updated to `gemini-1.5-flash` (stable version). If you still get errors:
- Wait a few minutes and try again (API might be updating)
- Check [Google AI Studio](https://aistudio.google.com) for model availability
- Verify your API key is active and has proper permissions

---

## 📊 Monitoring Usage

Track your Gemini API usage:
- Visit [Google AI Studio](https://aistudio.google.com)
- Go to **"API Keys"** section
- View usage statistics and limits

---

## 🆘 Need Help?

- **Streamlit Docs:** [docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)
- **Google AI Studio:** [aistudio.google.com](https://aistudio.google.com)
- **Gemini API Docs:** [ai.google.dev/docs](https://ai.google.dev/docs)

---

## ✨ Your App is Production-Ready!

Both OCR engines (Microsoft TrOCR and Google Gemini) will work seamlessly:
- **Locally:** Using your `.env` file
- **On Streamlit Cloud:** Using Streamlit Secrets

No code changes needed! 🎉
