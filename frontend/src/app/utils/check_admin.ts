import { EventEmitter } from '@angular/core';

export class CheckAdmin {
  static checkAdminEmitter = new EventEmitter<boolean>();
}
