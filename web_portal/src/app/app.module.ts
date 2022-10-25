import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DodooComponentLibraryModule } from './dodoo-component-library/dodoo-component-library.module';
import { PageDashboardComponent } from './pages/page-dashboard/page-dashboard.component';

@NgModule({
  declarations: [
    AppComponent,
    PageDashboardComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    DodooComponentLibraryModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
