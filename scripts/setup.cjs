/**
 * Create .venv, install backend/requirements.txt, then npm install.
 */
const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const root = path.join(__dirname, '..');

function run(cmd, args, opts = {}) {
  const result = spawnSync(cmd, args, {
    cwd: root,
    stdio: 'inherit',
    shell: process.platform === 'win32',
    ...opts,
  });
  if (result.error) throw result.error;
  if (result.status !== 0 && result.status !== null) {
    process.exit(result.status);
  }
}

const venvDir = path.join(root, '.venv');
if (!fs.existsSync(venvDir)) {
  run('python', ['-m', 'venv', '.venv']);
}

const pyExe =
  process.platform === 'win32'
    ? path.join(venvDir, 'Scripts', 'python.exe')
    : path.join(venvDir, 'bin', 'python');

run(pyExe, ['-m', 'pip', 'install', '--upgrade', 'pip']);
run(pyExe, ['-m', 'pip', 'install', '-r', 'backend/requirements.txt']);

run('npm', ['install']);
