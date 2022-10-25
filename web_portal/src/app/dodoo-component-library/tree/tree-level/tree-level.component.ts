import { Component, AfterContentInit, QueryList, ContentChild, ContentChildren } from '@angular/core';
import { TreeItemComponent } from '../tree-item/tree-item.component';

@Component({
  selector: 'app-tree-level',
  templateUrl: './tree-level.component.html',
  styleUrls: ['./tree-level.component.scss']
})
export class TreeLevelComponent implements AfterContentInit {

  collapsed = false;

  @ContentChild(TreeItemComponent) toggler !: TreeItemComponent;
  @ContentChildren(TreeLevelComponent, { descendants: false }) levels !: QueryList<TreeLevelComponent>;

  constructor() { }

  ngAfterContentInit(): void {
    this.toggler.onClick.asObservable().subscribe({
      next: (event) => {
        this.collapsed == true ? this.expand() : this.collapse();
      }
    })
  }

  expand() {
    console.info('Expand Called');
    this.collapsed = false;
  }

  collapse() {
    console.info('Collapse Called');
    this.collapsed = true;
    this.levels.forEach((level) => level.collapse());
  }

}
