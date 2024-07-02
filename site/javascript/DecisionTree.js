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
    const questions = data.trees[matchIndex].questions;
    
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
 ** Attemps to find a match based on initial conditions after checking against the loaded data via JSON file.
 **/
function findMatch(initialConditions, { hazard, peak_day, confidence, uncertainty }) {
  peak_day = parseInt(peak_day);

  return initialConditions.findIndex(condition => 
    condition.hazard === hazard &&
    condition.day_min <= peak_day && peak_day <= condition.day_max &&
    condition.conf_min <= confidence && confidence <= condition.conf_max &&
    condition.uncertainty === uncertainty
  );
}

/**
 ** TODO: Copies the recommended graphicast determined by the matched decision tree to the current slide for the forecaster to use.
 **/
function copyRecommendedGraphicast() {
  var presentation = SlidesApp.getActivePresentation();
  var selection = presentation.getSelection();
  var currentPage = selection.getCurrentPage();

  // Check if a slide is selected
  if (currentPage && currentPage.getPageType() === SlidesApp.PageType.SLIDE) {
    var currentSlide = currentPage.asSlide();

    // Get the ID of the current slide
    var slideId = currentSlide.getObjectId();

    // Get the index of the current slide
    var slides = presentation.getSlides();
    var currentIndex = slides.findIndex(slide => slide.getObjectId() === slideId);

    // Duplicate the current slide
    var newSlide = currentSlide.duplicate();

    // Move the new slide to the position right after the current slide
    newSlide.move(currentIndex + 1);
    
    // Message when copy was successful
    google.script.run.debugLog('Recommended graphicast has been successfully added.');
  } 
  else {
    // Message when copy was not successful
    google.script.run.debugLog('No slide is currently selected.', severity = 'WARNING');
  }
}