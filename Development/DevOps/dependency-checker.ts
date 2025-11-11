import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function checkDependencies() {
  console.log('🔍 Checking dependencies...');
  
  try {
    const { stdout } = await execAsync('npm outdated --json');
    const outdated = JSON.parse(stdout);
    
    for (const [pkg, info] of Object.entries(outdated)) {
      console.log(`📦 ${pkg}: ${info.current} → ${info.latest}`);
    }
  } catch (error) {
    console.log('✅ All dependencies up to date');
  }
}

checkDependencies();
