# tuff ash challenge

## Description

A lexander is a master at hiding his secrets! Oh... nevermind. Well at least you can't find his favorite one of them all! At least... not E veryone can...

https://docs.google.com/spreadsheets/d/1rivkwPvDg_qCnFHfgLdLlKXPEgZpzNPflt7BaGP9Nd8/edit?usp=sharing

NOTE: (Only 5 guesses be careful!)

## Solution Walkthrough

Opening the spreadsheet, you can see there are two sheets: `Money stuff to rule the world I guess` and `hidden xander secrets`. The latter is hidden, so you need to create a copy to view it.

When creating the copy, you can see it has an app script with the following content:

![alt text](image.png)

```js
function fillDecoyFlags() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("hidden xander secrets");
  
  // Failsafe: Ensures it ONLY runs on the specific sheet
  if (!sheet) {
    SpreadsheetApp.getUi().alert("Error: 'hidden xander secrets' sheet not found!");
    return;
  }

  // Set the size of your haystack grid (100 rows by 26 columns = 2,600 cells)
  var numRows = 100;
  var numCols = 26;
  var range = sheet.getRange(1, 1, numRows, numCols);

  // A pool of "weird" random characters (Greek, Spanish, Math, etc.)
  var weirdChars = "ÆØÅΩΣΨΔΘΞΦΣΠЛЖЦЧШЩЪЫЬЭЮЯñ¿¡©®™✓✗∞≈≠≤≥∑∫∂√";
  var values = [];

  // Generate the fake flags
  for (var r = 0; r < numRows; r++) {
    var row = [];
    for (var c = 0; c < numCols; c++) {
      // Pick a random length between 1 and 3 characters for the inside of the flag
      var flagLen = Math.floor(Math.random() * 3) + 1;
      var randomText = "";
      
      for (var i = 0; i < flagLen; i++) {
        var randIndex = Math.floor(Math.random() * weirdChars.length);
        randomText += weirdChars.charAt(randIndex);
      }
      
      row.push("cyber{" + randomText + "}");
    }
    values.push(row);
  }

  // Push all the generated flags to the sheet at once (much faster than cell-by-cell)
  range.setValues(values);
}
```

No clues can be found in this script, and the `hidden xander secrets` sheet contains only fake flags.

![alt text](image-1.png)

After trying for a long time, I discovered something strange in the challenge description. Looking at `A lexander` and `E veryone`, the prefixes are `A` and `E`, which combine to form `AE`. The `wierdChars` in the code above happens to include `Æ`.

After looking up this symbol, I found that its pronunciation is "ash," and the challenge title is `tuff ash challenge`. I then confirmed that the flag is `boroCTF{Æ}`.

## Flag

```text
boroCTF{Æ}
```
