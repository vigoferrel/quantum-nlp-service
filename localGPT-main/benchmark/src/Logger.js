// Basic color logging to avoid external dependencies like chalk
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m',
};

const print = (color, message) => console.log(`${color}%s${colors.reset}`, message);

const Logger = {
  header: (message) => {
    console.log(colors.magenta, '='.repeat(80));
    console.log(colors.magenta, message);
    console.log(colors.magenta, '='.repeat(80), colors.reset);
  },
  info: (message) => print(colors.cyan, message),
  success: (message) => print(colors.green, `  ✅ ${message}`),
  error: (message) => print(colors.red, `  ❌ ${message}`),
  warn: (message) => print(colors.yellow, `  ⚠️ ${message}`),
  result: (message) => console.log(colors.yellow, `   ⚛️  ${message}`),
};

module.exports = Logger;
