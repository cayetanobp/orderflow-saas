import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { DashboardSummary } from '../models/api.models';
import { apiConfig } from './api.config';

@Injectable({ providedIn: 'root' })
export class DashboardService {
  private readonly http = inject(HttpClient);

  getSummary() {
    return this.http.get<DashboardSummary>(`${apiConfig.baseUrl}/dashboard/summary`);
  }
}