import { Component, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule, Routes } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

// Main App Component
@Component({
  selector: 'app-root',
  template: `
    <div class="app-container">
      <nav>
        <a routerLink="/">Home</a>
        <a routerLink="/about">About</a>
        <a routerLink="/dashboard">Dashboard</a>
      </nav>
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [`
    .app-container {
      font-family: Arial, sans-serif;
    }
    nav {
      padding: 1rem;
      background: #333;
    }
    nav a {
      color: white;
      margin: 0 1rem;
      text-decoration: none;
    }
  `]
})
export class AppComponent {
  title = 'Angular Application';
}

// Home Component
@Component({
  selector: 'app-home',
  template: `
    <div class="home">
      <h1>Welcome to Angular</h1>
      <p>{{ message }}</p>
    </div>
  `
})
export class HomeComponent {
  message = 'Modern Angular Application';
}

// About Component
@Component({
  selector: 'app-about',
  template: `
    <div class="about">
      <h1>About Page</h1>
      <p>This is an Angular application</p>
    </div>
  `
})
export class AboutComponent {}

// Dashboard Component
@Component({
  selector: 'app-dashboard',
  template: `
    <div class="dashboard">
      <h1>Dashboard</h1>
      <p>Count: {{ count }}</p>
      <button (click)="increment()">Increment</button>
    </div>
  `
})
export class DashboardComponent {
  count = 0;

  increment() {
    this.count++;
  }
}

// Routes
const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'about', component: AboutComponent },
  { path: 'dashboard', component: DashboardComponent },
];

// App Module
@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    AboutComponent,
    DashboardComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule.forRoot(routes),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
