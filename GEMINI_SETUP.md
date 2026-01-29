# Setting Up Google Gemini OCR

This application now supports **two OCR engines**:
1. **Microsoft TrOCR** - Specialized for handwritten text recognition
2. **Google Gemini** - Advanced multimodal AI with strong image understanding

## Getting Your Gemini API Key

To use the Gemini OCR engine, you need to obtain a free API key from Google:

### Step 1: Get API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Copy your API key

### Step 2: Configure the Application
1. Open the `.env` file in the project root directory
2. Replace `your_gemini_api_key_here` with your actual API key:
   ```
   GEMINI_API_KEY=AIza...your_actual_key_here
   ```
3. Save the file

### Step 3: Run the Application
```bash
streamlit run gui/streamlit_app.py
```

## Choosing Between OCR Engines

### Microsoft TrOCR
- ✅ **Best for**: Handwritten text, offline processing
- ✅ **Pros**: Free, runs locally, specialized for handwriting
- ⚠️ **Cons**: Requires model download (~500MB), processes regions separately

### Google Gemini
- ✅ **Best for**: Complex layouts, mixed content, high accuracy
- ✅ **Pros**: State-of-the-art AI, excellent with both print and handwriting
- ⚠️ **Cons**: Requires internet connection and API key, usage limits apply

## API Usage & Limits

Google Gemini offers a **free tier** with generous limits:
- Free requests per minute
- Sufficient for personal projects and testing

For more details, visit: [Google AI Pricing](https://ai.google.dev/pricing)

## Troubleshooting

### "Gemini API key not found or not configured"
- Ensure you've set `GEMINI_API_KEY` in the `.env` file
- Make sure the `.env` file is in the project root directory
- Restart the Streamlit app after updating the `.env` file

### "Failed to initialize Gemini client"
- Check your internet connection
- Verify your API key is valid and active
- Ensure `google-genai` package is installed: `pip install google-genai`

## Privacy & Security

- ⚠️ **Never commit your `.env` file to version control**
- The `.env` file is already in `.gitignore` to prevent accidental commits
- Your images are sent to Google's API when using Gemini OCR
- Microsoft TrOCR processes everything locally on your machine

## Support

For more information about Google Gemini:
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Image Understanding Guide](https://ai.google.dev/gemini-api/docs/vision)
