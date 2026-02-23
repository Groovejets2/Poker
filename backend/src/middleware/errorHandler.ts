import { Request, Response, NextFunction } from 'express';

/**
 * Custom error interface extending Error
 */
interface CustomError extends Error {
  statusCode?: number;
  code?: string;
}

/**
 * Global Error Handler Middleware
 * Catches all errors and returns standardised JSON responses
 */
const errorHandler = (
  err: CustomError,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  console.error('Error:', err);

  const statusCode = err.statusCode || 500;
  const errorCode = err.code || 'INTERNAL_ERROR';
  const message = err.message || 'Internal server error';

  res.status(statusCode).json({
    error: {
      code: errorCode,
      message: message,
      ...(process.env.NODE_ENV === 'development' && { details: err.stack })
    }
  });
};

export default errorHandler;
