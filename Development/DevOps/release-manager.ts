import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs/promises';

const execAsync = promisify(exec);

async function createRelease(version: string) {
  console.log(`🚀 Creating release: v${version}`);
  
  // Update version
  await execAsync(`npm version ${version} --no-git-tag-version`);
  
  // Build
  await execAsync('npm run build');
  
  // Create git tag
  await execAsync(`git tag -a v${version} -m "Release v${version}"`);
  await execAsync('git push --tags');
  
  console.log('✅ Release created');
}

const version = process.argv[2] || 'patch';
createRelease(version);
