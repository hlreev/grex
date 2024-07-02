// Google Drive folder ID where logs will be stored
var FOLDER_ID = '1gAzvWyBKDLGpr8RQSi5Y9MXMpnium0mt';

// Log file names
var DEBUG_FILE_NAME = 'debug.txt';
var OUTPUT_FILE_NAME = 'output.txt';

/**
 ** Logs messages with optional severity levels at the current time of execution to 'debug.txt'.
 **/
function debugLog(message, severity = "INFO") {
  var timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss");

  appendToFile(DEBUG_FILE_NAME, `[${timestamp}] [${severity}] ${message}`);
}

/**
 ** Logs user entry information at the current time of execution to 'output.txt'.
 **/
function entryLog(entry, matchFound) {
  var matchStatus = matchFound ? "T" : "F";

  log(`Match Found: ${matchStatus} | User entry info: ${JSON.stringify(entry)}`);
}

/**
 ** Clears the content of both log files upon execution.
 **/
function clearLogs() {
  var folder = DriveApp.getFolderById(FOLDER_ID);
  var debugLog = folder.getFilesByName(DEBUG_FILE_NAME);
  var entryLog = folder.getFilesByName(OUTPUT_FILE_NAME);

  if (debugLog.hasNext()) {
    debugLog.next().setContent('');
  }
  if (entryLog.hasNext()) {
    entryLog.next().setContent('');
  }
}

/**
 ** Helper function: Logs messages to a file, similar to the built-in print function.
 **/
function log(...args) {
  var timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss");

  appendToFile(OUTPUT_FILE_NAME, `[${timestamp}] ` + args.join(' '));
}

/**
 ** Helper function: Appends a log entry to a file in Google Drive.
 **/
function appendToFile(fileName, content) {
  var folder = DriveApp.getFolderById(FOLDER_ID);
  var files = folder.getFilesByName(fileName);
  var file;

  if (files.hasNext()) {
    file = files.next();
  } 
  else {
    file = folder.createFile(fileName, '');
  }

  var currentContent = file.getBlob().getDataAsString();

  file.setContent(currentContent + '\n' + content);
}