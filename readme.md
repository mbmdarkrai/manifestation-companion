### Step 1: Initialize the GitHub Repository

1. Navigate to [GitHub](https://github.com/new).
2. Name the repository: `manifestation-companion`.
3. Create the repository.
4. Copy the repository URL.

### Step 2: Push Your Code to GitHub

```bash
cd manifestation-companion
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin [YOUR_GITHUB_URL]
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud

1. Go to [Streamlit Cloud](https://share.streamlit.io).
2. Click "New app".
3. Select your GitHub repository.
4. Choose `manifestation_app.py`.
5. Deploy the app.

### Optional: Add Claude API (For Full AI Features)

1. Obtain an API key from [Anthropic Console](https://console.anthropic.com).
2. In the Streamlit Cloud dashboard, go to Settings > Secrets.
3. Add:
   ```
   ANTHROPIC_API_KEY = "your-key-here"
   ```

### Usage:

- Users input a manifestation goal.
- Select from 7 tools.
- Receive personalized coaching.
- Track daily practice.
- Witness goals manifesting.

### Tips:

- Use the free version for simulated responses.
- Use the API key for unlimited personalized AI coaching.
- Compatible with mobile, tablet, and desktop.
- Sessions are fresh; no data is stored.

### Troubleshooting:

- **App Won't Start?**
  - Ensure Python version is 3.8+ or higher.
  - Run: `pip install -r requirements.txt`.

- **API Key Not Working?**
  - Verify you copied the entire key.
  - Try generating a new key.
  - Restart the app after adding the key.

- **Deployment Failing?**
  - Ensure your GitHub repo is public.
  - Confirm file names match exactly.
  - Check `gitignore` for `.streamlit/secrets.toml`.

---

YOU'RE READY TO DEPLOY! For questions, consult the deployment guide or troubleshooting docs.