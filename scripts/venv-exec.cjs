/**
 * Run the repo's .venv Python with the given args (cross-platform).
 * Usage: node scripts/venv-exec.cjs backend/app.py
 *        node scripts/venv-exec.cjs -m pytest backend/tests
 */
const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const root = path.join(__dirname, '..');
const python =
  process.platform === 'win32'
    ? path.join(root, '.venv', 'Scripts', 'python.exe')
    : path.join(root, '.venv', 'bin', 'python');

if (!fs.existsSync(python)) {
  console.error('Missing .venv Python. Run: npm run setup');
  process.exit(1);
}

const result = spawnSync(python, process.argv.slice(2), {
  cwd: root,
  stdio: 'inherit',
});
process.exit(result.status ?? 1);
