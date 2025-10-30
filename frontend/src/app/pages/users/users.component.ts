import { Component, OnInit } from '@angular/core';
import { UsersService } from '../../services/users-service.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css'],
})
export class UsersComponent implements OnInit {
  selectedUser: any = null;
  users: any[] = [];

  constructor(private userService: UsersService, private router: Router) {}

  ngOnInit(): void {
    this.userService.getAllUsers().subscribe((result: any) => {
      this.users = result.users;
    });
  }

  removeUser(id: number): void {
    this.userService.deleteUser(id).subscribe(() => {
      this.users = this.users.filter((user) => user.id !== id);
    });
  }
}
