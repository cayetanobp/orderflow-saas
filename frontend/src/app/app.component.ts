import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive, RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  readonly authService = inject(AuthService);
  private readonly router = inject(Router);
  isMenuOpen = false;

  toggleMenu() { this.isMenuOpen = !this.isMenuOpen; }

  setTenant(tenantSlug: string) {
    this.authService.setActiveTenant(tenantSlug);
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}