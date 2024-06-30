// Load the decision trees (JSON file: model_data_v2.json) from Google Drive
function loadDecisionTrees() {
    var fileId = '1efQT-dUV2AF8vFatVoHLcD1GwtT0KjhN'; 
    var file = DriveApp.getFileById(fileId);
    var content = file.getBlob().getDataAsString();
  
    return JSON.parse(content);
  }
  
  // Process the form data against initial conditions in the database
  function processInitialConditions(formData) {
    var data = loadDecisionTrees();
    var initialConditions = data.trees.map(tree => tree.initial_conditions);
    var matchResult = findMatch(initialConditions, formData);
    
    if (matchResult.matchFound) {
      var questions = data.trees[matchResult.index].questions;
  
      return { matchFound: true, questions: questions };
    } 
    else {
  
      return { matchFound: false, questions: null };
    }
  }
  
  // Find the match based on initial conditions
  function findMatch(initialConditions, formData) {
    for (var i = 0; i < initialConditions.length; i++) {
      var condition = initialConditions[i];
  
      if (
        condition.hazard === formData.hazard &&
        condition.day_min <= parseInt(formData.peak_day) && parseInt(formData.peak_day) <= condition.day_max &&
        condition.conf_min <= formData.confidence && formData.confidence <= condition.conf_max &&
        condition.uncertainty === formData.uncertainty
      ) {
  
        return { matchFound: true, index: i };
      }
    }
  
    return { matchFound: false, index: null };
  }