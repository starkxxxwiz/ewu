# 🎓 EWU Course Fetching Tool

A beautiful, interactive terminal-based Python tool for fetching course schedules from the East West University (EWU) portal and exporting them to professional PDF reports.

> **⚠️ Educational Purpose Only**: This tool is designed for educational purposes to help students efficiently access their course information.

## ✨ Features

- 🔐 **Secure Authentication** - Direct integration with EWU portal authentication system
- 📊 **Real-time Course Data** - Fetches live course schedules, availability, and details
- 🎨 **Beautiful Terminal UI** - Clean, single-screen interface with smooth transitions
- 📄 **Professional PDF Export** - Generate well-formatted PDF reports with course details
- ⚡ **Fast & Reliable** - Optimized HTTP requests with proper session management
- 🔒 **Password Security** - Hidden password entry using secure input methods
- 📈 **Course Statistics** - View total courses, capacity, availability at a glance

## 📋 Requirements

- Python 3.7 or higher
- Internet connection
- Valid EWU portal credentials

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Tool

```bash
python main.py
```

Or on Windows, simply double-click:
```
run.bat
```

### Step 3: Follow the Interactive Prompts

1. Enter your Student ID
2. Enter your password (hidden)
3. View course statistics
4. Confirm to save PDF report
5. PDF saved to `output/` folder!

## 📦 Installation (Detailed)

### For Windows Users

1. **Download/Clone the Project**
   ```bash
   git clone <repository-url>
   cd tool
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Using Batch File**
   - Double-click `run.bat`
   - Or run in command prompt: `run.bat`

### For Linux/Mac Users

1. **Download/Clone the Project**
   ```bash
   git clone <repository-url>
   cd tool
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Tool**
   ```bash
   python3 main.py
   ```

## 💻 Usage

### Interactive Workflow

The tool provides a clean, single-screen experience:

**Screen 1: Authentication**
```
  ______       ____  __  ______            __
 / ____/ | | /| / / / / / /_  __/___  ____  / /
/ __/  | | /| / / / / / / / / / __ \/ __ \/ / 
/ /___ | |/ |/ / /_/ /  /_/ / / / /_/ / /_/ / /  
\____/|__/|__/\____/_/\____/_/  \____/\____/_/   

======================================================================
                    EWU Course Fetching Tool
                     Secure • Fast • Reliable
           This is educational tool just for course fetching.
======================================================================

🆔 Student ID: 2020-1-60-123
🔒 Password: ********
```

**Screen 2: Course Fetching**
```
  ______       ____  __  ______            __
 [Banner remains visible]

⏳ Connecting to server...
📡 Fetching course data...
📋 Parsing response...

✅ Successfully fetched 331 courses!
⏱️  Completed in 3.34 seconds

======================================================================

   📚 Total Courses:       331
   ⏱️  Fetch Time:          3.34s
   💺 Total Capacity:      10017
   ✅ Total Taken:         9677
   🎯 Total Available:     340

======================================================================

❓ Would you like to save this data as a PDF report? [Y/n]:
```

**Screen 3: Success**
```
  ______       ____  __  ______            __
 [Banner remains visible]

✅ PDF saved successfully!
ℹ️  Location: C:\path\to\output\EWU_Courses_2025-10-07_21-30-45.pdf

======================================================================
           Thank you for using EWU Course Filter Tool!
                     Have a productive day 👋
======================================================================
```

## 📂 Project Structure

```
tool/
├── main.py              # Main application entry point
├── auth.py              # EWU portal authentication
├── fetch_courses.py     # Course data fetching and parsing
├── pdf_export.py        # PDF report generation
├── utils.py             # Terminal UI utilities
├── requirements.txt     # Python dependencies
├── run.bat             # Windows batch file launcher
├── output/             # PDF reports saved here
│   └── README.txt
└── README.md           # This file
```

## 🔧 Module Overview

### `main.py` - Application Controller
- Orchestrates the entire workflow
- Manages authentication and course fetching
- Handles user interactions
- Controls screen clearing and banner display

### `auth.py` - Authentication Module
- Replicates EWU portal authentication
- Manages session cookies
- Handles login requests
- Supports retry logic

### `fetch_courses.py` - Course Fetcher
- Fetches course data via authenticated API
- Parses JSON responses
- Formats course information
- Error handling and validation

