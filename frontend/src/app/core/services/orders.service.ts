import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { Order, OrderPayload, OrderTransitionPayload, PaginatedResponse } from '../models/api.models';
import { apiConfig } from './api.config';

@Injectable({ providedIn: 'root' })
export class OrdersService {
  private readonly http = inject(HttpClient);

  list() {
    return this.http.get<PaginatedResponse<Order>>(`${apiConfig.baseUrl}/orders`);
  }

  create(payload: OrderPayload) {
    return this.http.post<Order>(`${apiConfig.baseUrl}/orders/`, payload);
  }

  update(orderId: number, payload: Partial<OrderPayload>) {
    return this.http.patch<Order>(`${apiConfig.baseUrl}/orders/${orderId}/`, payload);
  }

  delete(orderId: number) {
    return this.http.delete<void>(`${apiConfig.baseUrl}/orders/${orderId}/`);
  }

  transition(orderId: number, payload: OrderTransitionPayload) {
    return this.http.post(`${apiConfig.baseUrl}/orders/${orderId}/transition/`, payload);
  }
}