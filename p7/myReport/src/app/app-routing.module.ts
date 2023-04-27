import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FirstReportComponent } from './first-report/first-report.component';
import { SecondReportComponent } from './second-report/second-report.component';

const routes: Routes = [
    {path: '', component:FirstReportComponent},
    {path: '2', component:SecondReportComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