### `pdf_export.py` - PDF Generator
- Creates professional PDF reports
- Landscape A4 layout
- Color-coded headers
- Alternating row backgrounds
- Auto-pagination support

### `utils.py` - UI Utilities
- ASCII banner generation
- Colored console output
- Course summary display
- User input prompts
- Screen management

## 📄 PDF Report Features

Generated PDFs include:
- 📋 Complete course listing
- 🏫 Course codes and sections
- 👨‍🏫 Faculty information
- 💺 Seat capacity, taken, and availability
- 📅 Day and time information
- 🏢 Room locations
- ⏰ Generation timestamp
- 🆔 Student ID

**Layout:**
- Landscape A4 format for better table viewing
- Color-coded header (blue)
- Alternating row colors for readability
- Professional styling and alignment

## ⚙️ Configuration

### Output Directory
PDFs are saved to the `output/` folder by default. This folder is created automatically.

### Session Management
- Sessions are temporary and not persisted
- Automatic session cleanup after execution
- No credential storage

## ⚠️ Troubleshooting

### Common Issues

**1. SSL Certificate Errors**
```
The tool disables SSL verification for compatibility with EWU portal.
This is intentional and matches the original PHP implementation.
```

**2. Authentication Failed**
- ✅ Verify credentials are correct
- ✅ Check internet connection
- ✅ Ensure EWU portal is accessible
- ✅ Wait a moment and try again

**3. Module Not Found Error**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**4. PDF Generation Failed**
- ✅ Check write permissions in output folder
- ✅ Ensure sufficient disk space
- ✅ Verify reportlab is installed correctly

**5. Import Errors**
```bash
# Ensure you're in the correct directory
cd tool
pip install -r requirements.txt
```

## 🔒 Security & Privacy

- ✅ Passwords are never stored or logged
- ✅ Secure password input (hidden from terminal)
- ✅ Session cookies are temporary
- ✅ No data sent to third parties
- ✅ All data stays on your local machine
- ✅ HTTPS connection to EWU portal

## 📝 Dependencies

```
requests==2.31.0        # HTTP library for API calls
rich==13.7.0            # Beautiful terminal formatting
pyfiglet==1.0.2         # ASCII art generation
reportlab==4.0.7        # PDF generation
urllib3==2.1.0          # HTTP utilities
```

Install all at once:
```bash
pip install -r requirements.txt
```

## 🎯 Use Cases

- 📚 **Course Planning** - View all available courses and plan your semester
- 📊 **Availability Tracking** - Check seat availability across all courses
- 📄 **Record Keeping** - Save course schedules as PDF for future reference
- 🔍 **Course Research** - Browse course offerings with faculty and timing details
- 📱 **Offline Access** - Export and view course data without internet

## 🌟 Best Practices

1. **Run Regularly** - Course availability changes frequently
2. **Save PDFs** - Keep records of different fetch times to compare availability
3. **Check Output Folder** - PDFs are timestamped for easy organization
4. **Verify Credentials** - Ensure you're using correct Student ID format

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Code Style** - Follow PEP 8 guidelines
2. **Testing** - Test all features before submitting
3. **Documentation** - Update README for new features
4. **Comments** - Add clear comments for complex logic

## 📜 License

This project is for educational purposes only. Use responsibly and in accordance with East West University's terms of service.

## 🎉 Acknowledgments

Built with powerful Python libraries:
- **Rich** - Beautiful terminal UI ([https://github.com/Textualize/rich](https://github.com/Textualize/rich))
- **ReportLab** - Professional PDF generation ([https://www.reportlab.com/](https://www.reportlab.com/))
- **PyFiglet** - ASCII art generation ([https://github.com/pwaller/pyfiglet](https://github.com/pwaller/pyfiglet))
- **Requests** - HTTP for Humans ([https://requests.readthedocs.io/](https://requests.readthedocs.io/))

## 📧 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Verify all dependencies are installed correctly
3. Ensure you're using Python 3.7 or higher
4. Check that you have a stable internet connection

## 🚀 Future Enhancements

Potential improvements (contributions welcome):
- [ ] Course filtering by department
- [ ] Export to CSV format
- [ ] Email notification for seat availability
- [ ] Course comparison between semesters
- [ ] Advanced search and filtering
- [ ] Multiple export format options

---

**Made with ❤️ for EWU Students**

*Happy Course Browsing! 🎓*
