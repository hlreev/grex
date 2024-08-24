// Google Drive folder ID where logs will be stored
var FOLDER_ID = '1gAzvWyBKDLGpr8RQSi5Y9MXMpnium0mt';

// Log file names
var DEBUG_FILE_NAME = 'debug.txt';
var OUTPUT_FILE_NAME = 'output.txt';

/**
 ** Sleep function to create a delay.
 **/
function sleep(ms) {

  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 ** Logs messages with optional severity levels at the current time of execution to 'debug.txt'. Default severity is "INFO" for all logging.
 ** Severity options are as follows: INFO - Generic runtime information, WARNING - Something may have went wrong, ERROR - Something definitely went wrong, SUCCESS - Run completed with no errors/warnings
 **/
async function debugLog(message, severity = "INFO") {
  severity = severity.toUpperCase();

  const validSeverities = ["INFO", "WARNING", "ERROR", "SUCCESS"];

  if (!validSeverities.includes(severity)) {
    console.warn(`Invalid severity level "${severity}" provided. Defaulting to "INFO".`);
    severity = "INFO";
  }

  var timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss");

  appendToFile(DEBUG_FILE_NAME, `[${timestamp}] [${severity}] ${message}`);
  
  // Mininum delay - 100, Safe delay - 200, Maximum delay - 300
  await sleep(100);
}

/**
 ** Logs user entry information at the current time of execution to 'output.txt'.
 **/
function entryLog(entry, matchFound) {
  var matchStatus = matchFound ? "TRUE" : "FALSE";

  // Specify the desired order for the user entry info for consistent logging purposes
  const orderedEntry = {
    hazard: entry.hazard,
    selected_days: entry.selected_days,
    peak_day: entry.peak_day,
    confidence: entry.confidence
  };

  console.log(matchStatus);

  log(`Match Found: ${matchStatus} | User entry info: ${JSON.stringify(orderedEntry)}`);
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