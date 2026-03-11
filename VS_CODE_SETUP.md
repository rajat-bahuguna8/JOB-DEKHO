# 🎯 Running JOB DEKHO in VS Code

## 🚀 Quick Start (3 Steps)

### Step 1: Open in VS Code
1. Open VS Code
2. **File → Open Folder**
3. Select: `C:\Users\PC\Desktop\Job_Dekho`

### Step 2: Open Terminal
- Press `` Ctrl + ` `` (backtick key)
- Or: **Terminal → New Terminal** from menu

### Step 3: Run the App
```bash
python app.py
```

### Step 4: Open Browser
- Click the link in terminal: `http://127.0.0.1:5000`
- Or manually visit: http://127.0.0.1:5000

---

## 📋 All Methods to Run

### Method 1: Terminal Command (Recommended)
```bash
# In VS Code terminal
python app.py
```

### Method 2: Run Button
1. Open `app.py`
2. Click the **▶ Run** button (top-right corner)
3. Or press **F5**

### Method 3: Run Tasks (Professional)
1. Press **Ctrl + Shift + P**
2. Type: `Tasks: Run Task`
3. Select: **Run JOB DEKHO**

Or press **Ctrl + Shift + B** (Build Task)

### Method 4: Debug Mode
1. Press **F5**
2. Select: **Python: Run app.py**
3. Set breakpoints by clicking left of line numbers

---

## ⚙️ VS Code Configuration

I've created VS Code configuration files for you:

### Files Created:
- ✅ `.vscode/tasks.json` - Task definitions
- ✅ `.vscode/launch.json` - Debug configurations
- ✅ `.vscode/settings.json` - Project settings

### Available Tasks:
- **Run JOB DEKHO** - Start the application
- **Initialize Database** - Setup database with sample data
- **Run Tests** - Execute test suite

---

## 🔧 Recommended VS Code Extensions

Install these for better development experience:

### Python Extension (Essential)
- **Name:** Python
- **ID:** ms-python.python
- **Install:** `Ctrl + Shift + X` → Search "Python" → Install

### HTML/CSS/JS Extensions (Optional but Helpful)
- **HTML CSS Support** - IntelliSense for HTML
- **Auto Rename Tag** - Auto rename paired tags
- **Prettier** - Code formatter
- **Live Server** - Preview HTML files

---

## 📁 VS Code File Explorer

Your project structure in VS Code:

```
JOB_DEKHO/
├── .vscode/           ← VS Code configuration
│   ├── tasks.json     ← Run tasks
│   ├── launch.json    ← Debug configs
│   └── settings.json  ← Project settings
├── templates/         ← HTML files
├── static/            ← CSS & JS
├── uploads/           ← Resume files
├── app.py            ← Main application
├── models.py         ← Database models
└── ... (other files)
```

---

## 🎯 Common VS Code Shortcuts

### Running the App:
- **Ctrl + Shift + B** - Run build task (starts app)
- **F5** - Start debugging
- **Ctrl + C** - Stop the server (in terminal)

