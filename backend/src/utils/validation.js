/**
 * Input Validation Utilities
 */

const validators = {
  username: (val) => {
    if (!val || typeof val !== 'string') return false;
    return val.length >= 3 && val.length <= 32 && /^[a-zA-Z0-9_]+$/.test(val);
  },

  email: (val) => {
    if (!val || typeof val !== 'string') return false;
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
  },

  password: (val) => {
    if (!val || typeof val !== 'string') return false;
    return val.length >= 6;
  },

  tournamentName: (val) => {
    if (!val || typeof val !== 'string') return false;
    return val.length >= 3 && val.length <= 128;
  },

  buyInChips: (val) => {
    return Number.isInteger(val) && val > 0;
  },

  entryFee: (val) => {
    return typeof val === 'number' && val >= 0;
  },

  maxPlayers: (val) => {
    return Number.isInteger(val) && val >= 2 && val <= 8;
  },

  futureDate: (val) => {
    const date = new Date(val);
    return !isNaN(date.getTime()) && date > new Date();
  },

  stack: (val) => {
    return Number.isInteger(val) && val >= 0;
  }
};

module.exports = validators;
