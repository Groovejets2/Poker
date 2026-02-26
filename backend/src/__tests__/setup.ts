/**
 * Jest Test Setup
 * Sets environment variables before tests run
 * CRIT-1: Set JWT_SECRET to prevent fatal error during test module loading
 */

process.env.JWT_SECRET = 'test-secret-key-for-unit-tests-only';
process.env.NODE_ENV = 'test';
