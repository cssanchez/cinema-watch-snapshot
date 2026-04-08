const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Try to load local server, expecting files in docs/
  try {
    await page.goto('http://localhost:8000/docs/', { waitUntil: 'networkidle' });
    console.log('Successfully navigated to http://localhost:8000/docs/');
  } catch (error) {
    console.error('Failed to navigate:', error);
    process.exit(1);
  }

  // Find a button with data-location-target and click it
  try {
      const button = await page.locator('[data-location-target]').first();
      const target = await button.getAttribute('data-location-target');
      console.log('Found button targeting:', target);
      await button.click();

      const panel = page.locator(`[data-location-panel="${target}"]`);
      const isHidden = await panel.isHidden();
      if (!isHidden) {
          console.log('Panel is successfully shown after click.');
      } else {
          console.error('Panel is still hidden after click.');
          process.exit(1);
      }

      await page.screenshot({ path: 'screenshot.png' });
  } catch(error) {
      console.log('No buttons found or click failed:', error);
  }

  await browser.close();
})();
