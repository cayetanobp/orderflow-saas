import { CommonModule } from '@angular/common';
import { Component, effect, inject } from '@angular/core';

import { DashboardService } from '../../core/services/dashboard.service';
import { AuthService } from '../../core/services/auth.service';
import { DashboardSummary } from '../../core/models/api.models';

@Component({
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard-page.component.html',
  styleUrl: './dashboard-page.component.css',
})
export class DashboardPageComponent {
  private readonly dashboardService = inject(DashboardService);
  private readonly authService = inject(AuthService);

  summary: DashboardSummary | null = null;
  message = 'Load dashboard metrics after signing in.';

  constructor() {
    effect(() => {
      if (this.authService.isAuthenticated() && this.authService.activeTenantSlug()) {
        this.load();
      }
    });
  }

  load() {
    this.message = 'Loading dashboard data...';
    this.dashboardService.getSummary().subscribe({
      next: (summary: DashboardSummary) => {
        this.summary = summary;
        this.message = '';
      },
      error: () => {
        this.message = 'Dashboard could not be loaded. Verify the backend is running and a tenant is selected.';
      },
    });
  }
}