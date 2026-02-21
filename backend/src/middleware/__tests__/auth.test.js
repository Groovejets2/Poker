/**
 * Auth Middleware Tests
 */

const jwt = require('jsonwebtoken');
const authMiddleware = require('../auth');

describe('Auth Middleware', () => {
  let req, res, next;

  beforeEach(() => {
    req = { headers: {} };
    res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };
    next = jest.fn();
  });

  test('should return 401 if no token provided', () => {
    authMiddleware(req, res, next);

    expect(res.status).toHaveBeenCalledWith(401);
    expect(res.json).toHaveBeenCalledWith(
      expect.objectContaining({
        error: expect.objectContaining({
          code: 'UNAUTHORIZED',
          message: 'Missing authentication token'
        })
      })
    );
    expect(next).not.toHaveBeenCalled();
  });

  test('should return 401 if token invalid', () => {
    req.headers.authorization = 'Bearer invalid_token';

    authMiddleware(req, res, next);

    expect(res.status).toHaveBeenCalledWith(401);
    expect(res.json).toHaveBeenCalledWith(
      expect.objectContaining({
        error: expect.objectContaining({
          code: 'UNAUTHORIZED'
        })
      })
    );
  });

  test('should return 401 if token expired', () => {
    const expiredToken = jwt.sign(
      { user_id: 1, username: 'player1' },
      'dev-secret-key',
      { expiresIn: '-1h' }
    );

    req.headers.authorization = `Bearer ${expiredToken}`;

    authMiddleware(req, res, next);

    expect(res.status).toHaveBeenCalledWith(401);
  });

  test('should pass token to req.user on valid token', () => {
    const token = jwt.sign(
      { user_id: 1, username: 'player1' },
      'dev-secret-key',
      { expiresIn: '1h' }
    );

    req.headers.authorization = `Bearer ${token}`;

    authMiddleware(req, res, next);

    expect(next).toHaveBeenCalled();
    expect(req.user).toBeDefined();
    expect(req.user.user_id).toBe(1);
    expect(req.user.username).toBe('player1');
  });

  test('should extract token from Bearer prefix', () => {
    const token = jwt.sign(
      { user_id: 2, username: 'player2' },
      'dev-secret-key'
    );

    req.headers.authorization = `Bearer ${token}`;

    authMiddleware(req, res, next);

    expect(req.user.user_id).toBe(2);
    expect(next).toHaveBeenCalled();
  });
});
