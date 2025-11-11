type Listener = () => void;

class StateManager<T> {
  private state: T;
  private listeners: Set<Listener> = new Set();

  constructor(initialState: T) {
    this.state = initialState;
  }

  getState(): T {
    return this.state;
  }

  setState(newState: Partial<T>): void {
    this.state = { ...this.state, ...newState };
    this.notify();
  }

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private notify(): void {
    this.listeners.forEach(listener => listener());
  }
}

// Example store
interface AppState {
  user: { name: string; email: string } | null;
  theme: 'light' | 'dark';
  notifications: string[];
}

const appStore = new StateManager<AppState>({
  user: null,
  theme: 'light',
  notifications: [],
});

export { StateManager, appStore };
