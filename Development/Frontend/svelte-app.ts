// App.svelte (Main Component)
export const AppComponent = `
<script lang="ts">
  import { Router, Route } from 'svelte-routing';
  import Home from './routes/Home.svelte';
  import About from './routes/About.svelte';
  import Dashboard from './routes/Dashboard.svelte';
</script>

<Router>
  <nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
    <a href="/dashboard">Dashboard</a>
  </nav>

  <main>
    <Route path="/" component={Home} />
    <Route path="/about" component={About} />
    <Route path="/dashboard" component={Dashboard} />
  </main>
</Router>

<style>
  nav {
    padding: 1rem;
    background: #333;
  }
  nav a {
    color: white;
    margin: 0 1rem;
    text-decoration: none;
  }
</style>
`;

// Home.svelte
export const HomeComponent = `
<script lang="ts">
  let message = 'Modern Svelte Application';
</script>

<div class="home">
  <h1>Welcome to Svelte</h1>
  <p>{message}</p>
</div>
`;

// Dashboard.svelte
export const DashboardComponent = `
<script lang="ts">
  import { writable } from 'svelte/store';
  
  let count = writable(0);
  
  function increment() {
    count.update(n => n + 1);
  }
</script>

<div class="dashboard">
  <h1>Dashboard</h1>
  <p>Count: {$count}</p>
  <button on:click={increment}>Increment</button>
</div>
`;

// Store
export const counterStore = `
import { writable } from 'svelte/store';

export const count = writable(0);

export function increment() {
  count.update(n => n + 1);
}

export function decrement() {
  count.update(n => n - 1);
}

export function reset() {
  count.set(0);
}
`;

// main.ts
import App from './App.svelte';

const app = new App({
  target: document.getElementById('app')!,
});

export default app;
