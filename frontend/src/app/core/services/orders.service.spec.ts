import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { OrdersService } from './orders.service';

describe('OrdersService', () => {
  let service: OrdersService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting(), OrdersService],
    });

    service = TestBed.inject(OrdersService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('creates an order', () => {
    service
      .create({
        customer: 1,
        code: 'ORD-1',
        title: 'Order',
        description: '',
        status: 'draft',
        priority: 'medium',
        due_date: null,
        items: [],
      })
      .subscribe();

    const request = httpMock.expectOne('/api/v1/orders/');
    expect(request.request.method).toBe('POST');
    request.flush({ id: 1 });
  });

  it('transitions an order', () => {
    service.transition(4, { to_status: 'confirmed', note: 'Ready' }).subscribe();

    const request = httpMock.expectOne('/api/v1/orders/4/transition/');
    expect(request.request.method).toBe('POST');
    request.flush({ id: 11 });
  });
});