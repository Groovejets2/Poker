import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('should load login page', async ({ page }) => {
    await page.goto('/login');

    await expect(page.locator('h2')).toContainText('Login to your account');
  });

  test('should display login form fields', async ({ page }) => {
    await page.goto('/login');

    // Check form fields exist
    await expect(page.getByLabel(/username/i)).toBeVisible();
    await expect(page.getByLabel(/password/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /login/i })).toBeVisible();
  });

  test('should have link to registration', async ({ page }) => {
    await page.goto('/login');

    await expect(page.getByRole('link', { name: /register here/i })).toBeVisible();
  });

  test('should load registration page', async ({ page }) => {
    await page.goto('/register');

    await expect(page.locator('h2')).toContainText('Create your account');
  });

  test('should display registration form fields', async ({ page }) => {
    await page.goto('/register');

    // Check form fields exist
    await expect(page.getByLabel(/username/i)).toBeVisible();
    await expect(page.getByLabel(/email/i)).toBeVisible();
    await expect(page.getByLabel(/^password$/i)).toBeVisible();
    await expect(page.getByLabel(/confirm password/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /register/i })).toBeVisible();
  });

  test('should navigate between login and register', async ({ page }) => {
    await page.goto('/login');

    // Click Register link
    await page.getByRole('link', { name: /register here/i }).click();

    await expect(page).toHaveURL(/\/register/);
    await expect(page.locator('h2')).toContainText('Create your account');

    // Click Login link
    await page.getByRole('link', { name: /login here/i }).click();

    await expect(page).toHaveURL(/\/login/);
    await expect(page.locator('h2')).toContainText('Login to your account');
  });

  test('should show validation for empty form submission', async ({ page }) => {
    await page.goto('/login');

    // Try to submit empty form
    await page.getByRole('button', { name: /login/i }).click();

    // HTML5 validation should prevent submission
    // Check that we're still on login page
    await expect(page).toHaveURL(/\/login/);
  });
});
