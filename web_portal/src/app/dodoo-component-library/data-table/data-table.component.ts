import { Component, OnInit, Input } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'app-data-table',
  templateUrl: './data-table.component.html',
  styleUrls: ['./data-table.component.scss']
})
export class DataTableComponent implements OnInit {

  @Input() module!: string;
  @Input() model!: string;
  @Input('page-size') pageSize: number = 100;

  headers = new BehaviorSubject<any[]>([
    { label: 'Id', key: 'id', widget: 'Text' },
    { label: 'Name', key: 'name', widget: 'Text' },
    { label: 'Data 1', key: 'data_1', widget: 'Text' }
  ]);
  dataset = new BehaviorSubject<any[]>([
    { id: 1, name: 'Sadat', data_1: 'Test 1' },
    { id: 2, name: 'Sakif', data_1: 'Test 2' },
    { id: 3, name: 'Ahmed', data_1: 'Test 3' },
    { id: 4, name: 'Ornab', data_1: 'Test 4' },
    { id: 5, name: 'Jessie', data_1: 'Test 5' },
    { id: 6, name: 'Daru', data_1: 'Test 6' },
  ]);

  getRowData(row: any) {
    const out = [];
    for (const head of this.headers.value) {
      out.push(row[head.key]);
    }
    return out;
  }

  constructor() { }

  ngOnInit(): void {
  }

}
