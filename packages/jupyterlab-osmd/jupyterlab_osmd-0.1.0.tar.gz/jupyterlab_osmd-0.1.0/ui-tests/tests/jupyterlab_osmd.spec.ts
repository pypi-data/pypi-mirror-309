import { expect, test } from '@jupyterlab/galata';

test('should display musicxml data file', async ({ page }) => {
  const filename = 'test.musicxml';
  await page.menu.clickMenuItem('File>New>Text File');

  // Set MIME type content in fill
  await page.getByRole('main').getByRole('textbox').fill('');

  await page.menu.clickMenuItem('File>Save Text');

  await page.locator('.jp-Dialog').getByRole('textbox').fill(filename);

  await page.getByRole('button', { name: 'Rename' }).click();
  await page.waitForTimeout(200);

  // Close file opened as editor
  await page.activity.closePanel('test.my_type');

  await page.filebrowser.open(filename);

  const view = page.getByRole('main').locator('.mimerenderer-musicxml');

  expect(await view.screenshot()).toMatchSnapshot('musicxml-file.png');
});

test('should display notebook musicxml output', async ({ page }) => {
  await page.menu.clickMenuItem('File>New>Notebook');

  await page.getByRole('button', { name: 'Select' }).click();

  await page.notebook.setCell(
    0,
    'code',
    `from IPython.display import display
# Example of MIME type content
output = {
    "application/vnd.recordare.musicxml": ""
}

display(output, raw=True)`
  );

  await page.notebook.run();

  const outputs = page
    .getByRole('main')
    .locator('.mimerenderer-musicxml.jp-OutputArea-output');

  await expect(outputs).toHaveCount(1);
});
