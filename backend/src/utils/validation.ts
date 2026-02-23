/**
 * Input Validation Utilities
 * Provides validation functions for user input across the application
 */

/**
 * Validates username format
 * @param val - Username to validate
 * @returns true if valid (3-32 chars, alphanumeric + underscore only)
 */
export const username = (val: any): boolean => {
  if (!val || typeof val !== 'string') return false;
  return val.length >= 3 && val.length <= 32 && /^[a-zA-Z0-9_]+$/.test(val);
};

/**
 * Validates email format
 * @param val - Email address to validate
 * @returns true if valid email format
 */
export const email = (val: any): boolean => {
  if (!val || typeof val !== 'string') return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
};

/**
 * Validates password strength
 * @param val - Password to validate
 * @returns true if password is at least 6 characters
 */
export const password = (val: any): boolean => {
  if (!val || typeof val !== 'string') return false;
  return val.length >= 6;
};

/**
 * Validates tournament name format
 * @param val - Tournament name to validate
 * @returns true if valid (3-128 chars)
 */
export const tournamentName = (val: any): boolean => {
  if (!val || typeof val !== 'string') return false;
  return val.length >= 3 && val.length <= 128;
};

/**
 * Validates buy-in chip amount
 * @param val - Buy-in amount to validate
 * @returns true if positive integer
 */
export const buyInChips = (val: any): boolean => {
  return Number.isInteger(val) && val > 0;
};

/**
 * Validates entry fee amount
 * @param val - Entry fee to validate (in USD)
 * @returns true if non-negative number
 */
export const entryFee = (val: any): boolean => {
  return typeof val === 'number' && val >= 0;
};

/**
 * Validates maximum player count
 * @param val - Max players to validate
 * @returns true if integer between 2 and 8
 */
export const maxPlayers = (val: any): boolean => {
  return Number.isInteger(val) && val >= 2 && val <= 8;
};

/**
 * Validates future date
 * @param val - Date to validate
 * @returns true if valid date in the future
 */
export const futureDate = (val: any): boolean => {
  const date = new Date(val);
  return !isNaN(date.getTime()) && date > new Date();
};

/**
 * Validates stack size
 * @param val - Stack size to validate
 * @returns true if non-negative integer
 */
export const stack = (val: any): boolean => {
  return Number.isInteger(val) && val >= 0;
};
