/**
 * 俊才坊行政系統 v2 · Google Sheets 自動化
 * Extensions → Apps Script → 貼上 → 儲存 → 重新載入
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("俊才坊行政")
    .addItem("📊 顯示儀表板摘要", "showDashboardSummary")
    .addSeparator()
    .addItem("標記欠費學生", "highlightOverdue")
    .addItem("統計本月營收", "summarizeMonthlyRevenue")
    .addItem("列出今日課表", "showTodaySchedule")
    .addItem("生成繳費提醒", "generatePaymentReminders")
    .addSeparator()
    .addItem("生成學習進度訊息", "copyProgressMessages")
    .addItem("標記逾期家長通訊", "highlightOverdueComms")
    .addItem("標記導師合約即將到期", "highlightTutorContracts")
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

const DATA_ROW = 6; // header at row 5

function showDashboardSummary() {
  const students = getSheet(["學生資料庫"]);
  const fees = getSheet(["收費記錄"]);
  const parents = getSheet(["家長通訊"]);
  if (!students || !fees || !parents) return;

  const month = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM");
  const lastRow = students.getLastRow();
  const active = countValues(students, 18, DATA_ROW, lastRow, "在讀"); // R欄 學生狀態
  const overdue = countValues(students, 10, DATA_ROW, lastRow, "欠費"); // J欄 付款狀態

  const feeLast = fees.getLastRow();
  let revenue = 0;
  if (feeLast >= DATA_ROW) {
    const months = fees.getRange(DATA_ROW, 5, feeLast - DATA_ROW + 1, 1).getValues();
    const amounts = fees.getRange(DATA_ROW, 8, feeLast - DATA_ROW + 1, 1).getValues();
    for (let i = 0; i < months.length; i++) {
      if (String(months[i][0]).indexOf(month) === 0) revenue += Number(amounts[i][0]) || 0;
    }
  }

  const pending = countValues(parents, 8, DATA_ROW, parents.getLastRow(), "跟進中")
    + countValues(parents, 8, DATA_ROW, parents.getLastRow(), "待處理");

  SpreadsheetApp.getUi().alert(
    "俊才坊營運摘要\n\n" +
    "在讀學生：" + active + " 人\n" +
    "欠費學生：" + overdue + " 人\n" +
    "本月實收：$" + revenue.toLocaleString() + "\n" +
    "待跟進通訊：" + pending + " 則"
  );
}

function countValues(sheet, col, startRow, lastRow, target) {
  if (lastRow < startRow) return 0;
  const data = sheet.getRange(startRow, col, lastRow - startRow + 1, 1).getValues();
  return data.filter((r) => String(r[0]) === target).length;
}

function highlightOverdue() {
  const sheet = getSheet(["學生資料庫"]);
  if (!sheet) return;
  const lastRow = sheet.getLastRow();
  if (lastRow < DATA_ROW) return;
  const cols = sheet.getLastColumn();
  sheet.getRange(DATA_ROW, 1, lastRow - DATA_ROW + 1, cols).setBackground(null);
  const data = sheet.getRange(DATA_ROW, 10, lastRow - DATA_ROW + 1, 1).getValues();
  let count = 0;
  for (let i = 0; i < data.length; i++) {
    if (String(data[i][0]) === "欠費" || String(data[i][0]) === "部分") {
      sheet.getRange(i + DATA_ROW, 1, 1, cols).setBackground("#FEE2E2");
      count++;
    }
  }
  SpreadsheetApp.getUi().alert("已標記 " + count + " 名欠費/部分付款學生。");
}

function summarizeMonthlyRevenue() {
  const sheet = getSheet(["收費記錄"]);
  if (!sheet) return;
  const lastRow = sheet.getLastRow();
  if (lastRow < DATA_ROW) return;
  const month = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM");
  const months = sheet.getRange(DATA_ROW, 5, lastRow - DATA_ROW + 1, 1).getValues();
  const due = sheet.getRange(DATA_ROW, 7, lastRow - DATA_ROW + 1, 1).getValues();
  const paid = sheet.getRange(DATA_ROW, 8, lastRow - DATA_ROW + 1, 1).getValues();
  let totalPaid = 0, totalDue = 0, count = 0;
  for (let i = 0; i < months.length; i++) {
    if (String(months[i][0]).indexOf(month) === 0) {
      totalDue += Number(due[i][0]) || 0;
      totalPaid += Number(paid[i][0]) || 0;
      count++;
    }
  }
  SpreadsheetApp.getUi().alert(
    "本月（" + month + "）\n" +
    "收款筆數：" + count + "\n" +
    "應收合計：$" + totalDue.toLocaleString() + "\n" +
    "實收合計：$" + totalPaid.toLocaleString() + "\n" +
    "未收合計：$" + (totalDue - totalPaid).toLocaleString()
  );
}

function showTodaySchedule() {
  const sheet = getSheet(["排課表"]);
  if (!sheet) return;
  const days = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
  const today = days[new Date().getDay()];
  const lastRow = sheet.getLastRow();
  const data = sheet.getRange(DATA_ROW, 1, lastRow - DATA_ROW + 1, 5).getValues();
  const lines = [];
  for (const row of data) {
    if (String(row[0]) === today) {
      lines.push(row[1] + "  " + row[2] + "  " + row[4] + "  " + row[3]);
    }
  }
  SpreadsheetApp.getUi().alert(
    lines.length ? "今日課表（" + today + "）：\n\n" + lines.join("\n") : "今日（" + today + "）無排課。"
  );
}

function generatePaymentReminders() {
  const sheet = getSheet(["學生資料庫"]);
  if (!sheet) return;
  const lastRow = sheet.getLastRow();
  const data = sheet.getRange(DATA_ROW, 1, lastRow - DATA_ROW + 1, 13).getValues();
  const msgs = [];
  for (const row of data) {
    if (String(row[9]) === "欠費" || String(row[9]) === "部分") {
      const fee = row[8];
      const owed = row[10] || fee;
      msgs.push(
        "【俊才坊繳費提醒】\n" + row[11] + "您好，" + row[1] + " 同學的 " + row[5] +
        " 尚有 $" + owed + " 未繳，請於本月內透過 FPS/PayMe 繳付。謝謝！"
      );
    }
  }
  SpreadsheetApp.getUi().alert(
    msgs.length ? "欠費提醒（" + msgs.length + " 則）：\n\n" + msgs.join("\n\n---\n\n") : "目前無欠費學生。"
  );
}

function copyProgressMessages() {
  const sheet = getSheet(["學習進度"]);
  if (!sheet) return;
  const lastRow = sheet.getLastRow();
  const data = sheet.getRange(DATA_ROW, 14, lastRow - DATA_ROW + 1, 1).getValues();
  const sent = sheet.getRange(DATA_ROW, 14, lastRow - DATA_ROW + 1, 1).getValues();
  const msgs = [];
  for (let i = 0; i < data.length; i++) {
    if (String(sent[i][0]) === "✗" && data[i][0]) msgs.push(data[i][0]);
  }
  SpreadsheetApp.getUi().alert(
    msgs.length ? "待發送進度訊息（" + msgs.length + " 則）：\n\n" + msgs.join("\n\n---\n\n") : "所有進度報告已發送。"
  );
}

function highlightOverdueComms() {
  const sheet = getSheet(["家長通訊"]);
  if (!sheet) return;
  const lastRow = sheet.getLastRow();
  const cols = sheet.getLastColumn();
  sheet.getRange(DATA_ROW, 1, lastRow - DATA_ROW + 1, cols).setBackground(null);
  const data = sheet.getRange(DATA_ROW, 11, lastRow - DATA_ROW + 1, 1).getValues();
  let count = 0;
  for (let i = 0; i < data.length; i++) {
    if (String(data[i][0]) === "⚠️") {
      sheet.getRange(i + DATA_ROW, 1, 1, cols).setBackground("#FEE2E2");
      count++;
    }
  }
  SpreadsheetApp.getUi().alert("已標記 " + count + " 則逾期家長通訊。");
}

function highlightTutorContracts() {
  const sheet = getSheet(["導師資料"]);
  if (!sheet) return;
  const lastRow = sheet.getLastRow();
  const cols = sheet.getLastColumn();
  sheet.getRange(DATA_ROW, 1, lastRow - DATA_ROW + 1, cols).setBackground(null);
  const data = sheet.getRange(DATA_ROW, 11, lastRow - DATA_ROW + 1, 1).getValues();
  let count = 0;
  for (let i = 0; i < data.length; i++) {
    const days = Number(data[i][0]);
    if (!isNaN(days) && days <= 60) {
      sheet.getRange(i + DATA_ROW, 1, 1, cols).setBackground("#FEF3C7");
      count++;
    }
  }
  SpreadsheetApp.getUi().alert("已標記 " + count + " 名合約 60 天內到期的導師。");
}
