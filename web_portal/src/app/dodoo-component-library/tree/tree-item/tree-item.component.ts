import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-tree-item',
  templateUrl: './tree-item.component.html',
  styleUrls: ['./tree-item.component.scss']
})
export class TreeItemComponent implements OnInit {

  @Output() onClick = new EventEmitter<any>();

  constructor() { }

  ngOnInit(): void {
  }

  clicked(eevent: Event): void {
    event?.preventDefault();
    event?.stopImmediatePropagation();
    this.onClick.emit(this);
  }

}