### Navigation:
- **Ctrl + P** - Quick file open
- **Ctrl + Shift + F** - Search across files
- **Ctrl + B** - Toggle sidebar
- **Ctrl + `** - Toggle terminal

### Editing:
- **Ctrl + /** - Comment/uncomment line
- **Alt + Up/Down** - Move line up/down
- **Shift + Alt + F** - Format document
- **F2** - Rename symbol

---

## 🐛 Debugging in VS Code

### Set Breakpoints:
1. Click left margin next to line number (red dot appears)
2. Press **F5** to start debugging
3. App pauses at breakpoints

### Debug Controls:
- **F5** - Continue
- **F10** - Step over
- **F11** - Step into
- **Shift + F11** - Step out
- **Shift + F5** - Stop

### View Variables:
- Left sidebar shows all variables
- Hover over variables to see values
- Watch specific variables in Watch panel

---

## 📊 Using Integrated Terminal

### Multiple Terminals:
1. Click **+** in terminal panel
2. Run different commands in each:
   - Terminal 1: `python app.py`
   - Terminal 2: `python test_project.py`

### Terminal Types:
- **PowerShell** (default on Windows)
- **Command Prompt**
- **Git Bash** (if installed)

Change terminal: Click dropdown next to **+**

---

## ✨ VS Code Features for This Project

### IntelliSense (Auto-complete):
- Type `@app.` - Shows available methods
- Type `db.` - Shows database operations
- Ctrl + Space - Trigger suggestions

### Go to Definition:
- **F12** - Go to definition
- **Ctrl + Click** - Jump to definition
- **Alt + Left** - Go back

### Find References:
- **Shift + F12** - Find all references
- Right-click → "Find All References"

### Rename Symbol:
- **F2** - Rename across all files
- Updates everywhere automatically

---

## 🔄 Git Integration

VS Code has built-in Git support:

### Source Control Panel:
- **Ctrl + Shift + G** - Open source control
- View changes, stage files, commit
- Push/pull from VS Code

### Git Commands:
- Click branch name (bottom-left)
- Create branches, switch branches
- View history with Timeline view

---

## 📝 Editing HTML Templates

### Features:
- **Emmet** - Fast HTML writing
  - Type `div.card>h1+p` → Press Tab
- **Auto Close Tags** - Automatically closes tags
- **Jinja Syntax** - Supports `{% %}` and `{{ }}`

### Live Preview:
1. Install "Live Server" extension
2. Right-click HTML file
3. Select "Open with Live Server"

---

## 🎨 Editing CSS

### Features:
- **Color Preview** - Shows color squares
- **IntelliSense** - CSS property suggestions
- **Hover Info** - See CSS documentation

### Format CSS:
- **Shift + Alt + F** - Format document
- Auto-indent, organize properties

---

## 🔍 Search & Replace

### Search:
- **Ctrl + F** - Find in file
- **Ctrl + H** - Replace in file
- **Ctrl + Shift + F** - Search all files
- **Ctrl + Shift + H** - Replace all files

### Regex Support:
- Click `.*` button for regex
- Search patterns across files

---

## 🚀 Running Different Commands

### In VS Code Terminal:

```bash
# Start application
python app.py

# Initialize database
python init_db.py

# Run tests
python test_project.py

# Install packages
pip install -r requirements.txt

# Check Python version
python --version
```

---

## 💡 Tips & Tricks

### Multi-Cursor Editing:
- **Alt + Click** - Add cursor
- **Ctrl + Alt + Up/Down** - Add cursor above/below
- Edit multiple lines at once

### Split Editor:
- **Ctrl + \\** - Split editor
- View multiple files side-by-side
- `app.py` and `models.py` together

### Zen Mode:
- **Ctrl + K, Z** - Distraction-free mode
- Press **Esc Esc** to exit

### Command Palette:
- **Ctrl + Shift + P** - Access all commands
- Type what you want to do
- Search available commands

---

## 🎯 Quick Workflow

### Typical Development Session:

1. **Open VS Code**
   ```
   Open folder: C:\Users\PC\Desktop\Job_Dekho
   ```

2. **Start Terminal**
   ```
   Ctrl + ` (backtick)
   ```

3. **Run Application**
   ```bash
   python app.py
   ```

4. **Edit Files**
   - Make changes to Python/HTML/CSS
   - Save: Ctrl + S

5. **Restart App**
   - Terminal: Ctrl + C (stop)
   - Run: `python app.py` (start)

6. **Test in Browser**
   - Visit: http://127.0.0.1:5000

---

## 🐛 Troubleshooting

### "Python not found"
- Install Python extension
- Check Python path in Settings

### "Port already in use"
- Kill previous process: Ctrl + C
- Or restart VS Code

### Changes not reflecting
- Stop server: Ctrl + C
- Restart: `python app.py`
- Hard refresh browser: Ctrl + Shift + R

---

## 🎊 Ready to Code!

You're all set! VS Code is configured for JOB DEKHO development.

**To start:**
1. Open folder in VS Code
2. Press `` Ctrl + ` ``
3. Type: `python app.py`
4. Visit: http://127.0.0.1:5000

Happy coding! 🚀
