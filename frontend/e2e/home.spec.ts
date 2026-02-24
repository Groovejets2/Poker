import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should load the home page', async ({ page }) => {
    await page.goto('/');

    // Check title and main heading
    await expect(page).toHaveTitle(/OpenClaw Poker/i);
    await expect(page.locator('h1')).toContainText('Welcome to OpenClaw Poker');
  });

  test('should display feature cards', async ({ page }) => {
    await page.goto('/');

    // Check for three main feature cards
    await expect(page.getByText('🏆 Tournaments')).toBeVisible();
    await expect(page.getByText('📊 Leaderboard')).toBeVisible();
    await expect(page.getByText('👤 Your Stats')).toBeVisible();
  });

  test('should show login/register buttons for guests', async ({ page }) => {
    await page.goto('/');

    // Navigation should show Login and Register buttons
    await expect(page.getByRole('link', { name: /login/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /register/i })).toBeVisible();
  });

  test('should navigate to tournaments page', async ({ page }) => {
    await page.goto('/');

    // Click on View Tournaments button
    await page.getByRole('link', { name: /view tournaments/i }).first().click();

    // Should navigate to tournaments page
    await expect(page).toHaveURL(/\/tournaments/);
  });

  test('should navigate to leaderboard page', async ({ page }) => {
    await page.goto('/');

    // Click on View Leaderboard button
    await page.getByRole('link', { name: /view leaderboard/i }).first().click();

    // Should navigate to leaderboard page
    await expect(page).toHaveURL(/\/leaderboard/);
  });

  test('should show create account CTA for guests', async ({ page }) => {
    await page.goto('/');

    // Should show call-to-action section
    await expect(page.getByText(/Ready to get started/i)).toBeVisible();
    await expect(page.getByRole('link', { name: /create account/i })).toBeVisible();
  });
});
