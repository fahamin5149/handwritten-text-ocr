# 🔑 API Key Configuration - Quick Reference

## Overview

Your app now supports **both local and cloud deployment** with automatic API key detection:

```
┌─────────────────────────────────────────────┐
│   Running Location Detection                │
├─────────────────────────────────────────────┤
│                                             │
│   Is Streamlit Cloud? ──Yes──> Use st.secrets['GEMINI_API_KEY']
│         │                                   │
│        No                                   │
│         │                                   │
│         └──> Use os.getenv('GEMINI_API_KEY') from .env
│                                             │
└─────────────────────────────────────────────┘
```

---

## Local Development Setup

### File: `.env` (in project root)
```bash
GEMINI_API_KEY=AIza...your_actual_key_here
```

**Status:** ✅ Already configured
**Location:** `e:\University\PPIT\handwritten-text-ocr\.env`
**Git:** Ignored (won't be committed)

---

## Streamlit Cloud Setup

### Configure via Dashboard

1. **Navigate to:** [share.streamlit.io](https://share.streamlit.io)
2. **Find your app** in the dashboard
3. **Click:** ⚙️ Settings → Secrets
4. **Add this:**

```toml
GEMINI_API_KEY = "AIza...your_actual_key_here"
```

5. **Save** → App restarts automatically ✅

### Example Screenshot Flow:
```
Streamlit Dashboard
  └─> Your App
      └─> ⚙️ (Settings menu)
          └─> Secrets
              └─> [Text editor appears]
                  └─> Paste: GEMINI_API_KEY = "your_key"
                  └─> Click "Save"
```

---

## Code Changes Summary

### Before (Only local .env):
```python
api_key = os.getenv("GEMINI_API_KEY")
```

### After (Both local and cloud):
```python
# Try Streamlit secrets first (cloud)
try:
    import streamlit as st
    if 'GEMINI_API_KEY' in st.secrets:
        api_key = st.secrets['GEMINI_API_KEY']
except:
    pass

# Fall back to .env (local)
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")
```

---

## Security Checklist

- [x] `.env` added to `.gitignore`
- [x] `.streamlit/secrets.toml` added to `.gitignore`
- [x] Code checks Streamlit secrets first
- [x] Falls back to environment variables
- [x] Clear error messages for missing keys

---

## Files Created/Updated

| File | Purpose | Action |
|------|---------|--------|
| `core/ocr_engine.py` | Updated API key detection | ✏️ Modified |
| `.gitignore` | Prevent secrets from being committed | ✏️ Updated |
| `.streamlit/secrets.toml.example` | Template for local secrets | ➕ Created |
| `DEPLOYMENT_GUIDE.md` | Detailed deployment instructions | ➕ Created |
| `API_KEY_SETUP.md` | This quick reference | ➕ Created |

---

## Testing Checklist

### Local Testing:
- [ ] `.env` file has your API key
- [ ] Run `streamlit run gui/streamlit_app.py`
- [ ] Select "Google Gemini" engine
- [ ] Upload image and convert
- [ ] Check console: "Using Gemini API key from .env file"

### Cloud Testing:
- [ ] Secrets configured in Streamlit Cloud dashboard
- [ ] App deployed successfully
- [ ] Select "Google Gemini" engine
- [ ] Upload image and convert
- [ ] Check logs: "Using Gemini API key from Streamlit secrets"

---

## Troubleshooting

### Local Issue: "Gemini API key not found"
```bash
# Check if .env exists
ls .env

# Check content (without exposing key)
cat .env | grep GEMINI

# Verify format (no spaces around =)
GEMINI_API_KEY=your_key_here  ✅ Correct
GEMINI_API_KEY = your_key_here  ❌ Might cause issues
```

### Cloud Issue: "Gemini API key not found"
1. Open Streamlit Cloud dashboard
2. Check Secrets section
3. Verify exact spelling: `GEMINI_API_KEY`
4. Ensure TOML format is correct
5. Save and wait for app to restart (30-60 seconds)

---

## Additional Notes

- **Model Updated:** Changed from `gemini-2.5-flash` to `gemini-1.5-flash` (stable)
- **Deprecation Fixed:** Updated `use_container_width` to `width='stretch'`
- **No code changes needed** when deploying - works automatically!

---

## Quick Commands

```bash
# Test locally
streamlit run gui/streamlit_app.py

# Check if secrets are in git (should return nothing)
git ls-files | grep -E '(\.env|secrets\.toml)$'

# Verify .gitignore is working
git status

# Push to GitHub (secrets won't be included)
git add .
git commit -m "Updated for cloud deployment"
git push
```

---

**You're all set! 🎉**

Your app will automatically use:
- `.env` when running locally
- Streamlit Secrets when deployed on Streamlit Cloud
