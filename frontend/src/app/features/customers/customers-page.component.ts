import { CommonModule } from '@angular/common';
import { Component, effect, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { Customer, CustomerPayload } from '../../core/models/api.models';
import { AuthService } from '../../core/services/auth.service';
import { CustomersService } from '../../core/services/customers.service';

@Component({
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './customers-page.component.html',
  styleUrl: './customers-page.component.css',
})
export class CustomersPageComponent {
  private readonly formBuilder = inject(FormBuilder);
  private readonly customersService = inject(CustomersService);
  private readonly authService = inject(AuthService);

  readonly form = this.formBuilder.group({
    full_name: ['', [Validators.required]],
    email: ['', [Validators.email]],
    phone: [''],
    company_name: [''],
    notes: [''],
  });

  customers: Customer[] = [];
  message = 'Load tenant customers after selecting a tenant.';
  errorMessage = '';
  successMessage = '';
  isSaving = false;
  editingCustomerId: number | null = null;
  deletingCustomerId: number | null = null;

  constructor() {
    effect(() => {
      if (this.authService.isAuthenticated() && this.authService.activeTenantSlug()) {
        this.load();
      }
    });
  }

  load() {
    this.message = 'Loading customers...';
    this.customersService.list().subscribe({
      next: (response: { results: Customer[] }) => {
        this.customers = response.results;
        this.message = '';
      },
      error: () => {
        this.message = 'Customers could not be loaded. Verify authentication and the active tenant header.';
      },
    });
  }

  editCustomer(customer: Customer) {
    this.editingCustomerId = customer.id;
    this.errorMessage = '';
    this.successMessage = '';
    this.form.setValue({
      full_name: customer.full_name,
      email: customer.email,
      phone: customer.phone,
      company_name: customer.company_name,
      notes: customer.notes,
    });
  }

  resetForm() {
    this.editingCustomerId = null;
    this.errorMessage = '';
    this.form.reset({
      full_name: '',
      email: '',
      phone: '',
      company_name: '',
      notes: '',
    });
  }

  submit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.isSaving = true;
    this.errorMessage = '';
    this.successMessage = '';
    const payload = this.form.getRawValue() as CustomerPayload;
    const request$ = this.editingCustomerId
      ? this.customersService.update(this.editingCustomerId, payload)
      : this.customersService.create(payload);

    request$.subscribe({
      next: () => {
        this.isSaving = false;
        const successMessage = this.editingCustomerId ? 'Customer updated.' : 'Customer created.';
        this.resetForm();
        this.successMessage = successMessage;
        this.load();
      },
      error: () => {
        this.isSaving = false;
        this.errorMessage = 'The customer could not be saved. Review the form and try again.';
      },
    });
  }

  deleteCustomer(customer: Customer) {
    this.deletingCustomerId = customer.id;
    this.errorMessage = '';
    this.successMessage = '';

    this.customersService.delete(customer.id).subscribe({
      next: () => {
        this.deletingCustomerId = null;
        if (this.editingCustomerId === customer.id) {
          this.resetForm();
        }
        this.successMessage = 'Customer deleted.';
        this.load();
      },
      error: () => {
        this.deletingCustomerId = null;
        this.errorMessage = 'The customer could not be deleted.';
      },
    });
  }
}