import { of } from 'rxjs';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AuthService } from '../../core/services/auth.service';
import { CustomersService } from '../../core/services/customers.service';
import { CustomersPageComponent } from './customers-page.component';

describe('CustomersPageComponent', () => {
  let fixture: ComponentFixture<CustomersPageComponent>;
  let component: CustomersPageComponent;
  const customersService = {
    list: jasmine.createSpy('list').and.returnValue(of({ results: [] })),
    create: jasmine.createSpy('create').and.returnValue(of({ id: 1 })),
    update: jasmine.createSpy('update').and.returnValue(of({ id: 1 })),
    delete: jasmine.createSpy('delete').and.returnValue(of(void 0)),
  };
  const authService = {
    isAuthenticated: () => true,
    activeTenantSlug: () => 'northwind-print',
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CustomersPageComponent],
      providers: [
        { provide: CustomersService, useValue: customersService },
        { provide: AuthService, useValue: authService },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(CustomersPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('submits a new customer when the form is valid', () => {
    component.form.setValue({
      full_name: 'Customer Name',
      email: '',
      phone: '',
      company_name: '',
      notes: '',
    });

    component.submit();

    expect(customersService.create).toHaveBeenCalled();
  });
});