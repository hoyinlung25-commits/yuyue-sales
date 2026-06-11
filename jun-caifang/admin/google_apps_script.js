/**
 * 俊才坊行政系統 · Google Sheets 自動化
 * 貼上方式：Extensions → Apps Script → 貼上此檔 → 儲存 → 重新載入試算表
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("俊才坊行政")
    .addItem("標記欠費學生", "highlightOverdue")
    .addItem("統計本月營收", "summarizeMonthlyRevenue")
    .addItem("列出今日課表", "showTodaySchedule")
    .addItem("生成繳費提醒名單", "generatePaymentReminders")
    .addToUi();
}

function getSheet(names) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  for (const n of names) {
    const s = ss.getSheetByName(n);
    if (s) return s;
  }
  SpreadsheetApp.getUi().alert("找不到工作表：" + names.join(" / "));
  return null;
}

/** 在學生資料庫標記欠費（付款狀態 = 欠費） */
function highlightOverdue() {
  const sheet = getSheet(["學生資料庫"]);
  if (!sheet) return;
  const lastRow = sheet.getLastRow();
  if (lastRow < 5) return;
  const statusCol = 8; // H 欄：付款狀態
  sheet.getRange(5, 1, lastRow - 4, sheet.getLastColumn()).setBackground(null);
  const data = sheet.getRange(5, statusCol, lastRow - 4, 1).getValues();
  let count = 0;
  for (let i = 0; i < data.length; i++) {
    if (String(data[i][0]) === "欠費") {
      sheet.getRange(i + 5, 1, 1, sheet.getLastColumn()).setBackground("#FEE2E2");
      count++;
    }
  }
  SpreadsheetApp.getUi().alert("已標記 " + count + " 名欠費學生（紅色）。");
}

/** 統計收費記錄本月實收總額 */
function summarizeMonthlyRevenue() {
  const sheet = getSheet(["收費記錄"]);
  if (!sheet) return;
  const lastRow = sheet.getLastRow();
  if (lastRow < 5) return;
  const month = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM");
  const months = sheet.getRange(5, 4, lastRow - 4, 1).getValues();
  const amounts = sheet.getRange(5, 7, lastRow - 4, 1).getValues();
  let total = 0;
  let count = 0;
  for (let i = 0; i < months.length; i++) {
    if (String(months[i][0]).indexOf(month) === 0) {
      total += Number(amounts[i][0]) || 0;
      count++;
    }
  }
  SpreadsheetApp.getUi().alert(
    "本月（" + month + "）\n已記錄收款：" + count + " 筆\n實收總額：$" + total.toLocaleString()
  );
}

/** 列出今日排課 */
function showTodaySchedule() {
  const sheet = getSheet(["排課表"]);
  if (!sheet) return;
  const days = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
  const today = days[new Date().getDay()];
  const lastRow = sheet.getLastRow();
  const data = sheet.getRange(5, 1, lastRow - 4, 5).getValues();
  const lines = [];
  for (const row of data) {
    if (String(row[0]) === today) {
      lines.push(row[1] + "  " + row[2] + "  " + row[3] + "  " + row[4]);
    }
  }
  if (lines.length === 0) {
    SpreadsheetApp.getUi().alert("今日（" + today + "）無排課。");
  } else {
    SpreadsheetApp.getUi().alert("今日課表（" + today + "）：\n\n" + lines.join("\n"));
  }
}

/** 生成欠費學生繳費提醒文字（複製貼上至 WhatsApp） */
function generatePaymentReminders() {
  const sheet = getSheet(["學生資料庫"]);
  if (!sheet) return;
  const lastRow = sheet.getLastRow();
  const data = sheet.getRange(5, 1, lastRow - 4, 11).getValues();
  const msgs = [];
  for (const row of data) {
    if (String(row[7]) === "欠費") {
      const name = row[1];
      const course = row[4];
      const fee = row[6];
      const parent = row[8];
      msgs.push(
        "【俊才坊繳費提醒】\n" +
          parent + "您好，" + name + " 同學的 " + course +
          " 月費 $" + fee + " 尚未收到，請於本月內透過 FPS/PayMe 繳付。如有疑問請回覆此訊息。謝謝！"
      );
    }
  }
  if (msgs.length === 0) {
    SpreadsheetApp.getUi().alert("目前無欠費學生。");
  } else {
    SpreadsheetApp.getUi().alert("欠費提醒（共 " + msgs.length + " 則）：\n\n" + msgs.join("\n\n---\n\n"));
  }
}
