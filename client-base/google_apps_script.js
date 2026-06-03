/**
 * Paste into Google Sheets: Extensions → Apps Script
 * Then reload sheet → menu "Client Base"
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("Client Base")
    .addItem("Sort Pipeline by Priority", "sortByPriority")
    .addItem("Highlight Hot + Client rows", "highlightHot")
    .toBrowser();
}

function sortByPriority() {
  const sheet = getPipelineSheet();
  if (!sheet) return;
  const lastRow = sheet.getLastRow();
  const lastCol = sheet.getLastColumn();
  if (lastRow < 2) return;
  sheet.getRange(2, 1, lastRow - 1, lastCol).sort([
    { column: 3, ascending: false },
    { column: 1, ascending: true },
  ]);
  SpreadsheetApp.getUi().alert("Sorted by Priority Score (column C).");
}

function highlightHot() {
  const sheet = getPipelineSheet();
  if (!sheet) return;
  const lastRow = sheet.getLastRow();
  sheet.getRange(2, 1, lastRow - 1, sheet.getLastColumn()).setBackground(null);
  const catCol = 2;
  const data = sheet.getRange(2, catCol, lastRow - 1, 1).getValues();
  for (let i = 0; i < data.length; i++) {
    const cat = String(data[i][0]);
    if (cat === "Hot" || cat === "Client") {
      sheet.getRange(i + 2, 1, 1, sheet.getLastColumn()).setBackground("#FFF2CC");
    }
  }
  SpreadsheetApp.getUi().alert("Highlighted Hot and Client rows.");
}

function getPipelineSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const names = ["Pipeline Upgraded", "Sheet1", "工作表1"];
  for (const n of names) {
    const s = ss.getSheetByName(n);
    if (s) return s;
  }
  SpreadsheetApp.getUi().alert("Sheet not found. Rename tab to Pipeline Upgraded.");
  return null;
}
