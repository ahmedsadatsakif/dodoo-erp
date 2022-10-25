import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-sidebar-link',
  templateUrl: './sidebar-link.component.html',
  styleUrls: ['./sidebar-link.component.scss']
})
export class SidebarLinkComponent implements OnInit {

  @Input() label!: string;
  @Input() url!: string;
  @Input('active-class') activeClass: string = 'active';

  constructor() { }

  ngOnInit(): void {
  }

}
