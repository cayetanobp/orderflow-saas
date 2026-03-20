import { CommonModule } from '@angular/common';
import { Component, effect, inject } from '@angular/core';
import { FormArray, FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { forkJoin } from 'rxjs';

import { Customer, Order, OrderItem, OrderPayload } from '../../core/models/api.models';
import { AuthService } from '../../core/services/auth.service';
import { CustomersService } from '../../core/services/customers.service';
import { OrdersService } from '../../core/services/orders.service';

@Component({
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './orders-page.component.html',
  styleUrl: './orders-page.component.css',
})
export class OrdersPageComponent {
  private readonly formBuilder = inject(FormBuilder);
  private readonly ordersService = inject(OrdersService);
  private readonly authService = inject(AuthService);
  private readonly customersService = inject(CustomersService);

  readonly statusOptions = [
    { value: 'draft', label: 'Draft' },
    { value: 'confirmed', label: 'Confirmed' },
    { value: 'in_progress', label: 'In progress' },
    { value: 'awaiting_review', label: 'Awaiting review' },
    { value: 'completed', label: 'Completed' },
    { value: 'delivered', label: 'Delivered' },
    { value: 'canceled', label: 'Canceled' },
  ];

  readonly priorityOptions = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
  ];

  readonly form = this.formBuilder.group({
    customer: [null as number | null, [Validators.required]],
    code: ['', [Validators.required]],
    title: ['', [Validators.required]],
    description: [''],
    status: ['draft', [Validators.required]],
    priority: ['medium', [Validators.required]],
    due_date: [''],
    items: this.formBuilder.array([this.createItemGroup()]),
  });

  orders: Order[] = [];
  customers: Customer[] = [];
  message = 'Load tenant orders to inspect operational flow.';
  errorMessage = '';
  successMessage = '';
  isSaving = false;
  isTransitioning = false;
  editingOrderId: number | null = null;
  deletingOrderId: number | null = null;
  transitionStatus = 'confirmed';
  transitionNote = '';

  constructor() {
    effect(() => {
      if (this.authService.isAuthenticated() && this.authService.activeTenantSlug()) {
        this.load();
      }
    });
  }

  get items() {
    return this.form.controls.items as FormArray;
  }

  get estimatedTotal() {
    return this.items.controls.reduce((total, itemControl) => {
      const quantity = Number(itemControl.get('quantity')?.value ?? 0);
      const unitPrice = Number(itemControl.get('unit_price')?.value ?? 0);
      return total + quantity * unitPrice;
    }, 0);
  }

  createItemGroup(item?: Partial<OrderItem>) {
    return this.formBuilder.group({
      name: [item?.name ?? '', [Validators.required]],
      quantity: [item?.quantity ?? 1, [Validators.required, Validators.min(1)]],
      unit_price: [item?.unit_price ?? '0.00', [Validators.required, Validators.min(0)]],
      notes: [item?.notes ?? ''],
    });
  }

  addItem(item?: Partial<OrderItem>) {
    this.items.push(this.createItemGroup(item));
  }

  removeItem(itemIndex: number) {
    if (this.items.length === 1) {
      return;
    }

    this.items.removeAt(itemIndex);
  }

  load() {
    this.message = 'Loading orders...';
    forkJoin({
      orders: this.ordersService.list(),
      customers: this.customersService.list(),
    }).subscribe({
      next: ({ orders, customers }) => {
        this.orders = orders.results;
        this.customers = customers.results;
        this.message = '';
      },
      error: () => {
        this.message = 'Orders could not be loaded. Verify authentication and tenant selection.';
      },
    });
  }

  editOrder(order: Order) {
    this.editingOrderId = order.id;
    this.errorMessage = '';
    this.successMessage = '';
    this.transitionStatus = order.status;
    this.transitionNote = '';
    this.form.patchValue({
      customer: order.customer,
      code: order.code,
      title: order.title,
      description: order.description,
      status: order.status,
      priority: order.priority,
      due_date: order.due_date ?? '',
    });

    this.items.clear();
    if (order.items.length === 0) {
      this.addItem();
      return;
    }

    for (const item of order.items) {
      this.addItem(item);
    }
  }

  resetForm() {
    this.editingOrderId = null;
    this.errorMessage = '';
    this.transitionStatus = 'confirmed';
    this.transitionNote = '';
    this.form.reset({
      customer: null,
      code: '',
      title: '',
      description: '',
      status: 'draft',
      priority: 'medium',
      due_date: '',
    });
    this.items.clear();
    this.addItem();
  }

  customerName(customerId: number) {
    return this.customers.find((customer) => customer.id === customerId)?.full_name ?? 'Unknown customer';
  }

  submit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.isSaving = true;
    this.errorMessage = '';
    this.successMessage = '';

    const payload: OrderPayload = {
      customer: Number(this.form.controls.customer.value),
      code: this.form.controls.code.value ?? '',
      title: this.form.controls.title.value ?? '',
      description: this.form.controls.description.value ?? '',
      status: this.form.controls.status.value ?? 'draft',
      priority: this.form.controls.priority.value ?? 'medium',
      due_date: this.form.controls.due_date.value || null,
      items: this.items.getRawValue() as OrderItem[],
    };

    const request$ = this.editingOrderId
      ? this.ordersService.update(this.editingOrderId, payload)
      : this.ordersService.create(payload);

    request$.subscribe({
      next: () => {
        this.isSaving = false;
        const successMessage = this.editingOrderId ? 'Order updated.' : 'Order created.';
        this.resetForm();
        this.successMessage = successMessage;
        this.load();
      },
      error: () => {
        this.isSaving = false;
        this.errorMessage = 'The order could not be saved. Review the form values and try again.';
      },
    });
  }

  deleteOrder(order: Order) {
    this.deletingOrderId = order.id;
    this.errorMessage = '';
    this.successMessage = '';

    this.ordersService.delete(order.id).subscribe({
      next: () => {
        this.deletingOrderId = null;
        this.successMessage = 'Order deleted.';
        if (this.editingOrderId === order.id) {
          this.resetForm();
        }
        this.load();
      },
      error: () => {
        this.deletingOrderId = null;
        this.errorMessage = 'The order could not be deleted.';
      },
    });
  }

  transitionSelectedOrder() {
    if (!this.editingOrderId) {
      return;
    }

    this.isTransitioning = true;
    this.errorMessage = '';
    this.successMessage = '';
    this.ordersService.transition(this.editingOrderId, { to_status: this.transitionStatus, note: this.transitionNote }).subscribe({
      next: () => {
        this.isTransitioning = false;
        this.successMessage = 'Order transitioned.';
        this.transitionNote = '';
        this.load();
      },
      error: () => {
        this.isTransitioning = false;
        this.errorMessage = 'The status transition could not be applied.';
      },
    });
  }
}