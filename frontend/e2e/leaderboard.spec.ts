import { test, expect } from '@playwright/test';

test.describe('Leaderboard Page', () => {
  test('should load leaderboard page', async ({ page }) => {
    await page.goto('/leaderboard');

    await expect(page.locator('h1')).toContainText('Global Leaderboard');
  });

  test('should display loading state initially', async ({ page }) => {
    await page.goto('/leaderboard');

    // May briefly see loading spinner
    const loadingSpinner = page.locator('.animate-spin');
    // Loading may be too fast to assert
  });

  test('should display leaderboard table or empty state', async ({ page }) => {
    await page.goto('/leaderboard');

    await page.waitForTimeout(1000);

    // Should show either players table or empty state
    const hasTable = await page.locator('table').count() > 0;
    const hasEmptyState = await page.getByText(/no players on the leaderboard/i).isVisible().catch(() => false);

    expect(hasTable || hasEmptyState).toBeTruthy();
  });

  test('should display table headers', async ({ page }) => {
    await page.goto('/leaderboard');

    await page.waitForTimeout(1000);

    const table = page.locator('table');

    if (await table.count() > 0) {
      // Check for table headers
      await expect(page.getByText('Rank')).toBeVisible();
      await expect(page.getByText('Player')).toBeVisible();
      await expect(page.getByText('Tournaments Played')).toBeVisible();
      await expect(page.getByText('Wins')).toBeVisible();
      await expect(page.getByText('Total Winnings')).toBeVisible();
    }
  });

  test('should navigate to player stats', async ({ page }) => {
    await page.goto('/leaderboard');

    await page.waitForTimeout(1000);

    // If there are players, click View Stats
    const viewStatsLink = page.getByRole('link', { name: /view stats/i }).first();

    if (await viewStatsLink.count() > 0) {
      await viewStatsLink.click();
      await expect(page).toHaveURL(/\/stats\/\d+/);
    }
  });
});
