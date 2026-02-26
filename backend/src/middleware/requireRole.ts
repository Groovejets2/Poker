import { Request, Response, NextFunction } from 'express';

/**
 * CRIT-6 FIX: Role-Based Access Control Middleware
 *
 * Checks if the authenticated user has one of the required roles.
 * Must be used AFTER authMiddleware to ensure req.user is populated.
 *
 * @param allowedRoles - Array of roles that are permitted (e.g., ['admin', 'moderator'])
 * @returns Express middleware function
 *
 * @example
 * // Only admins can create tournaments
 * router.post('/tournaments', authMiddleware, requireRole(['admin']), createTournament);
 *
 * // Both admins and moderators can access
 * router.delete('/user/:id', authMiddleware, requireRole(['admin', 'moderator']), deleteUser);
 */
export const requireRole = (allowedRoles: string[]) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    // Get user role from JWT payload (set by authMiddleware)
    const userRole = req.user?.role;

    // Check if user has a role and it's in the allowed list
    if (!userRole || !allowedRoles.includes(userRole)) {
      res.status(403).json({
        error: {
          code: 'FORBIDDEN',
          message: 'Insufficient permissions for this operation',
          required_role: allowedRoles.length === 1 ? allowedRoles[0] : allowedRoles
        }
      });
      return;
    }

    // User has required role, proceed
    next();
  };
};

export default requireRole;
