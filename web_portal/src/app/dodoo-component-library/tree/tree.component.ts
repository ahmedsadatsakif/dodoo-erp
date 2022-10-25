import { Component, AfterContentInit, ContentChildren, QueryList } from '@angular/core';
import { TreeLevelComponent } from './tree-level/tree-level.component';

@Component({
  selector: 'app-tree',
  templateUrl: './tree.component.html',
  styleUrls: ['./tree.component.scss']
})
export class TreeComponent implements AfterContentInit {

  @ContentChildren(TreeLevelComponent, { descendants: false}) levels !: QueryList<TreeLevelComponent>;

  constructor() { }

  ngAfterContentInit(): void {
    console.info(this.levels);
    this.levels.forEach((item) => { item.collapse() });
    this.levels.get(0)?.expand();
  }

  collapse(){}

  expand(){}

}
