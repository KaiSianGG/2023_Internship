import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FirstReportComponent } from './first-report/first-report.component';
import { SecondReportComponent } from './second-report/second-report.component';

@NgModule({
  declarations: [
    AppComponent,
    FirstReportComponent,
    SecondReportComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
