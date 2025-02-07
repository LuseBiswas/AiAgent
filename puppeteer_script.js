#!/usr/bin/env node
import puppeteer from 'puppeteer';

async function executeTask(subtasks) {
  console.log('🚀 Starting Persistent Puppeteer Automation',subtasks);
  
  const browser = await puppeteer.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();

  try {
    let finalResult = {};

    for (const subtask of subtasks) {
      console.log('Current Subtask:', JSON.stringify(subtask));

      switch (subtask.action) {
        case 'navigate':
          console.log(`🌐 Navigating to URL: ${subtask.url}`);
          await page.goto(subtask.url, { waitUntil: 'networkidle2' });
          finalResult = { status: 'navigated', url: subtask.url };
          break;

        case 'extract':
          console.log(`🔍 Extracting data with selector: ${subtask.selectors}`);
          await page.waitForSelector(subtask.selectors);
          const data = await page.evaluate(selector => {
            const elements = document.querySelectorAll(selector);
            return Array.from(elements).map(el => el.textContent.trim());
          }, subtask.selectors);
          console.log(`📊 Extracted ${data.length} items`);
          finalResult = { status: 'extracted', data, type: subtask.data_to_extract };
          break;

        case 'limit':
          const limit = parseInt(subtask.data_to_extract);
          console.log(`✂️ Limiting results to ${limit} items`);
          finalResult.data = finalResult.data.slice(0, limit);
          break;
      }
    }

    await browser.close();
    return finalResult;
  } catch (error) {
    console.error('❌ Task Execution Error:', error);
    await browser.close();
    throw error;
  }
}

(async () => {
  try {
    const subtasks = JSON.parse(process.argv[2]);
    const result = await executeTask(subtasks);
    console.log('🏁 Final Result:', JSON.stringify(result, null, 2));
    console.log(JSON.stringify(result));
  } catch (error) {
    console.error('💥 Script Execution Failed:', error);
    process.exit(1);
  }
})();