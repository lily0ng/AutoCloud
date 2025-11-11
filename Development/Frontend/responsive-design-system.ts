// Responsive Design System

interface Breakpoint {
  name: string;
  minWidth: number;
  maxWidth?: number;
}

interface SpacingScale {
  xs: string;
  sm: string;
  md: string;
  lg: string;
  xl: string;
  '2xl': string;
}

interface ColorPalette {
  primary: Record<number, string>;
  secondary: Record<number, string>;
  neutral: Record<number, string>;
  success: Record<number, string>;
  warning: Record<number, string>;
  error: Record<number, string>;
}

class DesignSystem {
  private breakpoints: Breakpoint[] = [
    { name: 'mobile', minWidth: 0, maxWidth: 639 },
    { name: 'tablet', minWidth: 640, maxWidth: 1023 },
    { name: 'desktop', minWidth: 1024, maxWidth: 1279 },
    { name: 'wide', minWidth: 1280 },
  ];

  private spacing: SpacingScale = {
    xs: '0.25rem',   // 4px
    sm: '0.5rem',    // 8px
    md: '1rem',      // 16px
    lg: '1.5rem',    // 24px
    xl: '2rem',      // 32px
    '2xl': '3rem',   // 48px
  };

  private colors: ColorPalette = {
    primary: {
      50: '#eff6ff',
      100: '#dbeafe',
      200: '#bfdbfe',
      300: '#93c5fd',
      400: '#60a5fa',
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
      800: '#1e40af',
      900: '#1e3a8a',
    },
    secondary: {
      50: '#f8fafc',
      500: '#64748b',
      900: '#0f172a',
    },
    neutral: {
      50: '#fafafa',
      500: '#737373',
      900: '#171717',
    },
    success: {
      500: '#22c55e',
      700: '#15803d',
    },
    warning: {
      500: '#f59e0b',
      700: '#b45309',
    },
    error: {
      500: '#ef4444',
      700: '#b91c1c',
    },
  };

  getBreakpoint(width: number): string {
    for (const bp of this.breakpoints) {
      if (width >= bp.minWidth && (!bp.maxWidth || width <= bp.maxWidth)) {
        return bp.name;
      }
    }
    return 'mobile';
  }

  getMediaQuery(breakpoint: string): string {
    const bp = this.breakpoints.find(b => b.name === breakpoint);
    if (!bp) return '';
    
    if (bp.maxWidth) {
      return `@media (min-width: ${bp.minWidth}px) and (max-width: ${bp.maxWidth}px)`;
    }
    return `@media (min-width: ${bp.minWidth}px)`;
  }

  getSpacing(size: keyof SpacingScale): string {
    return this.spacing[size];
  }

  getColor(palette: keyof ColorPalette, shade: number = 500): string {
    return this.colors[palette][shade] || this.colors[palette][500];
  }

  generateCSS(): string {
    let css = ':root {\n';
    
    // Add spacing variables
    Object.entries(this.spacing).forEach(([key, value]) => {
      css += `  --spacing-${key}: ${value};\n`;
    });
    
    // Add color variables
    Object.entries(this.colors).forEach(([palette, shades]) => {
      Object.entries(shades).forEach(([shade, color]) => {
        css += `  --color-${palette}-${shade}: ${color};\n`;
      });
    });
    
    css += '}\n';
    return css;
  }

  generateUtilityClasses(): string {
    let css = '';
    
    // Spacing utilities
    Object.entries(this.spacing).forEach(([key, value]) => {
      css += `.p-${key} { padding: ${value}; }\n`;
      css += `.m-${key} { margin: ${value}; }\n`;
    });
    
    // Color utilities
    Object.entries(this.colors).forEach(([palette, shades]) => {
      Object.entries(shades).forEach(([shade, color]) => {
        css += `.text-${palette}-${shade} { color: ${color}; }\n`;
        css += `.bg-${palette}-${shade} { background-color: ${color}; }\n`;
      });
    });
    
    return css;
  }
}

// Example usage
const designSystem = new DesignSystem();

console.log('🎨 Design System Initialized\n');

console.log('📐 Breakpoints:');
console.log('  Mobile:', designSystem.getMediaQuery('mobile'));
console.log('  Tablet:', designSystem.getMediaQuery('tablet'));
console.log('  Desktop:', designSystem.getMediaQuery('desktop'));

console.log('\n📏 Spacing:');
console.log('  Small:', designSystem.getSpacing('sm'));
console.log('  Medium:', designSystem.getSpacing('md'));
console.log('  Large:', designSystem.getSpacing('lg'));

console.log('\n🎨 Colors:');
console.log('  Primary:', designSystem.getColor('primary', 500));
console.log('  Success:', designSystem.getColor('success', 500));
console.log('  Error:', designSystem.getColor('error', 500));

console.log('\n📝 CSS Variables Generated:');
console.log(designSystem.generateCSS().substring(0, 200) + '...');

console.log('\n✅ Design system ready!');

export default DesignSystem;
