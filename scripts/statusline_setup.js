#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

const PLUGIN_NAME = "cc-distribution";

const projectDir = process.env.CLAUDE_PROJECT_DIR || process.cwd();
const settingsPath = path.join(projectDir, ".claude", "settings.json");

const readSettings = () => {
  try {
    return JSON.parse(fs.readFileSync(settingsPath, "utf8"));
  } catch (err) {
    return {};
  }
};

const writeSettings = (settings) => {
  fs.mkdirSync(path.dirname(settingsPath), { recursive: true });
  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + "\n");
};

const statuslineCommand = () =>
  "bash -lc '" +
  "plugin_dir=$(ls -td ~/.claude/plugins/cache/" +
  PLUGIN_NAME +
  "/" +
  PLUGIN_NAME +
  "/*/ 2>/dev/null | head -1);" +
  "if [ -z \"$plugin_dir\" ]; then exit 0; fi;" +
  "node \"${plugin_dir}scripts/statusline.js\"'";

const settings = readSettings();
if (!settings.statusLine) {
  settings.statusLine = {
    type: "command",
    command: statuslineCommand(),
  };
  writeSettings(settings);
}
