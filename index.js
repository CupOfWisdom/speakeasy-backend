const express = require("express");
const multer = require("multer");
const { exec } = require("child_process");
const fs = require("fs");
const path = require("path");

// Initialize Express app
const app = express();
const port = 3000;

// Configure multer for file uploads
const upload = multer({ dest: "uploads/" });

// Endpoint to upload and process a video
app.post("/analyze-video", upload.single("video"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "No file uploaded." });
  }

  const videoPath = req.file.path;
  const outputDir = path.join(__dirname, "results");

  // Create the results directory if it doesn't exist
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
  }

  // Call the Python script to analyze the video
  const pythonScriptPath = path.join(__dirname, "videoprocessing.py");
  const pythonCommand = `python ${pythonScriptPath} ${videoPath} ${outputDir}`;

  exec(pythonCommand, (pythonError, pythonStdout, pythonStderr) => {
    if (pythonError) {
      console.error(`Python error: ${pythonStderr}`);
      return res.status(500).json({ error: "Failed to analyze emotions." });
    }

    // Read the generated JSON file
    const jsonFiles = fs.readdirSync(outputDir).filter((file) => file.endsWith(".json"));
    if (jsonFiles.length === 0) {
      return res.status(500).json({ error: "No analysis results found." });
    }

    const latestJsonFile = jsonFiles[jsonFiles.length - 1];
    const jsonFilePath = path.join(outputDir, latestJsonFile);
    const emotionData = JSON.parse(fs.readFileSync(jsonFilePath, "utf8"));

    // Clean up: Delete the uploaded video and JSON file
    fs.unlinkSync(videoPath);
    fs.unlinkSync(jsonFilePath);

    // Return the emotion analysis results
    res.json(emotionData);
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});