import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from './sidebar/sidebar.component';
import { TreeComponent } from './tree/tree.component';
import { TreeLevelComponent } from './tree/tree-level/tree-level.component';
import { TreeItemComponent } from './tree/tree-item/tree-item.component';
import { SidebarLinkComponent } from './sidebar/sidebar-link/sidebar-link.component';
import { RouterModule } from '@angular/router';
import { DataTableComponent } from './data-table/data-table.component';



@NgModule({
  declarations: [
    SidebarComponent,
    SidebarLinkComponent,
    TreeComponent,
    TreeLevelComponent,
    TreeItemComponent,
    DataTableComponent,
  ],
  exports: [
    SidebarComponent,
    SidebarLinkComponent,
    TreeComponent,
    TreeLevelComponent,
    TreeItemComponent,
    DataTableComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ]
})
export class DodooComponentLibraryModule { }
