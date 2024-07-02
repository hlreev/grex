// Set the title for the Sidebar/menu pages
var title = 'Probabilistic Graphicast Recommender'

/**
 ** Adds the GRex menu to Google Slides on start-up, handles all sub-menu items.
 **/
function onOpen() {
  SlidesApp.getUi()
    .createMenu('GRex')
    .addItem('Run Graphicast Recommender', 'showSidebar')
    .addSeparator()
    .addItem('Help', 'showHelpDialog')
    .addToUi();
}

/**
 ** Loads H_Entry_Page.html into the sidebar when button is clicked.
 **/
function showSidebar() {
  var html = HtmlService.createHtmlOutputFromFile('H_Entry_Page')
    .setTitle(title);
      
  SlidesApp.getUi().showSidebar(html);
}

/**
 ** Loads H_Help_Page.html into the sidebar when button is clicked.
 **/
function showHelpDialog() {
  var html = HtmlService.createHtmlOutputFromFile('H_Help_Page')
    .setWidth(400)
    .setHeight(300);

  SlidesApp.getUi().showModalDialog(html, 'GRex Help');
}

/**
 ** Loads H_Query_Page.html into the sidebar when a match is found after submitting the entry data form.
 **/
function showDecisionTree(questions) {
  var htmlOutput = HtmlService.createHtmlOutputFromFile('H_Query_Page')
    .setTitle(title)

  // Send over the decision tree questions for access on the new page
  htmlOutput.append(`<script>var questions = ${JSON.stringify(questions)};</script>`);
  
  SlidesApp.getUi().showSidebar(htmlOutput);
}