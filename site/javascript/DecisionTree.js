// findMatch returns a -1 when no element exists to satisfy the function (meaning no match is found, in this case)
const NO_MATCH = -1;

/**
 ** Process the user submitted form data from the entry page against initial conditions in the database.
 **/
function processInitialConditions(formData) {
  const data = loadDecisionTreeData();
  const initialConditions = data.trees.map(tree => tree.initial_conditions);
  const matchIndex = findMatch(initialConditions, formData);
  
  // Check for a match through each decision tree in the loaded data
  if (matchIndex !== NO_MATCH) {
    const questions = data.trees[matchIndex].question_sets;
    
    return { matchFound: true, questions };
  }

  return { matchFound: false, questions: null };
}

/**
 ** Load the decision trees (JSON file: model_data_v2.json) from Google Drive.
 **/
function loadDecisionTreeData() {
  var fileId = '1efQT-dUV2AF8vFatVoHLcD1GwtT0KjhN';
  var file = DriveApp.getFileById(fileId);
  var content = file.getBlob().getDataAsString();

  return JSON.parse(content);
}

/**
 ** Attempts to find a match based on initial conditions after checking against the loaded data via JSON file.
 **/
function findMatch(initialConditions, { hazard, peak_day, confidence }) {
  peak_day = parseInt(peak_day);

  return initialConditions.findIndex(condition => 
    condition.hazard === hazard &&
    condition.day_min <= peak_day && peak_day <= condition.day_max &&
    condition.conf_min <= confidence && confidence <= condition.conf_max
  );
}

/**
 ** Finds the matching slide based on a specific presentation ID and the speaker notes text on the slide
 **/
function getSlideBySpeakerNote(presentationId, noteText) {
  var presentation = SlidesApp.openById(presentationId);
  var slides = presentation.getSlides();
  
  // Loop through slides to find the one with the matching note
  for (var i = 0; i < slides.length; i++) {
    var slide = slides[i];
    var notes = slide.getNotesPage().getSpeakerNotesShape().getText().asString();
    
    if (notes.includes(noteText)) {
      
      return slide;
    }
  }
  
  google.script.run.debugLog("The slide with the following speaker note was not found: " + noteText, "ERROR")
  throw new Error("Slide with the note '" + noteText + "' not found.");
}

/**
 ** Copies the recommended graphicast determined by the matched decision tree to the current slide for the forecaster to use
 **/
function copyRecommendedGraphicast(decisionText, GRAPHICAST_MAP) {
  // Obtain the graphicast to be copied into the new presentation
  var graphicInfo = GRAPHICAST_MAP[decisionText];
  
  // Prepare the presentation for the slide copying
  var currentPresentation = SlidesApp.getActivePresentation();
  
  // Get the slide by its note text
  var sourceSlide = getSlideBySpeakerNote(graphicInfo.presentationId, decisionText);
  var duplicatedSlide = sourceSlide.duplicate();
  
  // Append the duplicated slide to the current presentation
  var newSlide = currentPresentation.appendSlide(duplicatedSlide);
  
  // Move the new slide to the end of the presentation
  newSlide.move(currentPresentation.getSlides().length - 1);
  
  // Remove the duplicated slide from the source presentation
  duplicatedSlide.remove();
}