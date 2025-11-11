import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createPinia } from 'pinia';

// Main App Component
const App = {
  template: `
    <div id="app">
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/about">About</router-link>
        <router-link to="/dashboard">Dashboard</router-link>
      </nav>
      <router-view />
    </div>
  `,
};

// Components
const Home = {
  template: `
    <div class="home">
      <h1>Welcome to Vue 3</h1>
      <p>{{ message }}</p>
    </div>
  `,
  data() {
    return {
      message: 'Modern Vue.js Application',
    };
  },
};

const About = {
  template: `
    <div class="about">
      <h1>About Page</h1>
    </div>
  `,
};

const Dashboard = {
  template: `
    <div class="dashboard">
      <h1>Dashboard</h1>
      <p>Count: {{ count }}</p>
      <button @click="increment">Increment</button>
    </div>
  `,
  setup() {
    const store = useCounterStore();
    return {
      count: store.count,
      increment: store.increment,
    };
  },
};

// Router
const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/dashboard', component: Dashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Pinia Store
import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
  }),
  actions: {
    increment() {
      this.count++;
    },
  },
});

// Create and mount app
const pinia = createPinia();
const app = createApp(App);

app.use(router);
app.use(pinia);
app.mount('#app');

export default app;
