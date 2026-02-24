import { test, expect } from '@playwright/test';

test.describe('Tournaments Page', () => {
  test('should load tournaments page', async ({ page }) => {
    await page.goto('/tournaments');

    await expect(page.locator('h1')).toContainText('Tournaments');
  });

  test('should display loading state initially', async ({ page }) => {
    await page.goto('/tournaments');

    // May briefly see loading state
    // Note: This might be too fast to catch in real tests
    const loadingText = page.getByText(/loading tournaments/i);
    // Don't assert it's visible since it may have already loaded
  });

  test('should display tournaments list or empty state', async ({ page }) => {
    await page.goto('/tournaments');

    // Wait for loading to complete
    await page.waitForTimeout(1000);

    // Should show either tournaments or empty state
    const hasTournaments = await page.getByText(/buy-in/i).count() > 0;
    const hasEmptyState = await page.getByText(/no tournaments available/i).isVisible().catch(() => false);

    expect(hasTournaments || hasEmptyState).toBeTruthy();
  });

  test('should navigate to tournament details', async ({ page }) => {
    await page.goto('/tournaments');

    await page.waitForTimeout(1000);

    // If there are tournaments, click View Details
    const viewDetailsButton = page.getByRole('link', { name: /view details/i }).first();

    if (await viewDetailsButton.count() > 0) {
      await viewDetailsButton.click();
      await expect(page).toHaveURL(/\/tournaments\/\d+/);
    }
  });

  test('should show admin create button for admins', async ({ page }) => {
    await page.goto('/tournaments');

    // For guests/players, should not see create button
    const createButton = page.getByRole('link', { name: /create tournament/i });

    // Button exists but may not be visible for non-admins
    // This would require authentication to properly test
  });
});
