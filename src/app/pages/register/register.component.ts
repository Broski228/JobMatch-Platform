import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  method = 'other';
  login = '';
  password = '';
  role = 'worker';
  name = '';
  surname = '';
  patronymic = '';
  email = '';
  phone = '';
  address = '';
  company = '';
  methods = [
    { id: 'google', label: 'Google' },
    { id: 'icloud', label: 'iCloud' },
    { id: 'phone', label: 'Телефон' },
    { id: 'other', label: 'Другие' }
  ];
  constructor(private router: Router) {}
  selectMethod(value: string): void { this.method = value; }
  submit(): void {
    if (!this.login || !this.password || !this.name || !this.surname) {
      alert('Заполни обязательные поля');
      return;
    }
    const raw = localStorage.getItem('users');
    const users = raw ? JSON.parse(raw) : [];
    const exists = users.find((u: any) => u.login === this.login);
    if (exists) {
      alert('Такой логин уже существует');
      return;
    }
    const user = {
      id: Date.now(),
      method: this.method,
      login: this.login,
      password: this.password,
      role: this.role,
      name: this.name,
      surname: this.surname,
      patronymic: this.patronymic,
      email: this.email,
      phone: this.phone,
      address: this.address,
      company: this.company,
      resumes: [],
      favorites: [],
      notifications: []
    };
    users.push(user);
    localStorage.setItem('users', JSON.stringify(users));
    localStorage.setItem('currentUser', JSON.stringify(user));
    this.router.navigate(['/home']);
  }
}