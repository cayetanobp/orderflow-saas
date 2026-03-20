import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { CustomersService } from './customers.service';

describe('CustomersService', () => {
  let service: CustomersService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting(), CustomersService],
    });

    service = TestBed.inject(CustomersService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('lists tenant customers', () => {
    service.list().subscribe();

    const request = httpMock.expectOne('/api/v1/customers');
    expect(request.request.method).toBe('GET');
    request.flush({ count: 0, next: null, previous: null, results: [] });
  });

  it('creates a customer', () => {
    service.create({ full_name: 'Alpha', email: '', phone: '', company_name: '', notes: '' }).subscribe();

    const request = httpMock.expectOne('/api/v1/customers/');
    expect(request.request.method).toBe('POST');
    request.flush({ id: 1, full_name: 'Alpha', email: '', phone: '', company_name: '', notes: '', created_at: '', updated_at: '' });
  });
});