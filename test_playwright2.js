const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  try {
    await page.goto('http://localhost:8000/docs/', { waitUntil: 'networkidle' });
    console.log('Successfully navigated to http://localhost:8000/docs/');
  } catch (error) {
    console.error('Failed to navigate:', error);
    process.exit(1);
  }

  try {
      // First, find and click the dropdown toggle to make buttons visible
      const toggle = await page.locator('[data-location-dropdown-toggle]');
      await toggle.click();

      // Now click a button
      const button = await page.locator('[data-location-target]').nth(1); // Click second one
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
  } catch(error) {
      console.log('Test failed:', error);
      process.exit(1);
  }

  await browser.close();
})();
