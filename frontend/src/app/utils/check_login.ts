import { EventEmitter } from '@angular/core';

export class CheckLogin {
  static checkLoginEmitter = new EventEmitter<boolean>();
}
