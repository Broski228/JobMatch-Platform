import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  login = '';
  password = '';
  constructor(private router: Router) {}
  submit(): void {
    const raw = localStorage.getItem('users');
    const users = raw ? JSON.parse(raw) : [];
    const found = users.find((u: any) => u.login === this.login && u.password === this.password);
    if (!found) {
      alert('Неверный логин или пароль');
      return;
    }
    localStorage.setItem('currentUser', JSON.stringify(found));
    this.router.navigate(['/home']);
  }
}