// Set the title for the Sidebar/menu pages
var title = 'Probabilistic Graphicast Recommender'

// Add the GRex menu option and the submenu options
function onOpen() {
  SlidesApp.getUi()
    .createMenu('GRex')
    .addItem('Run Graphicast Recommender', 'showSidebar')
    .addSeparator()
    .addItem('Help', 'showHelpDialog')
    .addToUi();
}

// Load Entry_Page.html into the sidebar when button is clicked
function showSidebar() {
  var html = HtmlService.createHtmlOutputFromFile('Entry_Page')
    .setTitle(title);
      
  SlidesApp.getUi().showSidebar(html);
}

// Load Help_Page.html into the sidebar when button is clicked
function showHelpDialog() {
  var html = HtmlService.createHtmlOutputFromFile('Help_Page')
    .setWidth(400)
    .setHeight(300);

  SlidesApp.getUi().showModalDialog(html, 'GRex Help');
}

// Load DecisionTree_Page.html into the sidebar when matching initial conditions are found
function showDecisionTree(questions) {
  var htmlOutput = HtmlService.createHtmlOutputFromFile('DecisionTree_Page')
    .setTitle(title)

  // Send over the decision tree questions for access on the new page
  htmlOutput.append(`<script>var questions = ${JSON.stringify(questions)};</script>`);
  
  SlidesApp.getUi().showSidebar(htmlOutput);
}