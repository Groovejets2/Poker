module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/server.js'
  ],
  testMatch: ['**/__tests__/**/*.js', '**/?(*.)+(spec|test).js'],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 75,
      lines: 75,
      statements: 75
    }
  }
};
