import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { Customer, CustomerPayload, PaginatedResponse } from '../models/api.models';
import { apiConfig } from './api.config';

@Injectable({ providedIn: 'root' })
export class CustomersService {
  private readonly http = inject(HttpClient);

  list() {
    return this.http.get<PaginatedResponse<Customer>>(`${apiConfig.baseUrl}/customers`);
  }

  create(payload: CustomerPayload) {
    return this.http.post<Customer>(`${apiConfig.baseUrl}/customers/`, payload);
  }

  update(customerId: number, payload: Partial<CustomerPayload>) {
    return this.http.patch<Customer>(`${apiConfig.baseUrl}/customers/${customerId}/`, payload);
  }

  delete(customerId: number) {
    return this.http.delete<void>(`${apiConfig.baseUrl}/customers/${customerId}/`);
  }
}