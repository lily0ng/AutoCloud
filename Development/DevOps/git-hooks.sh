#!/bin/bash
# Git Hooks Setup

# Pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
npm run lint
npm run type-check
npm run test
EOF

chmod +x .git/hooks/pre-commit

echo "✅ Git hooks installed"
