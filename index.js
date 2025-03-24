const express = require("express");
const multer = require("multer");
const { exec } = require("child_process");
const fs = require("fs");
const path = require("path");

const app = express();
const port = 3000;

// Configure multer - ensure field name matches your frontend
const upload = multer({ 
  dest: "uploads/",
  fileFilter: (req, file, cb) => {
    if (file.mimetype === 'video/mp4') {
      cb(null, true);
    } else {
      cb(new Error('Only MP4 files are allowed'), false);
    }
  }
}).single("video"); // Make sure this matches your frontend's field name

// Handle file upload
app.post("/analyze-video", (req, res) => {
  upload(req, res, async (err) => {
    if (err) {
      return res.status(400).json({ error: err.message });
    }

    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded." });
    }

    try {
      // Handle Windows paths with spaces
      const videoPath = `"${req.file.path}"`;
      const outputDir = path.join(__dirname, "results");
      
      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir);
      }

      // Get absolute path to Python script
      const pythonScriptPath = path.join(__dirname, "videoprocessing.py");
      
      // Properly escape paths for Windows command line
      const command = `python "${pythonScriptPath}" "${videoPath}" "${outputDir}"`;

      exec(command, (error, stdout, stderr) => {
        if (error) {
          console.error(`Error: ${stderr}`);
          return res.status(500).json({ error: "Analysis failed" });
        }

        // Find the newest JSON file
        const jsonFiles = fs.readdirSync(outputDir)
          .filter(file => file.endsWith('.json'))
          .map(file => ({
            name: file,
            time: fs.statSync(path.join(outputDir, file)).mtime.getTime()
          }))
          .sort((a, b) => b.time - a.time);

        if (jsonFiles.length === 0) {
          return res.status(500).json({ error: "No results generated" });
        }

        const resultFile = path.join(outputDir, jsonFiles[0].name);
        const resultData = JSON.parse(fs.readFileSync(resultFile, 'utf8'));

        // Cleanup
        fs.unlinkSync(req.file.path);
        fs.unlinkSync(resultFile);

        res.json(resultData);
      });
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: "Server error" });
    }
  });
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});